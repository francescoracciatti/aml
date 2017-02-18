[![codecov](https://codecov.io/gh/francescoracciatti/aml/branch/master/graph/badge.svg)](https://codecov.io/gh/francescoracciatti/aml)

# Synopsis
AML stands for Attack Modeling Language. It is a language to model cyber-physical attacks against cyber-physical systems and complex networks.

# Code Example
TBD

# Motivation
Cyber-physical systems (CPS) and complex networks can be severely compromised by cyber-physical attacks. 
Since addressing all possible attacks is not viable, due to performance and economic reasons, it is fundamental to choose which attacks to address and which countermeasures to adopt. Hence, a quantitative analysis of attack impact is crucial to make an effective choice.

To do this, it is fundamental to have a tool to model attack scenarios against the CPS/Net under survey, to be run 
afterward by using a dedicated simulator. AML is exactly the modeling tool to achieve this purpose:
* it provides a powerful yet simple high level modeling language,
* it is independent from the underlying simulator (which will perform the simulations).

# Requirements
Python 3.6+

# Installation
### Linux/Unix
TBD

### Windows
TBD

### Mac OS X
TBD

# How To Run It
TBD

# Tests
Change the current working directory to the directory <i>aml/test</t> and type:
```shell
$ python3 -B -m unittest discover -p '*_test.py' -v
```

# API Reference
TBD

# Acknowledgments
* Marco Tiloca
* Alessandro Pischedda
* Gianluca Dini

# License
Copyright © 2016, [Francesco Racciatti](https://github.com/francescoracciatti). 
Released under [MIT license](https://github.com/francescoracciatti/aml/blob/master/LICENSE).
