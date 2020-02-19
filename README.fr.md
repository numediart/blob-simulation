# Blob Simulation & Detection
Détection d'un blob dans une image ainsi que détection des comprimés de nourriture. Simulation d'un blob dans PyGame à travers un système multi-agents à connaissance partagée.

1. [Utilisation](HOWTO.fr.md)
2. [Logiciels et bibliothèques requis](#logiciels-et-bibliothèques-requis)
3. [Pour aller plus loin](TOGOFURTHER.fr.md)
4. [Releases](#releases)
5. [Licence](#licence)
6. [Mentions légales](#mentions-légales)

## Utilisation
Vous trouverez la description détaille des différents scripts et des fichiers de configuration [ici](HOWTO.md).

## Logiciels et bibliothèques requis
+ [Python 3.6.8](https://www.python.org/downloads/release/python-368/) - [Documentation](https://docs.python.org/3.6/)
+ [Numpy 1.16.4](https://pypi.org/project/numpy/1.16.4/) - BSD License
+ [Pathfinding 0.0.4](https://pypi.org/project/pathfinding/0.0.4/) - MIT License
+ [PyGame 1.9.6](https://pypi.org/project/pygame/1.9.6/) - LGPL License - [Documentation](https://www.pygame.org/docs/)
+ [Imutils 0.5.2](https://pypi.org/project/imutils/0.5.2/) - MIT License
+ [OpenCV Python 4.1.0.25](https://pypi.org/project/opencv-python/4.1.0.25/) - MIT License - [Documentation](https://docs.opencv.org/4.1.0/)

## Pour aller plus loin
Vous trouverez quelques articles scientifiques et conseils de lecture en lien avec le développement de ce projet [ici](TOGOFURTHER.md).

## Releases
## Release 2.2 - *24/06/2019*
### Modifications : 
+ Ajout d'un fichier requirements.txt avec les versions des modules utilisées
+ Transformation de l'argument "input" en argument positionnel

### Scripts : 
+ Setup : `python setup.py data/example.jpg`
+ Detection : `python detect.py data/example.jpg`
+ Simulation : `python play.py data/output-examples/example-detect.board -s 3`
+ Compare : `python compare.py data/output-examples/simulation/10_loops/10_loops.board data/output-examples/simulation/100_loops/100_loops.board -s 3`

## Release 2.1 - *7/06/2019*

### Modifications : 
+ Déplacement des scripts dans le dossier root
+ Changement du nom des fichiers enregistrés par la détection
+ Automatisation des différents scripts, ajout d'un fonctionnement en mode "caché".
+ Automatisation de la simulation avec ajouts de paramètres et sauvegarde finale
+ Ajout d'un paramètre pour initialiser de la nourriture dans la simulation
+ Ajout d'un paramètre d'affichage dans la simulation
+ Uniformisation des paramètres dans les différents scripts
+ Possibilité de raffiner un modèle détecté avec un fichier d'informations supplémentaires
+ Variables de couleur déplacées dans un fichier json séparé
+ Ajout de fichiers d'exemples pour les différents scripts

### Scripts : 
+ Setup : `python setup.py -i data/example.jpg`
+ Detection : `python detect.py -i data/example.jpg`
+ Simulation : `python play.py -i data/output-examples/example-detect.board -s 3`
+ Compare : `python compare.py --first data/output-examples/simulation/10_loops/10_loops.board --second data/output-examples/simulation/100_loops/100_loops.board -s 3`

Les différentes sorties produites sont les suivantes : 
![Sortie du script de détection](data/output-examples/example-detect-details.jpg?raw=true "Sortie du script de détection") 
![Sortie de la simulation après 100 itérations](data/output-examples/simulation/100_loops/100_loops.jpg?raw=true "Sortie de la simulation après 100 itérations")
![Sortie du script de comparaison](data/compare_init_with_100.jpg?raw=true "Sortie du script de comparaison") 


## Release 2.0 - *27/05/2019*

Le passage à cette release invalide les fichiers de sauvegarde précédents, le format ayant été modifié.

### Modifications :
+ Logique du blob améliorée (les fourmis ont un horizon de vue, les exploratrices ont deux modes de fonctionnement et le blob calcule mieux la quantité de fourmis qu’il peut utiliser)
+ Utilisation de la nourriture améliorée (le lien entre détection et virtuel est plus réaliste, la nourriture peut s’épuiser et il est plus facile d’ajouter ou retirer de la nourriture en grande quantité)
+ Transformation d'une série de fichiers vers un format json (notamment les fichiers player et blob)
+ Déplacement d'une série de variables dans des fichiers de configuration et création des fichiers de configuration "par défaut"
+ Simplification du changement de couleurs de l'interface
+ Ajout d'un script de comparaison entre deux sauvegardes

La nouvelle interface de la simulation produira des images comme celle-ci : 

![Interface de simulation](https://github.com/numediart/blob-simulation/blob/2.0/example/test-run.jpg?raw=true "Interface de simulation") 

Pour exécuter le script de comparaison sur un exemple : 
`python compare.py --first example/test.board --second example/test-run.board`

L'image affichée sera la suivante : 

![Comparaison entre deux simulations](https://github.com/numediart/blob-simulation/blob/2.0/example/test-compare.jpg?raw=true "Comparaison entre deux simulations") 


## Release 1.1 - *13/05/2019*
Correction de bugs, réorganisation du code en dossiers et fichiers.
Les trois exécutables se trouvent maintenant ici : 
+ Fichier de setup : `detection/setup.py`
+ Fichier de détection du blob dans une image : `detection/detect.py`
+ Fichier de simulation : `simulation/play.py`

Pour essayer l'exemple, utiliser la commande : 
`python simulation/play.py --save_dir example/ --init_from test`

## Release 1.0 - *02/05/2019*

Première version d'un simulateur ainsi que de la détection dans une image.

Le workflow complet existe en partant d'un premier setup, suivi de détections et de simulations. Il demande encore des opérations manuelles cependant.

Dans l'ordre, exécuter `detection/setup-detection.py`, 
Puis exécuter `detection/detector.py`, le fichier board pour la simulation est généré dans la console, à replacer dans un fichier si celui-ci doit démarrer une simulation.

Le code `main.py` peut être lancé séparement ou à partir d'un fichier d'exemple.
Pour avoir l'exemple, utiliser la commande : 
`python main.py --save_dir example/ --init_from test`
Vous devriez alors voir apparaître la simulation suivante  : 

![Simulation screenshot](https://github.com/numediart/blob-simulation/blob/1.0/example/test.jpg?raw=true.jpg?raw=true "Test Simulation") 

### Commandes
#### Actions sur le blob
+ **P** démarre ou arrête la simulation
+ **RETURN** fait avancer d'un pas la simulation
+ **K** tue une des fourmis
+ **A** ajoute une fourmi
#### Actions du joueur
+ **Clic droit** ajoute un comprimé de nourriture à l'endroit cliqué / (Mode debug) ajoute du blob à l'endroit cliqué
+ **N** nettoie le plateau
+ **R** ajoute aléatoirement des comprimés de nourriture
+ **H** affiche la taille actuelle du blob en pourcentage
#### Actions admin
+ **D** passer en mode debug ou mode normal
+ **UP** augmente l'évaporation du blob
+ **DOWN** diminue l'évaporation du blob
+ **SPACE** montre ou cacher les fourmis
+ **S** sauvegarde la simulation

## Licence
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

*Cette bibliothèque est un logiciel libre ; vous pouvez la redistribuer et/ou
le modifier selon les termes du GNU Lesser General Public
Licence telle que publiée par la Free Software Foundation ; soit
la version 2.1 de la licence, ou (à votre choix) toute version ultérieure.*

*Cette bibliothèque est distribuée dans l'espoir qu'elle vous sera utile,
mais SANS AUCUNE GARANTIE ; sans même la garantie implicite de
la qualité marchande ou l'adéquation à un usage particulier.  Voir le site web de GNU
Lesser General Public License pour plus de détails.*

## Mentions légales
Cette publication a été réalisée dans le cadre du projet Interreg de coopération transfrontalière C2L3PLAY, cofinancé par L’Union Européenne.  
Avec le soutien du Fonds européen de développement régional /  
Met steun van het Europees Fonds voor Regionale Ontwikkeling

<img src="https://crossborderlivinglabs.eu/wp-content/uploads/2018/02/LogoProjets_GoToS3_C2L3PLAY.png" width="200px"/>
