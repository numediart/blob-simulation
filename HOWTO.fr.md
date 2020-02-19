# Utilisation
Le dossier "blob-simulation" contient quatre scripts Python qui sont autant de points d'entrées à différents moments du processus.

+ `setup.py` permet de configurer le setup entre la reconnaissance dans l'image et certains paramètres de la simulation. Il n'est à utiliser qu'une fois au moment de la configuration.
+ `detect.py` réalise la reconnaissance d'images, calcule la taille du blob et virtualise celui-ci. Il est possible de raffiner cette détection avec des données json supplémentaires.
+ `play.py` permet de lancer une simulation (automatique ou manuelle) du blob virtualisé
+ `compare.py` utilise deux sauvegardes de simulation pour générer une image représentant les différences entre les deux simulations.

Dans le dossier "data", un fichier "example.jpg" permet d'effectuer un test allant du premier au dernier script.

## Setup (setup.py)

**Commande rapide** : `python setup.py data/example.jpg`

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

Une fois lancé, le programme affiche un menu avec différentes options. Celles-ci sont à entrer dans la console :

+ **1** : permet de cliquer sur l’image pour définir les 4 coins du plateau (de préférence en commençant par celui en haut à gauche et en tournant dans le sens horloger). Lorsque les 4 coins ont été définis, appuyez sur ENTER pour valider ou sur un autre bouton pour recommencer.
+ **2** : permet de cliquer sur des échantillons de pixels représentant la couleur de la nourriture. A chaque click, les pixels désormais pris en compte s’affichent en rouge. A éviter : ne pas cliquer sur de la nourriture recouverte par du blob, ce serait alors ce dernier qui serait repéré dans la suite… Dans le cas d’une erreur, il est possible de retirer le dernier pixel ajouté en appuyant sur BACKSPACE. Lorsque suffisamment d’échantillons ont été sélectionnés, appuyez sur ENTER.
+ **3** : dans la console, vous pouvez entrer le ratio d’image à utiliser pour la détection et l’affichage. C’est un rapport « longueur / hauteur ». Il peut être différent de la résolution utilisée pour la virtualisation.
+ **4** : dans la console, vous pouvez entrer la résolution discrète de la hauteur et de la largeur du blob virtuel.
+ **5** : permet de cliquer sur les 4 coins d’un comprimé de nourriture afin d’en définir la plus petite taille possible. Il est donc plus intéressant de prendre un des plus petits comprimés et de tracer un carré plutôt inscrit à l’intérieur du comprimé.
+ **S** : pour sauver et quitter
+ **Q** : pour quitter sans sauver

*N.B. Lors de l'enregistrement, s'il existait un précédent fichier, celui-ci est archivé dans le dossier "bkp"*

## Détection (detect.py)

**Commande rapide** : python detect.py data/example.jpg

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

Une fois lancé, le programme réalise tout en une seule fois. Lorsque l’image s’affiche, appuyer sur n’importe quelle touche pour fermer le programme.
L’image affiche :

+ **En haut à gauche** : l’image d’origine ainsi qu’un trait correspondant au milieu de l’image (utilisé comme démarcation entre le plateau du haut et le plateau du bas)
+ **En haut à droite** : l’image virtualisée du blob (telle qu’elle sera utilisée dans la simulation)
+ **Au milieu à gauche** : les pixels détectés appartenant au blob
+ **Au milieu à droite** : ces mêmes pixels avec les couleurs d’origine
+ **En bas à gauche** : les pixels détectés appartenant à de la nourriture
+ **En bas à droite** : les agrégats de pixels, correspondant chacun à une nourriture. 

Dans l’image virtualisée, les carrés verts correspondent à de la nourriture. Une croix les recouvre lorsque le blob les a découvertes. Les nuances de gris correspondent à la présence de blob (de noir à blanc selon la quantité de blob supposée).

Dans la console, la quantité de blob sur la totalité, la moitié supérieure et la moitié inférieure du plateau est affichée. Le nombre de nourritures trouvées est également donné.

## Simulation (play.py)
**Commande rapide** : python play.py save/example-detect.board

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

Les couleurs dépendent du fichier "default/interface.json" mais il existe différents types de cases identifiables :

+ Les cases de nourriture non-découvertes par le blob sont de la couleur "FOOD_COLOR".
+ Les cases explorées par le blob sont soit de la couleur "TOUCHED_COLOR" si le blob s'en est retiré, soit entre "BLOB_LOWER_COLOR" et "BLOB_HIGHER_COLOR" selon la quantité de blob présente.
+ Les cases barrées par une croix sont des cases où de la nourriture est présente et connue du blob.
+ Les cases blanches correspondent aux actuateurs (ou "fourmis") du blob. Ce sont elles qui déposent une nouvelle quantité de blob sur une case.

En mode automatique, le programme démarre la simulation et se termine à l'issue du nombre de boucles renseignées en sauvegardant l'état du jeu ainsi qu'un fichier de résultats. Si l'utilisateur effectue une interaction avec le dispositif, le mode automatique s'interrompt pour repasser en mode manuel.

En mode manuel, différentes commandes sont disponibles.

### Commandes de la simulation

#### Commandes d'administration

+ **D** : Passage du mode normal au mode debug et inversement
+ **Flèche du haut / du bas** : Augmente / Diminue l'évaporation du blob sur toutes les cases
+ **ESPACE** : Montre / Cache les actuateurs (ou fourmis)
+ **S** : Sauvegarde l'état actuel du jeu

#### Commandes modifiées en mode debug

+ **Click droit** : Ajoute une petite quantité de blob sur cette case

#### Commandes du joueur

+ **Click droit** : Ajoute de la nourriture sur cette case (et les adjacentes selon la taille de nourriture enregistrée)
+ **C** : Nettoie le plus vieux des deux demi-plateaux
+ **R** : Dépose aléatoirement de la nourriture sur le demi-plateau le plus récent.
+ **H** : Affiche l'information sur la taille du blob
+ **ESCAPE** : Quitte le jeu, sans sauvegarder

#### Commandes de contrôle du blob

+ **P** : Démarre / Arrête la progression du blob
+ **RETOUR** : Effectue un seul pas de progression pour le blob
+ **K** : Diminue le nombre minimum d'actuateurs (fourmis) que doit avoir le blob
+ **A** : Augmente le nombre minimum d'actuateurs (fourmis) que doit avoir le blob

### Logique du blob (dossier simulation/logic)
Le comportement du blob est configurable de différentes manières grâce au fichier "default/blob.json".

La classe *BlobManager* prend en charge la gestion complète du blob. Celui-ci se comporte comme une colonie de fourmis, avec un nombre maximum de fourmis à disposition, chacune d'entre elles se déplaçant sur le plateau selon une certaine logique et déposant une certaine quantité de "blob" sur les cases où elles se trouvent. Elles disposent toutes d'un savoir partagé, contenu dans la variable "knowledge". Cette variable contient, entre autres, la logique à adopter et tous les emplacements de nourriture connus.

Pour calculer la taille maximale de la colonie, différentes propriétés du blob sont utilisées avec certains facteurs d'ajustement :

+ "Blob Size Factor" ajuste la taille de la colonie selon la quantité de blob présent sur le plateau.
+ "Covering Factor" ajuste la taille de la colonie selon la portion de plateau couverte par le blob (indépendamment de la quantité de blob sur chaque case).
+ "Known Foods Factor" modifie la taille de la colonie selon la quantité d'emplacements de nourriture connus.
+ "Global Factor" multiplie chaque facteur afin de notamment s'adapter à la taille du plateau.

Quelques autres variables sont encore utilisées dans cette classe :

+ "Global Decrease" représente la quantité de blob retirée sur chaque case après chaque tour, un tour étant équivalent à un déplacement pour chaque fourmi de la colonie.
+ "Remaining Blob on Food" contrecarre cette décroissance en imposant une limite minimum de blob restant lorsqu'il est sur une case de nourriture
+ "Scouters"->"Min" indique, quant à lui, la taille minimale de la colonie à respecter.

Chaque fourmi utilise la classe *FSMAnt*, une classe utilisant une machine FSM permettant de faire passer la fourmi d'une logique d'exploration (*Scouting*) à une logique de récolte (*Gathering* ou *Harvesting*). Chaque fourmi dispose d'une réserve de nourriture, qu'elle utilise au fur et à mesure de ses déplacements, proportionnellement à la quantité de blob déposée. Les variables suivantes sont utilisées :

+ "Harvesting"->"Eat" indique la quantité de nourriture (maximum) que la fourmi mange pour effectuer un déplacement. Elle en consomme moins si elle se déplace sur une case déjà occupée par du blob, proportionnellement à la quantité de blob se trouvant sur la case.
+ "Scouters"->"Drop by eat" indique la quantité de blob déposée par rapport à la quantité de nourriture utilisée.
+ "Harvesting"->"Collect" correspond à la valeur maximale emmagasinée par la fourmi lorsque celle-ci arrive sur une case de nourriture (peu importe la logique dans laquelle elle se trouve)
+ "Harvesting"->"Min" est la valeur minimale à emmagasiner avant de pouvoir sortir d'une logique de récolte vers une logique d'exploration
+ "Harvesting"->"Max" est la valeur maximale qu'une fourmi peut emmagasiner.

Au départ, une fourmi commence avec un stock minimum de nourriture et se trouve dans une logique d'exploration. Lorsqu'elle se retrouve sans réserve, la fourmi devient affamée et passe dans une logique de récolte jusqu'à avoir recouvré la valeur minimale à emmagasinner. Elle repasse alors dans une logique d'exploration.

Chaque logique est représentée par une classe : *Gatherer* et *AdvancedScouter*. Elles utilisent trois même types de variables, configurables indépendamment pour chacune des deux logiques :

+ "Diagonal Moves" autorise ou non des déplacements en diagonal sur le plateau
+ Lorsque "Light Compute" est actif, chaque fourmi ne calcule qu'une fois son trajet jusqu'à son objectif (d'exploration ou d'emplacement de nourriture). Le chemin trouvé est donc utilisé peu importe l'évolution du plateau (notamment d'éventuelles décroissances de blob). Cela permet cependant de diminuer la quantité de calculs effectués à chaque itération.
+ "Sightline" représente l'horizon vu par la fourmi en nombre de cases. La valeur -1 signifie que la fourmi a une vue sur l'ensemble du plateau. Attention cependant, cela ne signifie pas qu'elle connait pour autant l'emplacement de la nourriture en dehors du blob. Seul le fait que la case est inexplorée est utilisé, peu importe que celle-ci contienne de la nourriture ou pas.

Enfin, deux variables spéciales sont utilisées pour l'exploration :

+ Par défaut, une fourmi en exploration cherche à aller sur une des cases dans son horizon contenant le moins de blob. Cependant, à chaque déplacement, il existe une probabilité "Global Explore Probability" (entre 0 et 1 donc) de passer vers une recherche où la fourmi se déplace vers la case ayant le moins de blob dans son horizon. Ce n'est donc pas la quantité sur la case qui est minimisée mais bien la quantité vue sur l'entiereté de l'horizon. Pour repasser dans le premier type d'exploration, une probabilité de valeur 1-"Global Explore Probability" est utilisée.
+ Lorsque "Search Locally on Food" est vraie, lorsqu'une exploratrice trouve de la nourriture, elle repasse et reste automatiquement dans le premier type d'exploration.

Il existe encore deux autres types de logique implémentées mais non-utilisées : *SensingScouter* correspond à une exploratrice avec "Global Explore Probability" valant 0. *DumbScouter* est l'implétation minimale d'une exploratrice, sans connaissance ou logique de récolte.


## Comparaison (compare.py)

**Commande rapide** : python compare.py save/example-detect.board save/example-10_loops.board

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

Une fois lancé, le programme s'exécute en une fois. Si le paramètre "output" a été fourni, le résultat est sauvegardé sans être affiché. Autrement, une fenêtre pygame est ouverte montrant le résultat de la comparaison.

**Légende :**

+ Les nuances de bleu indiquent la présence plus importante de blob dans le premier mais pas le second fichier
+ Les nuances de rouge indiquent, à l'inverse, une présence plus importante de blob dans le second fichier plutôt que dans le premier
+ S'il existe des différences de position dans les nourritures, celles-ci sont affichées en nuances de vert

## Format des fichiers de configuration
### config.json (NON-modifiable)

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

Fichier généré par le script setup.py. A ne pas modifier à la main, le script est prévu pour encoder les différentes valeurs.

### "refine.json" (A créer si besoin)

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

Fichier pouvant servir d'argument optionnel au script detect.py. Il doit contenir les quatre labels mentionnés ci-dessus. "Width" et "Height" correspondent à la résolution utilisée pour renseigner la position des  "Foods". "Clean Top" est un booléen indiquant si le prochain demi-plateau à nettoyer est celui du haut (True) ou celui du bas (False).

### default/blob.json (Modifiable)

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

Fichier permettant d'initialiser les différentes variables du comportement du blob. A modifier à la main en fonction du comportement souhaité. Il est également enregistré lorsqu'une sauvegarde de la simulation est effectuée. Pour utiliser la logique la plus avancée du blob, tous les labels ci-dessus doivent être présents.

### default/interface.json (Modifiable)

	{
		"FOOD_COLOR": [244, 210, 128],
		"TOUCHED_COLOR": [218, 196, 136],
		"BLOB_LOWER_COLOR": [206, 182, 86],
		"BLOB_HIGHER_COLOR": [162, 106, 59],
		"BACKGROUND": [120, 120, 120],
		"BOARD_SEPARATOR": [0, 0, 0]
	}

Fichier contenant les différentes couleurs utilisées pour l'affichage de la simulation. Modifiable à la main.

### default/player.json (Modifiable)

	{
		"clean_top": true,
		"food_size": 5,
		"use_food_circle": true
	}

Fichier enregistrant les variables pour le "joueur". Modifiable à la main. "clean_top" à la même fonction que décrite plus haut. "food_size" correspond à la taille de la nourriture ajoutée par le joueur lorsqu'il clique dans l'interface. "use_food_circle" doit être à vrai pour poser des nourritures circulaires, sinon celles-ci seront en forme de carré.

### .board file (NON-Modifiable)

	300 120
	0,0.0,0.0 0,0.0,0.0 0,100.0,0.0 1,0.0,25.0 ...
	...
	0,0.0,0.0 0,0.0,0.0 0,0.0,0.0 0,0.0,0.0 ...

Fichier enregistré lorsqu'une sauvegarde de simulation est réalisée. A ne pas modifier à la main. Il est accompagné d'un fichier jpeg, d'un fichier player.json et d'un fichier blob.json. Il peut être accompagné d'un fichier results.json si le mode automatique était activé.

La première ligne indique la résolution (largeur hauteur) utilisée par la simulation. Le reste du fichier est utilisé pour représenté l'état du plateau au moment de la sauvegarde. Chaque groupe de trois valeurs est séparé des autres par un espace et les valeurs en elles-mêmes sont séparées par des virgules.

La première valeur indique si le blob a déjà exploré cette case ou non. La seconde valeur indique la quantité de nourriture présente sur cette case (valeur maximale hardcodée à 100) La troisième valeur indique la quantité de blob présent sur cette case (valeur hardcodée entre 0 et 255)

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

Fichier généré après une simulation en mode automatique.

+ "Covering" donne les pourcentages sur les deux demi-plateaux et le plateau complet que le blob a couvert (ou exploré).
+ "From" indique le fichier avec lequel la simulation a été générée.
+ "Init_foods" est présent s'il y a eu un dépôt aléatoire de nourriture au début de la simulation. Il contient alors les positions de celles-ci, dans la résolution de la simulation (autrement dit, la première ligne du fichier board). La taille utilisée est celle enregistrée dans le fichier player.json.
+ "Loops" indique le nombre de boucles effectuées.
+ "To" mentionne le nom des fichiers de sortie.

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

## Mentions légales
Cette publication a été réalisée dans le cadre du projet Interreg de coopération transfrontalière C2L3PLAY, cofinancé par L’Union Européenne. Avec le soutien du Fonds européen de développement régional / Met steun van het Europees Fonds voor Regionale Ontwikkeling

<img src="https://crossborderlivinglabs.eu/wp-content/uploads/2018/02/LogoProjets_GoToS3_C2L3PLAY.png" width="200px"/>
