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
from detection.detection_setup import setup


def main():

    ap = argparse.ArgumentParser("Setup the config file for blob detection and simulation")
    ap.add_argument("input", metavar="INPUT", help="Uses this input as image for setup")
    ap.add_argument("-s", "--scale", type=float, default=0.25, help="Scales image by this factor (default: x0.25)")
    ap.add_argument("-c", "--config", type=str, default="detection/config.json",
                    help="Saves config under this filename (default: detection/config.json)")

    args = vars(ap.parse_args())
    setup(args['input'], args['config'], args['scale'])


if __name__ == "__main__":
    main()
