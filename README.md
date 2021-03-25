# PyQt5-tr2-Project
The Pyqt5-tr2 project adds a GUI (graphical user interface) as well as a series of other functionalities to tr2 - a Python implementation of an algorithm to find a best position of nodes which define species group under a given guide tree. . To know more about it, please visit [link] https://tfujisawa@bitbucket.org/tfujisawa/tr2-delimitation-python3.git/).


As the algorithm is reasonably fast, you can search the best delimitation through a tree from each tip is distinct species to all tips are from one single species. Acceptable size of the number of taxa on guide tree is around 100. If you exceed 200 taxa, the memory requirement usually becomes huge and normal desktop computers can not handle. The current limitation of the number of input trees, that is, the limit of number of loci, is ~ 1000. Theoretically, it can be larger, but a problem on numerical calculation now limits the number of loci you can use. To run tr2 with a guide tree, you need a newick formatted guide tree file, and a gene tree file also in newick format. Only the first line of the guide tree file is used. In the standard analysis, guide tree tips must contain all taxa found in gene trees. Guide trees can be built any methods such as concatenated ML (eg. RAxML) or coalescent-based species tree methods (eg. ASTRAL). Most importantly, it must be properly rooted. Incorrect rooting often results in over-splitting. The gene tree file must contain one tree per line. They must be rooted too. Missing taxa are allowed.

Pyqt5-tr2 furthermore implements the output of results in the .spart format, developed to provide a uniform and standardized format for species partition results.


# Features

* Spart format export option


# How to use it

* To open it as the original commandline tool; please type python run_tr2.py and follow along the instructions.

* To use it as GUI tool; Please type python tr2f.py on your terminal and follow the instructions.  

