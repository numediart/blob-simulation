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

import cv2
import numpy as np
import imutils


def saturation(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return hsv[:, :, 1]


def mean_image(images):
    mean = np.zeros(images[0].shape)

    for image in images:
        mean += image/len(images)

    return mean.astype(np.uint8)


# If percentage should be linked to a smaller region than whole image, fill img_ratio with factor value
def mean_percent_value(img, img_ratio=1.0):
    return np.sum(img, dtype=np.int64) / img_ratio / img.size / 255 * 100


def find_food(img, min_food_size, lower_color_boundary, upper_color_boundary, kernel=None):
    img = img.copy()
    lower = np.array(lower_color_boundary, dtype="uint8")
    upper = np.array(upper_color_boundary, dtype="uint8")

    mask = cv2.inRange(img, lower, upper)

    if kernel is None:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(min_food_size/2), int(min_food_size/2)))

    cleaned = mask
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)

    cnts = cv2.findContours(cleaned.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    foods = []
    mask = np.zeros(img.shape[0:2], np.uint8)

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)

        if w >= min_food_size and h >= min_food_size:
            foods.append((x, y, w, h))
            cv2.drawContours(mask, [c], -1, 255, cv2.FILLED)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 10)

    return foods, mask, img


# Set area_ratio to 0 if you want to have the maximum possible blobs.
# Otherwise adding of blobs is break when the next blob to add is smaller than the first blob times the area_ratio
def find_blob(sat_img, max_blob=1, area_ratio=0.8, kernel=None):
    blur = cv2.GaussianBlur(sat_img, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    if kernel is None:
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))

    cleaned = thresh
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)

    contours, hierarchy = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    blobs = []

    while len(contours) != 0 and len(blobs) < max_blob:
        c = max(contours, key=cv2.contourArea)
        if len(blobs) != 0 and cv2.contourArea(blobs[0]) * area_ratio >= cv2.contourArea(c):
            break
        blobs.append(c)
        contours.remove(c)

    mask = np.zeros(sat_img.shape, np.uint8)
    cv2.drawContours(mask, blobs, -1, 255, cv2.FILLED)

    kept_cleaned = cv2.bitwise_and(cleaned, cleaned, mask=mask)

    return kept_cleaned
