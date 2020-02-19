# Blob Simulation & Detection
Detection of a blob in an image as well as detection of food tablets. Simulation of a blob in PyGame through a shared knowledge multi-agent system.

A french translation of this document is available [here](README.fr.md).  
Ce document est aussi disponible en français [ici](README.fr.md).

1. [How to use](HOWTO.md)
2. [Requirements](#requirements)
3. [To go further](TOGOFURTHER.md)
4. [Releases](#releases)
5. [License](#license)
6. [Legal notices](#legal-notices)

## How to use
You will find detailed descriptions of the different scripts and configuration files [here](HOWTO.md).

## Requirements
+ [Python 3.6.8](https://www.python.org/downloads/release/python-368/) - [Documentation](https://docs.python.org/3.6/)
+ [Numpy 1.16.4](https://pypi.org/project/numpy/1.16.4/) - BSD License
+ [Pathfinding 0.0.4](https://pypi.org/project/pathfinding/0.0.4/) - MIT License
+ [PyGame 1.9.6](https://pypi.org/project/pygame/1.9.6/) - LGPL License - [Documentation](https://www.pygame.org/docs/)
+ [Imutils 0.5.2](https://pypi.org/project/imutils/0.5.2/) - MIT License
+ [OpenCV Python 4.1.0.25](https://pypi.org/project/opencv-python/4.1.0.25/) - MIT License - [Documentation](https://docs.opencv.org/4.1.0/)

## To go further
You will find some scientific articles and tips related to the development of this project [here](TOGOFURTHER.md).

## Releases
### Release 2.2 - *24/06/2019*
#### Modifications : 
+ Add a *requirements.txt* file with the versions of the modules used
+ Transform "input" argument into positional

#### Scripts : 
+ Setup : `python setup.py data/example.jpg`
+ Detection : `python detect.py data/example.jpg`
+ Simulation : `python play.py data/output-examples/example-detect.board -s 3`
+ Compare : `python compare.py data/output-examples/simulation/10_loops/10_loops.board data/output-examples/simulation/100_loops/100_loops.board -s 3`

### Release 2.1 - *7/06/2019*

#### Modifications : 
+ Move scripts to the root folder
+ Change the name of the files recorded by the detection
+ Automation of the different scripts
+ Add a "hidden" mode of operation
+ Automation of the simulation with new parameters and final save
  + Add parameter to initialize food
  + Add parameter to control how simulation is displayed
+ Standardize parameters between different scripts
+ Ability to refine a detected template with an additional information file
+ Color values in a separate json file
+ Add examples for the scripts

#### Scripts : 
+ Setup : `python setup.py -i data/example.jpg`
+ Detection : `python detect.py -i data/example.jpg`
+ Simulation : `python play.py -i data/output-examples/example-detect.board -s 3`
+ Compare : `python compare.py --first data/output-examples/simulation/10_loops/10_loops.board --second data/output-examples/simulation/100_loops/100_loops.board -s 3`

Here are the outputs : 
![Detection script output](data/output-examples/example-detect-details.jpg?raw=true "Detection script output") 
![Simulation after 100 iterations](data/output-examples/simulation/100_loops/100_loops.jpg?raw=true "Simulation after 100 iterations")
![Comparison script output](data/compare_init_with_100.jpg?raw=true "Comparison script output") 


### Release 2.0 - *27/05/2019*

Switching to this release invalidates the previous backup files because the format has been changed.

#### Modifications :
+ Improved blob logic (ants have a horizon view, explorers have two modes of operation and the blob manages better how many ants it can use)
+ Improved food utilization (the link between detection and virtual is more realistic, the food can run out and it is easier to add or remove food in large quantities)
+ Transform some files to a json format (especially player and blob files)
+ Move a series of variables into configuration files and create "default" configuration files
+ Simplification of the interface color changeover
+ Add a script to compare two backups

The new interface will produce images like this : 

![simulation interface](https://github.com/numediart/blob-simulation/blob/2.0/example/test-run.jpg?raw=true "simulation interface") 

To call comparison script on one example : 
`python compare.py --first example/test.board --second example/test-run.board`

It will display an image like this one : 

![Comparison between two simulations](https://github.com/numediart/blob-simulation/blob/2.0/example/test-compare.jpg?raw=true "Comparison between two simulations") 


### Release 1.1 - *13/05/2019*
Bug fixes, code reorganization into folders and files.
The three executable scripts are now located here : 
+ Setup : `detection/setup.py`
+ Blob detection in a single image : `detection/detect.py`
+ Simulation : `simulation/play.py`

To run the example : 
`python simulation/play.py --save_dir example/ --init_from test`

### Release 1.0 - *02/05/2019*

First version of a simulator as well as detection in an image.

The complete workflow is usable, starting from a first setup, followed by detections and simulations. It still requires manual operations though.

First, call `detection/setup-detection.py`, 
Then `detection/detector.py`, the board file for the simulation is generated in the console, to be replaced in a file if the console has to start a simulation

The file `main.py` can be launched separately or from an example file.
To get the example, please run : 
`python main.py --save_dir example/ --init_from test`

You then should get this simulation :

![Simulation screenshot](https://github.com/numediart/blob-simulation/blob/1.0/example/test.jpg?raw=true.jpg?raw=true "Simulation screenshot") 

### Controls
#### Actions on the blob
+ **P** start an stop simulation
+ **RETURN** next simulation step
+ **K** kill one of the ants
+ **A** add one ant
#### Player actions
+ **Right click** add a food pellet at the clicked location / (Debug mode) add blob at the clicked location
+ **N** clean the board
+ **R** randomly add food pellet
+ **H** display the current size of the blob (percent)
#### Admin actions
+ **D** switch between normal and debug modes
+ **UP** increase blob evaporation
+ **DOWN** decrease blob evaporation
+ **SPACE** show where are the ants
+ **S** save the simulation

## License
Copyright (C) 2019 - UMons

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

## Legal notices
This publication has been produced in the framework of the Interreg cross-border cooperation project C2L3PLAY, co-financed by the European Union.  
With the support of the European Regional Development Fund /  
Avec le soutien du Fonds européen de développement régional /  
Met steun van het Europees Fonds voor Regionale Ontwikkeling

<img src="https://crossborderlivinglabs.eu/wp-content/uploads/2018/02/LogoProjets_GoToS3_C2L3PLAY.png" width="200px"/>
