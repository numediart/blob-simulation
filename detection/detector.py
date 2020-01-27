# Copyright (C) 2019 - UMons
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import argparse
import json
from detection.utils import *


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--input", default='data/_MG_0133.JPG', help="input image")
	ap.add_argument("-s", "--scale", type=float, default=0.1, help="based on the image shapes, scale the results by this factor")
	ap.add_argument("-f", "--file", type=str, default="setup.json", help="name file to load setup")

	args = vars(ap.parse_args())

	with open(args["file"], 'r') as file:
		setup = json.load(file)

	img = cv2.imread(args["input"])
	height, width, _ = img.shape

	global scale
	scale = args["scale"]

	limits = np.array(setup['Limits'])
	M = cv2.getPerspectiveTransform(np.float32(limits), np.float32(
		[[0, 0], [width, 0], [width, height], [0, height]]))
	img = cv2.warpPerspective(img, M, (width, height))

	upper_mask = cv2.rectangle(np.zeros(img.shape[0:2], np.uint8), (0, 0), (width, int(height/2)), 255)
	lower_mask = cv2.rectangle(np.zeros(img.shape[0:2], np.uint8), (0, int(height / 2)), (width, height), 255)

	show_img("Original", img)
	blob = blob_finder(img, 70, upper_mask, lower_mask, middle=[(0, int(height / 2)), (width, int(height/2))])
	foods = food_finder(img, setup['Low Food Color'], setup['High Food Color'])

	num_blob, num_food = numerize_blob(blob, foods, 100, 40)
	write_board(num_blob, num_food)

	cv2.waitKey(0)

def write_board(numerized_blob, numerized_food):
	height, width, _ = numerized_blob.shape
	gray = cv2.cvtColor(numerized_blob, cv2.COLOR_BGR2GRAY)
	output = ''
	for x in range(height):
		for y in range(width):
			output += format(gray[x, y] != 0, 'd') + "," + format((y, x) in numerized_food, 'd') \
						+ "," + str(gray[x, y]) + " "
		output = output[:-1]
		output += "\n"

	print(output)

	known_food = []
	for food in numerized_food:
		if gray[food[1], food[0]] != 0:
			known_food.append([food[0], food[1]])

	print(known_food)
	print(len(known_food))

def show_img(name, img):
	cv2.imshow(name, cv2.resize(img, (0,0), fx=scale, fy=scale))


def food_finder(img, low, high):
	foods, mask, food_img = find_food(img, 100, low, high)

	for food in foods:
		print(food)
	print("Food discovered: " + str(len(foods)))

	filled_mask = cv2.bitwise_and(img, img, mask=mask)

	show_img("Foods Mask", filled_mask)
	show_img("Foods", food_img)

	return foods


def blob_finder(img, board_ratio, upper_mask, lower_mask, limits=None, middle=None):
	sat = saturation(img)
	# sum = mean_image([satA, satB])
	mask = find_blob(sat)
	blob = cv2.bitwise_and(img, img, mask=mask)

	cover = mean_percent_value(mask)
	print("Blob covering:")
	print("--- {:.2f}% of the image.".format(cover))
	print("--- {:.2f}% of the board.".format(cover / board_ratio * 100))

	upper_cover = mean_percent_value(cv2.bitwise_and(mask, mask, mask=upper_mask)) / mean_percent_value(upper_mask) * 100
	lower_cover = mean_percent_value(cv2.bitwise_and(mask, mask, mask=lower_mask)) / mean_percent_value(lower_mask) * 100
	print("--- {:.2f}% of the upper board.".format(upper_cover))
	print("--- {:.2f}% of the lower board.".format(lower_cover))

	blob_grid = blob.copy()

	if limits is not None:
		for i, limit in enumerate(limits):
			cv2.line(blob_grid, tuple(limits[i-1]), tuple(limit), (0, 0, 255), thickness=5)
	if middle is not None:
		cv2.line(blob_grid, tuple(middle[0]), tuple(middle[1]), (0, 255, 0), thickness=5)

	show_img("Blob Mask", mask)
	show_img("Blob", blob_grid)

	return blob


def numerize_blob(img, foods, width, height):
	img_height, img_width, _ = img.shape
	numerized_blob = cv2.resize(img, (width, height), interpolation=cv2.INTER_NEAREST)
	numerized_food = []

	scaled = cv2.resize(numerized_blob, (0, 0), fx=10, fy=10, interpolation=cv2.INTER_NEAREST)
	for food in foods:
		x = int((food[0] + food[2]/2) / img_width * width)
		y = int((food[1] + food[3]/2) / img_height * height)
		numerized_food.append((x,y))
		cv2.drawMarker(scaled, (x *10 + 5, y * 10 + 5), (0, 0, 255), thickness=1)

	cv2.imshow("Test", scaled)

	return numerized_blob, numerized_food


if __name__ == "__main__":
	main()
