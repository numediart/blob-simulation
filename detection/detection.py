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

from detection.utils import *
from math import ceil


def detect(input_file, config):
    """
    Starts blob detection in the image and returns
    - the part of the image used (resized and warp perpective)
    - blob mask detected
    - blob segmented image
    - food mask detected
    - the image with food regions

    :param input_file: string filename for jpeg image detection
    :param config: dict with config used for detection
    """
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
    food_list, food_mask, food_img = find_food(img, config['Min Food Size'], config['Low Food Color'], config['High Food Color'])

    """ Print food information """
    print("Total food discovered: " + str(len(food_list)))
    # for i, food in enumerate(food_list):
        # print("\tFood N°" + str(i) + ": " + str(food))

    return img, blob_mask, blob, food_mask, food_img


def print_results(labels, images, scale=1.0, filename=None, hide=False, nbr_width=2):
    """
    Aggregate and show images in one window with each label displayed at the top of them.
    It can as well save the aggregated image.
    Each line contains 'nbr_width' images.
    If the number of images doesn't fit the last line, it's padded with a zero image.

    :param labels: each label to use for each image in images. assert len(labels) == len(images)
    :param images: each image to print in results window
    :param scale: the scale to use for results window with respect to image size
    :param filename: if provide, save results window under 'filename'.jpg name
    :param hide: if true, the results window isn't shown
    :param nbr_width: number of images to fit in line
    """
    padding = 35
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontsize = 0.45
    thickness = 1

    scaled_height = int(images[0].shape[0]*scale)
    scaled_width = int(images[0].shape[1]*scale)
    pad = np.zeros((scaled_height, padding, 3), dtype=np.uint8)
    line_pad = np.zeros((padding, (scaled_width + padding) * nbr_width + padding, 3), dtype=np.uint8)
    img_pad = np.zeros((scaled_height, scaled_width, 3), dtype=np.uint8)

    print_images = []
    for image in images:
        full_color = image if len(image.shape) == 3 else cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        print_image = cv2.resize(full_color, (scaled_width, scaled_height))
        print_images.append(print_image)

    middle = ((0, int(scaled_height / 2)), (scaled_width, int(scaled_height / 2)))
    cv2.line(print_images[0], middle[0], middle[1], (0, 255, 0), thickness=1)
    cv2.putText(print_images[0], 'Mid Line', (middle[0][0] + 5, middle[0][1] - 5),
                font, fontsize, (0, 255, 0), thickness, cv2.LINE_AA)

    lines = [line_pad]
    for j in range(ceil(len(images)/nbr_width)):
        concat_line = [pad]
        for i in range(nbr_width):
            if i + j * nbr_width < len(images):
                concat_line.append(print_images[i + j * nbr_width])
            else:
                concat_line.append(img_pad)
            concat_line.append(pad)

        lines.append(np.concatenate(tuple(concat_line), axis=1))
        lines.append(line_pad)

    aggregate = np.concatenate(tuple(lines))

    for i in range(len(print_images)):
        cv2.putText(aggregate, labels[i],
                    ((i % nbr_width) * (scaled_width + padding) + padding + 5,
                     int(i/nbr_width) * (scaled_height + padding) + padding - 5),
                    font, fontsize, (255, 255, 255), thickness, cv2.LINE_AA)

    if filename is not None:
        cv2.imwrite(filename + ".jpg", aggregate)

    if not hide:
        cv2.imshow("Results", aggregate)
        print("\nPress any key...")
        cv2.waitKey(0)


def discretize(blob_img, food_mask, width, height):
    """
    Transform blob and foods into a numeric blob and foods with discrete 'width' and 'height' resolution

    :param blob_img: a blob segmented numpy image
    :param food_mask: a food mask numpy image
    :param width: (int) the discrete width resolution
    :param height: (int) the discrete height resolution
    :return: the new image (as a saved simulated-like), the blob values in the image and the complete food position list
    """
    img_height, img_width, _ = blob_img.shape

    discrete_blob = cv2.resize(blob_img, (width, height), interpolation=cv2.INTER_NEAREST)

    discrete_food = cv2.resize(food_mask, (width, height), interpolation=cv2.INTER_NEAREST)

    discrete_food_list = []
    for x in range(height):
        for y in range(width):
            if discrete_food[x, y] != 0:
                discrete_food_list.append((y, x))

    height, width, _ = discrete_blob.shape
    discrete_blob = cv2.cvtColor(discrete_blob, cv2.COLOR_BGR2GRAY)

    # If discrete blob has to be connected, used this :
    # contours, hierarchy = cv2.findContours(discrete_blob, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # c = max(contours, key=cv2.contourArea)
    # mask = np.zeros(discrete_blob.shape, np.uint8)
    # cv2.drawContours(mask, [c], -1, 255, cv2.FILLED)
    # discrete_blob = cv2.bitwise_and(discrete_blob, discrete_blob, mask=mask)

    discrete_blob_bgr = cv2.cvtColor(discrete_blob, cv2.COLOR_GRAY2BGR)
    discrete_img = cv2.resize(discrete_blob_bgr, (0, 0), fx=10, fy=10, interpolation=cv2.INTER_NEAREST)
    for (x, y) in discrete_food_list:
        cv2.rectangle(discrete_img, (x * 10, y * 10), ((x + 1) * 10, (y + 1) * 10), (0, 255, 0), thickness=cv2.FILLED)
        if discrete_blob[y, x] != 0:
            cv2.drawMarker(discrete_img, (x * 10 + 5, y * 10 + 5), (255, 255, 255), thickness=2, markerSize=9,
                           markerType=cv2.MARKER_TILTED_CROSS)

    return discrete_img, discrete_blob, discrete_food_list
