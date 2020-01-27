import argparse
import json
from detection.utils import *
from os.path import splitext, basename, join


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--input", required=True, help="input image")
	ap.add_argument("-s", "--scale", type=float, default=0.1, help="scale images by this factor (default: x0.1)")
	ap.add_argument("-c", "--config", type=str, default="config.json",
					help="name file to load config (default: config.json)")
	ap.add_argument("-o", "--output", type=str, help="give a directory name to save the game files in it")
	ap.add_argument("--hide", action='store_true', default=False, help="hide images")

	args = vars(ap.parse_args())
	with open(args['config'], 'r') as file:
		config = json.load(file)

	orig, blob_mask, blob, food_mask, food_img, food_list = detect(args['input'], config)
	discrete_img, discrete_blob, discrete_food_list, known_food = discretize(blob, food_list, config['Discrete Width'],
																			 config['Discrete Height'])

	if args['output'] is not None:
		filename = splitext(basename(args['input']))[0]
		dir = args['output']
		save(join(dir, filename), discrete_img, discrete_blob, discrete_food_list, known_food)

	if not args['hide']:
		print_results(orig, blob_mask, blob, food_mask, food_img, discrete_img, args['scale'])


def detect(input_file, config):

	img = cv2.imread(input_file)
	height, width, _ = img.shape

	aspect_ratio = config["Aspect Ratio"]

	height = int(width*aspect_ratio)

	""" Resize image to limits in config file """
	limits = np.array(config['Limits'])
	transform_mat = cv2.getPerspectiveTransform(np.float32(limits), np.float32(
		[[0, 0], [width, 0], [width, height], [0, height]]))
	img = cv2.warpPerspective(img, transform_mat, (width, height))

	""" Prepare upper and lower mask board """
	upper_mask = np.zeros(img.shape[0:2], np.uint8)
	lower_mask = np.zeros(img.shape[0:2], np.uint8)

	upper_mask = cv2.rectangle(upper_mask, (0, 0), (width, int(height/2)), 255, thickness=cv2.FILLED)
	lower_mask = cv2.rectangle(lower_mask, (0, int(height / 2)), (width, height), 255, thickness=cv2.FILLED)

	""" Find blob """
	sat = saturation(img)
	# sum = mean_image([satA, satB])
	blob_mask = find_blob(sat)
	blob = cv2.bitwise_and(img, img, mask=blob_mask)

	""" Print blob information """
	print("Blob covering:")
	print("\t{:.2f}% of the board.".format(mean_percent_value(blob_mask)))
	print("\t{:.2f}% of the upper board.".format(
		mean_percent_value(cv2.bitwise_and(blob_mask, blob_mask, mask=upper_mask), img_ratio=0.5)))
	print("\t{:.2f}% of the lower board.".format(
		mean_percent_value(cv2.bitwise_and(blob_mask, blob_mask, mask=lower_mask), img_ratio=0.5)))

	""" Find food """
	food_list, food_mask, food_img = find_food(img, 100, config['Low Food Color'], config['High Food Color'])

	""" Print food information """
	print("Total food discovered: " + str(len(food_list)))
	for i, food in enumerate(food_list):
		print("\tFood N°" + str(i) + ": " + str(food))

	return img, blob_mask, blob, food_mask, food_img, food_list


def print_results(orig, blob_mask, blob, food_mask, food, discrete, scale=1.0):
		padding = 35
		nbr_width = 2
		nbr_height = 3
		font = cv2.FONT_HERSHEY_SIMPLEX
		fontsize = 0.45
		thickness = 1

		scaled_height = int(orig.shape[0]*scale)
		scaled_width = int(orig.shape[1]*scale)

		pad = np.zeros((scaled_height, padding, orig.shape[2]), dtype=np.uint8)
		line_pad = np.zeros((padding, (scaled_width + padding) * nbr_width + padding, orig.shape[2]), dtype=np.uint8)
		print_img = cv2.resize(orig, (scaled_width, scaled_height))

		middle = ((0, int(scaled_height/2)), (scaled_width, int(scaled_height/2)))
		cv2.line(print_img, middle[0], middle[1], (0, 255, 0), thickness=1)
		cv2.putText(print_img, 'Mid Line', (middle[0][0] + 5, middle[0][1] - 5),
					font, fontsize, (0, 255, 0), thickness, cv2.LINE_AA)

		print_blob_mask = cv2.resize(cv2.cvtColor(blob_mask, cv2.COLOR_GRAY2BGR), (scaled_width, scaled_height))
		print_blob = cv2.resize(blob, (scaled_width, scaled_height))
		print_food_mask = cv2.resize(cv2.cvtColor(food_mask, cv2.COLOR_GRAY2BGR), (scaled_width, scaled_height))
		print_food = cv2.resize(food, (scaled_width, scaled_height))
		print_discrete = cv2.resize(discrete, (scaled_width, scaled_height))

		concat_line1 = np.concatenate((pad, print_img, pad, print_discrete, pad), axis=1)
		concat_line2 = np.concatenate((pad, print_blob_mask, pad, print_blob, pad), axis=1)
		concat_line3 = np.concatenate((pad, print_food_mask, pad, print_food, pad), axis=1)

		aggregate = np.concatenate((line_pad, concat_line1, line_pad, concat_line2, line_pad, concat_line3, line_pad))

		cv2.putText(aggregate, 'Original:',
					(0 * (scaled_width + padding) + padding + 5, 0 * (scaled_height + padding) + padding - 5),
					font, fontsize, (255, 255, 255), thickness, cv2.LINE_AA)
		cv2.putText(aggregate, 'Discrete:',
					(1 * (scaled_width + padding) + padding + 5, 0 * (scaled_height + padding) + padding - 5),
					font, fontsize, (255, 255, 255), thickness, cv2.LINE_AA)
		cv2.putText(aggregate, 'Blob Mask:',
					(0 * (scaled_width + padding) + padding + 5, 1 * (scaled_height + padding) + padding - 5),
					font, fontsize, (255, 255, 255), thickness, cv2.LINE_AA)
		cv2.putText(aggregate, 'Blob:',
					(1 * (scaled_width + padding) + padding + 5, 1 * (scaled_height + padding) + padding - 5),
					font, fontsize, (255, 255, 255), thickness, cv2.LINE_AA)
		cv2.putText(aggregate, 'Food Mask:',
					(0 * (scaled_width + padding) + padding + 5, 2 * (scaled_height + padding) + padding - 5),
					font, fontsize, (255, 255, 255), thickness, cv2.LINE_AA)
		cv2.putText(aggregate, 'Food Regions:',
					(1 * (scaled_width + padding) + padding + 5, 2 * (scaled_height + padding) + padding - 5),
					font, fontsize, (255, 255, 255), thickness, cv2.LINE_AA)

		cv2.imshow("Results", aggregate)
		print("\nPress any key...")
		cv2.waitKey(0)


def discretize(blob_img, food_list, width, height):
	img_height, img_width, _ = blob_img.shape

	discrete_blob = cv2.resize(blob_img, (width, height), interpolation=cv2.INTER_NEAREST)

	discrete_food_list = []
	for food in food_list:
		x = int((food[0] + food[2]/2) / img_width * width)
		y = int((food[1] + food[3]/2) / img_height * height)
		discrete_food_list.append((x,y))

	height, width, _ = discrete_blob.shape
	discrete_blob = cv2.cvtColor(discrete_blob, cv2.COLOR_BGR2GRAY)

	known_food = []
	for food in discrete_food_list:
		if discrete_blob[food[1], food[0]] != 0:
			known_food.append([food[0], food[1]])

	discrete_blob_bgr = cv2.cvtColor(discrete_blob, cv2.COLOR_GRAY2BGR)
	discrete_img = cv2.resize(discrete_blob_bgr, (0, 0), fx=10, fy=10, interpolation=cv2.INTER_NEAREST)
	for (x, y) in discrete_food_list:
		cv2.rectangle(discrete_img, (x * 10, y * 10), ((x + 1) * 10, (y + 1) * 10), (0, 255, 0), thickness=cv2.FILLED)

	for (x, y) in known_food:
		cv2.drawMarker(discrete_img, (x * 10 + 5, y * 10 + 5), (255, 255, 255), thickness=2, markerSize=9,
						markerType=cv2.MARKER_TILTED_CROSS)

	return discrete_img, discrete_blob, discrete_food_list, known_food


def save(filename, discrete_img, discrete_blob, discrete_food_list, known_food):

	height, width = discrete_blob.shape

	# TODO Add size in output if told so
	board_str = str(width) + ' ' + str(height) + '\n'
	for x in range(height):
		for y in range(width):
			board_str += format(discrete_blob[x, y] != 0, 'd') + "," + format((y, x) in discrete_food_list, 'd') \
						+ "," + str(discrete_blob[x, y]) + " "
		board_str = board_str[:-1]
		board_str += "\n"
	board_str = board_str[:-1]

	with open(filename + ".board", 'w') as board_file:
		board_file.write(board_str)

	with open(filename + ".blob", 'w') as blob_file:
		knowledge = dict()
		knowledge['food'] = known_food
		knowledge['max_scouters'] = len(known_food)
		json.dump(knowledge, blob_file)

	with open(filename + ".player", 'w') as player_file:
		player_file.write("0")

	cv2.imwrite(filename + ".jpg", discrete_img)


if __name__ == "__main__":
	main()
