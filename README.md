# Synopsis
AML stands for Attack Modeling Language. It is a language to model cyber-physical attacks against cyber-physical systems and complex networks.

# Code Example
TBD

# Motivation
Cyber-physical systems (CPS) and complex networks can be severely compromised by cyber-physical attacks. 
Since addressing all possible attacks is not viable, due to performance and economic reasons, it is fundamental to choose which attacks to address and which countermeasures to adopt. Hence, a quantitative analysis of attack impact is crucial to make an effective choice.

To do so, it is fundamental to have a tool to model attack scenarios against the CPS/Net under survey, to be run afterward by using a dedicated simulator. 

Note that AML is designed to be independent from the underlying simulator.

# Requirements
Python 3.6+

# Installation
### Linux/Unix
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
