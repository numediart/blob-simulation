# How to use
The "blob-simulation" folder contains four Python scripts that are entry points at different points in the process.

+ `setup.py` is used to configure the setup between the recognition in the image and some parameters of the simulation. It is to be used only once at the time of configuration.
+ `detect.py` performs the image recognition, calculates the size of the blob and virtualizes it. It is possible to refine this detection with additional json data.
+ `play.py` allows to launch a simulation (automatic or manual) of the virtualized blob.
+ `compare.py` uses two simulation saves to generate an image representing the differences between the two simulations.

In the "data" folder, a file "example.jpg" allows to perform a test from the first to the last script.
Setup (setup.py)

## Setup (setup.py)

**Quick command**: `python setup.py data/example.jpg`

	> python setup.py -h
	usage: Setup the config file for blob detection and simulation
		   [-h] [-s SCALE] [-c CONFIG] INPUT

	positional arguments:
	  INPUT                 Uses this input as image for setup

	optional arguments:
	  -h, --help            show this help message and exit
	  -s SCALE, --scale SCALE
				Scales image by this factor (default: x0.25)
	  -c CONFIG, --config CONFIG
				Saves config under this filename (default:
				detection/config.json)

Once started, the program displays a menu with various options. These are to be entered in the console:

+ **1**: allows you to click on the image to define the 4 corners of the board (preferably starting with the top left corner and turning clockwise). When the 4 corners have been defined, press ENTER to validate or another button to start again.
+ **2**: allows you to click on pixel samples representing the colour of the food. With each click, the pixels now taken into account are displayed in red. To avoid: do not click on food covered by blob, it would then be the blob that would be spotted in the following... In the case of an error, it is possible to remove the last pixel added by pressing BACKSPACE. When enough samples have been selected, press ENTER.
+ **3**: in the console, you can enter the image ratio to be used for detection and display. This is a "length/height" ratio. It can be different from the resolution used for virtualization.
+ **4**: in the console, you can enter the discrete resolution of the height and width of the virtual blob.
+ **5**: allows you to click on the 4 corners of a blob to define the smallest possible size. It is therefore more interesting to take one of the smaller tablets and draw a square rather inscribed inside the tablet.
+ **S**: to save and exit
+ **Q**: to leave without saving

*N.B. When saving, if there was a previous file, it is archived in the "bkp" folder.*

## Detection (detect.py)

**Quick command**: python detect.py data/example.jpg

	> python detect.py -h
	usage: Detect a blob and foods in an image. 
		[-h] [-s SCALE] [-c CONFIG]
		[--save SAVE] [--hide]
		[--refine REFINE]
		INPUT

	positional arguments:
	  INPUT                 Uses this input as image for detection

	optional arguments:
	  -h, --help            show this help message and exit
	  -s SCALE, --scale SCALE
				Scales images by this factor (default: x0.1)
	  -c CONFIG, --config CONFIG
				Loads config from this file (default: detection/config.json)
	  --save SAVE           Pass the directory where saves are stored. (default: save/)
	  --hide                Hide images if parameter is set
	  --refine REFINE       Pass a json file to refine model

Once launched, the program does it all at once. When the image is displayed, press any button to close the program. The image displays:

+ **Top left**: the original image and a line corresponding to the middle of the image (used as a demarcation between the top tray and the bottom tray).
+ **Top right**: the virtualized image of the blob (as it will be used in the simulation)
+ **Middle left**: detected pixels belonging to the blob
+ **Middle right**: the same pixels with the original colors
+ **Bottom left**: detected pixels belonging to food
+ **Bottom right**: aggregates of pixels, each corresponding to a food.

In the virtualized image, the green squares correspond to food. A cross covers them when the blob has discovered them. The shades of grey correspond to the presence of blob (from black to white depending on the amount of blob assumed).

In the console, the amount of blob on the whole, upper half and lower half of the tray is displayed. The number of feeds found is also given.

## Simulation (play.py)
**Quick command**: python play.py save/example-detect.board

	> python play.py -h
	usage: play.py [-h] [--height HEIGHT] [--width WIDTH] [-s SCALE] [--save SAVE]
		[--computing_ratio COMPUTING_RATIO] [--auto_loops AUTO_LOOPS]
		[--display DISPLAY] [--init_foods INIT_FOODS]
		[INPUT]

	positional arguments:
	  INPUT                 Initialize game from a save. Overwrite height and
		width parameters. Pass the board filename as input (.board extension)

	optional arguments:
	  -h, --help            show this help message and exit
	  --height HEIGHT       New game board height resolution if no input is
				given(default: 40)
	  --width WIDTH         New game board width resolution if no input is
				given(default: 100)
	  -s SCALE, --scale SCALE
				Scales board resolution by this factor (default: x10)
	  --save SAVE           Pass the directory where saves are stored. (default: save/)
	  --computing_ratio COMPUTING_RATIO
				How many times computing loop is done before drawing GUI
	  --auto_loops AUTO_LOOPS
				Set number of loops needed before saving and closing automatically
	  --display DISPLAY     Set to '1' to display as centered window, 
				'2' to display as centered window with no border, 
				'3' to display as fullscreen, 
				'0' to hide display (only if auto_loops is set correctly)
	  --init_foods INIT_FOODS
				Starts the game by initializing a certain quantity of
				foods in one of the half-board

The colors depend on the file "default/interface.json" but there are different types of identifiable boxes :

+ The food boxes not discovered by the blob are of the color "FOOD_COLOR".
+ The boxes explored by the blob are either "TOUCHED_COLOR" if the blob has removed itself, or between "BLOB_LOWER_COLOR" and "BLOB_HIGHER_COLOR" depending on the amount of blob present.
+ Crossed out boxes are boxes where food is present and known to the blob.
+ The white boxes are the actuators (or "ants") of the blob. They are the ones that deposit a new amount of blob on a square.

In automatic mode, the program starts the simulation and ends at the end of the number of loops filled in, saving the state of the game and a results file. If the user interacts with the device, the automatic mode is interrupted to return to manual mode.

In manual mode, different commands are available.

### Commands of the simulation

#### Administration commands

+ **D**: Switch from normal mode to debug mode and vice versa
+ **Up / Down Arrow**: Increases / Decreases blob evaporation on all squares
+ **SPACE**: Show / Hide actuators (or ants)
+ **S**: Saves the current state of the game

#### Changed commands in debug mode

+ **Right click** : Adds a small amount of blob to this box

#### Player Controls

+ **Right click**: Adds food on this square (and the adjacent ones according to the recorded food size)
+ **C**: Cleans the older of the two half-trays
+ **A**: Randomly place food on the most recent half tray.
+ **H**: Displays blob size information
+ **ESCAPE**: Quits the game, without saving

#### Blob control commands

+ **P**: Starts / Stops blob progress
+ **RETURN**: Makes a single step forward for the blob
+ **K**: Decreases the minimum number of actuators (ants) that the blob must have.
+ **A**: Increases the minimum number of actuators (ants) the blob must have

### Blob logic (simulation/logic folder)
The behavior of the blob is configurable in different ways using the "default/blob.json" file.

The *BlobManager* class takes care of the complete management of the blob. It behaves like a colony of ants, with a maximum number of ants available, each of them moving around the board according to a certain logic and depositing a certain amount of "blob" on the squares where they are. They all have a shared knowledge, contained in the variable "knowledge". This variable contains, among other things, the logic to be adopted and all known food locations.

To calculate the maximum size of the colony, different properties of the blob are used with certain adjustment factors:

+ "Blob Size Factor" adjusts the colony size according to the amount of blob present on the tray.
+ "Covering Factor" adjusts the colony size according to the portion of the tray covered by the blob (regardless of the amount of blob in each square).
+ "Known Foods Factor adjusts the colony size based on the amount of known food locations.
+ "Global Factor" multiplies each factor to, among other things, adjust for tray size.

Some other variables are still used in this class:

+ "Global Decrease" represents the amount of blob removed from each square after each turn, one turn being equivalent to one move for each ant in the colony.
+ "Remaining Blob on Food" counters this decay by imposing a minimum limit on the amount of blob remaining when on a food square.
+ "Scouters"->"Min" indicates the minimum size of the colony to be respected.

Each ant uses the *FSMAnt* class, a class that uses an FSM machine to switch the ant from a scouting logic (*Scouting*) to a harvesting logic (*Gathering* or *Harvesting*). Each ant has a reserve of food, which it uses as it moves, in proportion to the amount of blob deposited. The following variables are used:

+ "Harvesting"->"Eat" indicates the amount of food (maximum) the ant eats to make a move. It consumes less if it moves to a square already occupied by blob, in proportion to the amount of blob on the square.
+ "Scouters"->"Drop by eat" indicates the amount of blob deposited in relation to the amount of food used.
+ "Harvesting"->"Collect" corresponds to the maximum value stored by the ant when it arrives on a food square (regardless of the logic in which it is located)
+ "Harvesting"->"Min" is the minimum value to be stored before being able to exit from a harvesting logic to an exploration logic.
+ "Harvesting"->"Max" is the maximum value an ant can store.

Initially, an ant starts with a minimum stock of food and is in a logic of exploration. When it is without reserves, the ant becomes hungry and goes into a harvesting logic until it has recovered the minimum value to be stored. It then returns to a logic of exploration.

Each logic is represented by a class: *Gatherer* and *AdvancedScouter*. They use three same types of variables, independently configurable for each of the two logics :

+ "Diagonal Moves" authorizes or not diagonal movements on the board
+ When "Light Compute" is active, each ant only calculates its route to its objective (exploration or feeding location) once. The path found is therefore used regardless of the evolution of the plateau (including possible blob decreases). However, this reduces the amount of calculations performed at each iteration.
+ "Sightline" represents the horizon seen by the ant in number of cells. The value -1 means that the ant has a view of the whole board. However, this does not mean that the ant knows the location of the food outside the blob. Only the fact that the square is unexplored is used, regardless of whether it contains food or not.

Finally, two special variables are used for exploration:

+ By default, an ant in exploration tries to go to one of the squares in its horizon containing the least blob. However, with each move, there is a "Global Explore Probability" (between 0 and 1 therefore) to move to a search where the ant moves to the square with the least blob in its horizon. So it is not the quantity on the box that is minimized but the quantity seen on the whole horizon. To go back to the first type of exploration, a probability of value 1-"Global Explore Probability" is used.
+ When "Search Locally on Food" is true, when an explorer finds food, she automatically returns to the first type of exploration.

There are two other types of logic implemented but not used: *SensingScouter* corresponds to an explorer with "Global Explore Probability" set to 0. *DumbScouter* is the minimal implementation of an explorer with no knowledge or harvesting logic.


## Comparison (compare.py)

**Quick command**: python compare.py save/example-detect.board save/example-10_loops.board

	> python compare.py -h
	usage: compare.py [-h] [-s SCALE] [-o OUTPUT] FIRST_INPUT SECOND_INPUT

	Compare two board files and express it as an image.

	positional arguments:
	  FIRST_INPUT           first board file
	  SECOND_INPUT          second board file to compare with

	optional arguments:
	  -h, --help            Show this help message and exit
	  -s SCALE, --scale SCALE
				Scales board resolution by this factor (default: x10)
	  -o OUTPUT, --output OUTPUT
				Give a name to save the jpeg file
				
Once started, the program runs in one go. If the parameter "output" has been provided, the result is saved without being displayed. Otherwise, a pygame window is opened showing the result of the comparison.

**Legend:**

+ Shades of blue indicate more blob in the first file but not in the second file.
+ The shades of red indicate, conversely, a greater presence of blob in the second file rather than in the first file.
+ If there are differences in the position of the foods, these are displayed in shades of green.

## Configuration file format
### config.json (NOT editable)


	{
		"Aspect Ratio": 0.4,
		"Discrete Height": 160,
		"Discrete Width": 400,

		"Limits": [
			[136, 268],
			[5484, 208],
			[5452, 3296],
			[136, 3308]
		],
		"Low Food Color": [150, 185, 198],
		"High Food Color": [214, 230, 237],
		"Min Food Size": 60
	}

File generated by the setup.py script. Not to be modified by hand, the script is designed to encode the different values.

### "refine.json" (To be created if needed)

	{
		"Width": 100,
		"Height": 40,
		"Foods": [
			[10, 10],
			[18,28],
			[23, 8],
			[44,23],
			[96,22]
		],
		"Clean Top": false
	}

File that can be used as an optional argument to the detect.py script. It must contain the four labels mentioned above. "Width" and "Height" correspond to the resolution used to inform the position of the "Foods". "Clean Top" is a boolean indicating whether the next half tray to be cleaned is the top one (True) or the bottom one (False).

### default/blob.json (Editable)

	{
		"Computing": {
			"Blob Size Factor": 0.25,
			"Covering Factor": 0.75,
			"Global Factor": 2.78,
			"Known Foods Factor": 0.05
		},
		"Gathering": {
			"Diagonal Moves": true,
			"Light Compute": true,
			"Sightline": -1
		},
		"Global Decrease": 0.1,
		"Harvesting": {
			"Collect": 10,
			"Eat": 5,
			"Max": 30,
			"Min": 30
		},
		"Remaining Blob on Food": 50,
		"Scouters": {
			"Drop by eat": 25,
			"Min": 2
		},
		"Scouting": {
			"Diagonal Moves": true,
			"Global Explore Probability": 0.02,
			"Light Compute": true,
			"Search Locally on Food": true,
			"Sightline": 3
		}
	}

File allowing to initialize the different variables of the blob behavior. To be modified manually according to the desired behavior. It is also saved when the simulation is saved. To use the most advanced logic of the blob, all the above labels must be present.

### default/interface.json (Editable)

	{
		"FOOD_COLOR": [244, 210, 128],
		"TOUCHED_COLOR": [218, 196, 136],
		"BLOB_LOWER_COLOR": [206, 182, 86],
		"BLOB_HIGHER_COLOR": [162, 106, 59],
		"BACKGROUND": [120, 120, 120],
		"BOARD_SEPARATOR": [0, 0, 0]
	}

File containing the different colors used to display the simulation. Can be modified by hand.

### default/player.json (Editable)

	{
		"clean_top": true,
		"food_size": 5,
		"use_food_circle": true
	}

File recording the variables for the "player". Can be modified by hand. "clean_top" to the same function as described above. "food_size" is the size of the food added by the player when he clicks in the interface. "use_food_circle" must be true to put circular food, otherwise it will be square-shaped.

### .board file (NON Editable)

	300 120
	0,0.0,0.0 0,0.0,0.0 0,100.0,0.0 1,0.0,25.0 ...
	...
	0,0.0,0.0 0,0.0,0.0 0,0.0,0.0 0,0.0,0.0 ...

File saved when a simulation backup is made. Not to be modified by hand. It is accompanied by a jpeg file, a player.json file and a blob.json file. It can be accompanied by a results.json file if the automatic mode was activated.

The first line indicates the resolution (width height) used by the simulation. The rest of the file is used to represent the state of the board at the time of saving. Each group of three values is separated from the others by a space and the values themselves are separated by commas.

The first value indicates whether the blob has already explored this box or not. The second value indicates the amount of food present on this box (maximum value hardcoded to 100) The third value indicates the amount of blob present on this box (hardcoded value between 0 and 255).

### .results.json

	{
		"Covering": {
			"Bottom": 34.56,
			"Top": 10.09,
			"Total": 22.33
		},
		"From": "save/example-detect",
		"Init_foods": [
			[183, 56],
		],
		"Loops": 10,
		"To": "save/output"
	}
	
File generated after a simulation in automatic mode.

+ "Covering" gives the percentages on the two half trays and the full tray that the blob has covered (or explored).
+ "From" indicates the file with which the simulation was generated.
+ "Init_foods" is present if there was a random deposit of food at the beginning of the simulation. It then contains the positions of these in the resolution of the simulation (i.e. the first line of the board file). The size used is the one saved in the player.json file.
+ "Loops" indicates the number of loops performed.
+ "To" mentions the name of the output files.

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

## Legal Notice
This publication has been produced in the framework of the Interreg cross-border cooperation project C2L3PLAY, co-financed by the European Union. With the support of the European Regional Development Fund 

<img src="https://crossborderlivinglabs.eu/wp-content/uploads/2018/02/LogoProjets_GoToS3_C2L3PLAY.png" width="200px"/>
