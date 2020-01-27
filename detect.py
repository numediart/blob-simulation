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
from detection.detection import detect, discretize, print_results
from detection.refine import simulate, save
from os.path import splitext, basename, join


def main():
    ap = argparse.ArgumentParser("Detect a blob and foods in an image.")
    ap.add_argument("input", metavar="INPUT", help="Uses this input as image for detection")
    ap.add_argument("-s", "--scale", type=float, default=0.10, help="Scales images by this factor (default: x0.1)")
    ap.add_argument("-c", "--config", type=str, default="detection/config.json",
                    help="Loads config from this file (default: detection/config.json)")
    ap.add_argument("--save", type=str, default="save/",
                    help="Pass the directory where saves are stored. (default: save/)")
    ap.add_argument("--hide", action='store_true', default=False, help="Hide images if parameter is set")
    ap.add_argument("--refine", type=str, help="Pass a json file to refine model")

    args = ap.parse_args()
    with open(args.config, 'r') as file:
        config = json.load(file)

    if args.refine is not None:
        with open(args.refine, 'r') as file:
            refine = json.load(file)
    else:
        refine = None

    orig, blob_mask, blob, food_mask, food_img = detect(args.input, config)
    dsc_img, dsc_blob, dsc_food_list = discretize(blob, food_mask, config['Discrete Width'], config['Discrete Height'])

    if args.save is not None:
        filename = splitext(basename(args.input))[0] + "-detect"
        file_path = join(args.save, filename)

        board, player, img = simulate(dsc_img, dsc_blob, dsc_food_list, config, refine)
        save(file_path, board, player, img)

        # Prepare file_path for details if any to save
        file_path += "-details"
    else:
        file_path = None

    labels = ["Original", "Discrete", "Blob Mask", "Blob", "Food Mask", "Food Regions"]
    images = [orig, img, blob_mask, blob, food_mask, food_img]
    print_results(labels, images, args.scale, file_path, args.hide, nbr_width=2)


if __name__ == "__main__":
    main()
