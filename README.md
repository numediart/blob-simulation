# Blob Simulation & Detection
Détection d'un blob dans une image ainsi que détection des comprimés de nourriture. Simulation d'un blob dans PyGame à travers un système multi-agents à connaissance partagée.

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

![Interface de simulation](example/test-run.jpg?raw=true "Interface de simulation") 


Pour exécuter le script de comparaison sur un exemple : 
`python compare.py --first example/test.board --second example/test-run.board`

L'image affichée sera la suivante : 

![Comparaison entre deux simulations](example/test-compare.jpg?raw=true "Comparaison entre deux simulations") 


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

Dans l'ordre, exécuter "detection/setup-detection.py", 
Puis exécuter "detection/detector.py", le fichier board pour la simulation est généré dans la console, à replacer dans un fichier si celui-ci doit démarrer une simulation.

Le code "main.py" peut être lancé séparement ou à partir d'un fichier d'exemple.
Pour avoir l'exemple, utiliser la commande : 
`python main.py --save_dir example/ --init_from test`
Vous devriez alors voir apparaître la simulation suivante  : 

![Simulation screenshot](example/test.jpg?raw=true "Test Simulation") 

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