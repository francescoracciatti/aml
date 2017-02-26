[![Build Status](https://travis-ci.org/francescoracciatti/aml.svg?branch=master)](https://travis-ci.org/francescoracciatti/aml)
[![codecov](https://codecov.io/gh/francescoracciatti/aml/branch/master/graph/badge.svg)](https://codecov.io/gh/francescoracciatti/aml)

# AML
AML stands for Attack Modeling Language. It is a language to model cyber-physical attacks against cyber-physical systems and networks.

AML provides:
* a set of keywords and syntax rules to model attack scenarios against generic systems,
* an interpreter that provides the representation of the attack scenarios.
 
## Synopsis
AML is designed to be used on top of the off-the-shelf cyber-physical systems and networks simulators.
Its purpose is to enable the simulation of the effects of the modeled attacks on the systems under survey.

## Motivation
Cyber-physical systems and networks can be severely compromised by cyber-physical attacks. 
Since addressing all possible attacks is not viable, due to performance and economic reasons, it is fundamental to choose which attacks to address and which countermeasures to adopt. Hence, a quantitative analysis of attack impact is crucial to make an effective choice.

To do this, it is fundamental to have a tool to model attack scenarios against the system under survey, to be run 
afterward by using a dedicated simulator. AML is exactly the modeling tool to achieve this purpose.


## Code Example
Let the figure 1 represent the network scenario.

TODO add the figure

When the simulation starts, we want to perform the attack scenario that follows:
* at time 100 s destroy the sensor node 1
* from time 100, every 10 ms, inject a fake udp packets toward the node 3
* from time 100 drop all the messages passing through the node 4 having the source port number 80

The AML code is the following:
```aml
scenario {

    from 100 {

        once {    
            destroyNode(1)
        }
        
        every 10 ms {
            packet fake
            createPacket(fake, "udp")
            injectPacket(fake, 3, rx, 0, s)
        }

        list targets = [4]
        filter packetfilter = (("layer4.sourcePort" == 80))
        for nodes in targets {
            for packets matching packetfilter {
                drop(captured)
            }
        }
    
    }

}
```

## Requirements
* Python 3.6+
* PLY 3.9+

## Installation
### Linux/Unix
TBD

### Windows
TBD

### Mac OS X
TBD

## How To Run It
TBD

## Tests
Change the current working directory to the directory <i>aml/test</t> and type:
```shell
$ python3 -B -m unittest discover -p '*_test.py' -v
```

## API Reference
TBD

## Acknowledgments
* Marco Tiloca
* Alessandro Pischedda
* Gianluca Dini

## License
Copyright © 2016, [Francesco Racciatti](https://github.com/francescoracciatti). 
Released under [MIT license](https://github.com/francescoracciatti/aml/blob/master/LICENSE).
