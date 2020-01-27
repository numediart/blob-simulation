# Pour aller plus loin
## Physarum polycephalum ou Blob
Beaucoup d'articles scientifiques (et des livres de vulgarisation) existent sur le blob mais ceux-ci se concentrent sur l'analyse de son comportement et sur sa faculté à résoudre certains problèmes. La plupart de ses problèmes sont liés à des représentations sous forme de graphe (TSP Problem, Dijkstra, Voronoï diagram, Delaunay triangluation, ...) Il n'y a donc pas d'articles cherchant à modéliser son comportement. Au niveau détection, il existe le code MatLab fourni par le CNRS.

**Dussutour**, Audrey (2017).*Tout ce que vous avez toujours voulu savoir sur le blob sans avoir jamais oser le demander.* Des Équateurs, Hors collection, 179 pages.

**Tsuda**, Soichiro, **Zauner**, Klaus-Peter and **Gunji**, Yukio-Pegio (2006) *Robot Control: From Silicon Circuitry to Cells.*      Ijspeert, Auke Jan, Masuzawa, Toshimitsu and Kusumoto, Shinji (eds.)      In Biologically Inspired Approaches to Advanced Information Technology, Second International Workshop, BioADIT 2006, Osaka, Japan, January 26-27, 2006, Proceedings.   Springer.  pp. 20-32.

**Whiting** JG, **Jones** J, **Bull** L, **Levin** M, **Adamatzky** A.* Towards a Physarum learning chip*. *Sci Rep*. 2016;6:19948. Published 2016 Feb 3.

**Jones, Jeff, &amp; Andrew Adamatzky.** [Computation of the travelling salesman problem by a shrinking blob](http://www.phychip.eu/wp-content/uploads/2013/03/Computation-of-the-travelling-salesman-problem-by-a-shrinking-blob.pdf) *Natural Computing,* (13), 1, p. 1-16, (2014).</p>
**Shirakawa**, Tomohiro &amp; **Adamatzky**, Andrew &amp; **Gunji**, Yukio-Pegio &amp; **Miyake**, Yoshihiro. (2009). On Simultaneous Construction of Voronoi Diagram and Delaunay Triangulation by. I. J. Bifurcation and Chaos. 19. 3109-3117. 10.1142/S0218127409024682.

## Système multi-agents

En soi, le blob n'est pas un système multi-agents puisqu'il n'est constitué que d'une seule cellule. Néanmoins, la plupart des problèmes qu'il arrive à résoudre sont aujourd'hui plus facilement résolu par des systèmes multi-agents.

Un type connu de système multi-agents est le comportement d'une colonie de fourmis. On retrouve donc le lien entre blob et fourmis à travers ses différents problèmes. Audrey Dussutour, avant de se concentrer sur le blob, se spécifiait dans le comportement des fourmis également.

NetLogo est un langage de programmation pour système multi-agents, basé sur du Logo (lui-même basé sur du LISP). L'environnement n'est pas ultra-modulable mais il fournit une série de modèles implémentés et prêts à l'emploi. Certains de ceux-ci (listés ci-dessous) correspondent aux problèmes résolus par le blob ou par des algorithmes ACO (Ants Colony Optimization).

Il existe également un pseudo-code permettant de simuler le comportement d'un blob à travers une approche multi-agents.

Wilensky, U. (1999). **NetLogo**. [http://ccl.northwestern.edu/netlogo/](http://ccl.northwestern.edu/netlogo/) Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.</p>

### Modèles
+ Stonedahl, F. and Wilensky, U. (2008).  [**NetLogo Virus on a Network model**](http://ccl.northwestern.edu/netlogo/models/VirusonaNetwork). Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

+ Wilensky, U. (2005).  [**NetLogo Preferential Attachment model**](http://ccl.northwestern.edu/netlogo/models/PreferentialAttachment). Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

+ Stonedahl, F. and Wilensky, U. (2008). [**NetLogo Diffusion on a Directed Network model**](http://ccl.northwestern.edu/netlogo/models/DiffusiononaDirectedNetwork).  Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

+ Grider, R. and Wilensky, U. (2015). [**NetLogo Paths model**](http://ccl.northwestern.edu/netlogo/models/Paths).  Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL
+ Wilensky, U. (1997).  [**NetLogo Ant Lines model**](http://ccl.northwestern.edu/netlogo/models/AntLines).  Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

[Pseudo-code multi-agents pour simuler un blob](http://www.simulace.info/index.php/Multi-agent_systems) dans NetLogo.

## IA &amp; Optimization Algorithm Problems
Aucune base de données n'étant disponible pour simuler le blob dans le cas précis du projet, il est nécessaire d'en revenir à des comportements prédits de manière algorithmiques.

Les techniques classiques d'IA utilisées pour résoudre des problèmes par exploration d'arbres de solution sont donc à privilégier. Le blob peut être envisagé comme un joueur devant découvrir au plus vite des ressources dans un environnement inconnu et à optimiser les connexions entre ces ressources. Sur ce second point, il travaille donc comme un algorithme ACO. Pour la partie découverte, il existe également déjà des simulateurs de parcours de fourmis mais ceux trouvés sont difficilement modifiables.

**Russel**, Stuart Jonathan, **Norvig**, Peter (2009). *Artificial Intelligence : A modern approach*. Pearson, 3rd Edition,&nbsp; 1152 pages.

**geoyar**(2013). [*Applying Ant Colony Optimization Algorithms to Solve the Traveling Salesman Problem*](https://www.codeproject.com/articles/644067/applying-ant-colony-optimization-algorithms-to-sol). Code Project.

**Kohout** Peter (2006). [*Genetic and Ant Colony Optimization Algorithms*](https://www.codeproject.com/Articles/5436/Genetic-and-Ant-Colony-Optimization-Algorithms). Code Project.

**Lichtenberg** Malte, **Tittmann** Lucas (2012). [Programmation Project - Ant Simulation](https://github.com/Andarin/Ant-Colony-Simulation-Python). Andarin, Github Code (Python 2, Cython).

**Akavall** (2019). [Ant Colony Optimization Algorithm using Python](https://github.com/Akavall/AntColonyOptimization). Akavall, Github Code (Python 3).

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