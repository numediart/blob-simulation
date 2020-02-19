# To go further
## Physarum polycephalum or Blob
Many scientific articles (and popular books) exist on the blob, but these focus on the analysis of its behaviour and its ability to solve certain problems. Most of its problems are related to graphical representations (TSP Problem, Dijkstra, Voronoï diagram, Delaunay triangluation, ...). There are therefore no articles trying to model its behaviour. At the detection level, there is the MatLab code provided by the CNRS.

**Dussutour**, Audrey (2017).*Tout ce que vous avez toujours voulu savoir sur le blob sans avoir jamais oser le demander.* Des Équateurs, Hors collection, 179 pages.

**Tsuda**, Soichiro, **Zauner**, Klaus-Peter and **Gunji**, Yukio-Pegio (2006) *Robot Control: From Silicon Circuitry to Cells.*      Ijspeert, Auke Jan, Masuzawa, Toshimitsu and Kusumoto, Shinji (eds.)      In Biologically Inspired Approaches to Advanced Information Technology, Second International Workshop, BioADIT 2006, Osaka, Japan, January 26-27, 2006, Proceedings.   Springer.  pp. 20-32.

**Whiting** JG, **Jones** J, **Bull** L, **Levin** M, **Adamatzky** A.* Towards a Physarum learning chip*. *Sci Rep*. 2016;6:19948. Published 2016 Feb 3.

**Jones, Jeff, &amp; Andrew Adamatzky.** [Computation of the travelling salesman problem by a shrinking blob](http://www.phychip.eu/wp-content/uploads/2013/03/Computation-of-the-travelling-salesman-problem-by-a-shrinking-blob.pdf) *Natural Computing,* (13), 1, p. 1-16, (2014).</p>
**Shirakawa**, Tomohiro &amp; **Adamatzky**, Andrew &amp; **Gunji**, Yukio-Pegio &amp; **Miyake**, Yoshihiro. (2009). On Simultaneous Construction of Voronoi Diagram and Delaunay Triangulation by. I. J. Bifurcation and Chaos. 19. 3109-3117. 10.1142/S0218127409024682.

## Multi-agent system

In itself, the blob is not a multi-agent system since it consists of only one cell. Nevertheless, most of the problems it can solve are nowadays more easily solved by multi-agent systems.

A known type of multi-agent system is the behaviour of a colony of ants. The link between blob and ants can be found in its various problems. Audrey Dussutour, before concentrating on the blob, was specifying herself in the behavior of ants as well.

NetLogo is a programming language for multi-agent systems, based on Logo (itself based on LISP). The environment is not ultra-modular, but it provides a series of implemented and ready-to-use models. Some of these (listed below) correspond to problems solved by blob or by ACO (Ants Colony Optimization) algorithms.

There is also a pseudo-code to simulate the behavior of a blob through a multi-agent approach.

Wilensky, U. (1999). **NetLogo**. [http://ccl.northwestern.edu/netlogo/](http://ccl.northwestern.edu/netlogo/) Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.</p>

### Models
+ Stonedahl, F. and Wilensky, U. (2008).  [**NetLogo Virus on a Network model**](http://ccl.northwestern.edu/netlogo/models/VirusonaNetwork). Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

+ Wilensky, U. (2005).  [**NetLogo Preferential Attachment model**](http://ccl.northwestern.edu/netlogo/models/PreferentialAttachment). Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

+ Stonedahl, F. and Wilensky, U. (2008). [**NetLogo Diffusion on a Directed Network model**](http://ccl.northwestern.edu/netlogo/models/DiffusiononaDirectedNetwork).  Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

+ Grider, R. and Wilensky, U. (2015). [**NetLogo Paths model**](http://ccl.northwestern.edu/netlogo/models/Paths).  Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL
+ Wilensky, U. (1997).  [**NetLogo Ant Lines model**](http://ccl.northwestern.edu/netlogo/models/AntLines).  Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

[Pseudo-code multi-agents pour simuler un blob](http://www.simulace.info/index.php/Multi-agent_systems) dans NetLogo.

## IA &amp; Optimization Algorithm Problems
Since no database is available to simulate the blob in the specific case of the project, it is necessary to return to algorithmically predicted behaviors.

Classical AI techniques used to solve problems by exploring solution trees are therefore to be preferred. The blob can be seen as a player who must discover resources in an unknown environment as quickly as possible and optimize the connections between these resources. On this second point, it works like an ACO algorithm. For the discovery part, there are also already simulators of ant routes but those found are difficult to modify.

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

## Legal Notice
This publication has been produced in the framework of the Interreg cross-border cooperation project C2L3PLAY, co-financed by the European Union. With the support of the European Regional Development Fund 

<img src="https://crossborderlivinglabs.eu/wp-content/uploads/2018/02/LogoProjets_GoToS3_C2L3PLAY.png" width="200px"/>
