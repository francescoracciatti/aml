[![codecov](https://codecov.io/gh/francescoracciatti/aml/branch/master/graph/badge.svg)](https://codecov.io/gh/francescoracciatti/aml)

# Synopsis
AML stands for Attack Modeling Language. It is a language to model cyber-physical attacks against cyber-physical systems and complex networks.


# Code Example
Let the figure 1 represent the network scenario.

TODO add the figure

We want perform the attack scenario that follows:
* at time 50 s destroy the sensor node 1
* from time 100 inject a fake udp packets toward the node 3 every 10 ms
* from time 100 capture and drop all the udp messages having the source 
port number 2000 passing through the node 4

The AML code is the following:
```aml
scenario {
    from 50 {
        once {    
            destroyNode(1)
        }
    }
    from 100 {
        every 10 ms {
            packet fake
            createPacket(fake, "udp")
            injectPacket(fake, 3, rx, 0, s)
        }

        list targets = [4]
        filter packetfilter = (("layer4.sourcePort" == 2000))
        for nodes in targets {
            for packets matching packetfilter {
                drop(captured)
            }
        }
    }
}
```

# Motivation
Cyber-physical systems and complex networks can be severely compromised by cyber-physical attacks. 
Since addressing all possible attacks is not viable, due to performance and economic reasons, it is fundamental to choose which attacks to address and which countermeasures to adopt. Hence, a quantitative analysis of attack impact is crucial to make an effective choice.

To do this, it is fundamental to have a tool to model attack scenarios against the system under survey, to be run 
afterward by using a dedicated simulator. AML is exactly the modeling tool to achieve this purpose:
* it provides a powerful yet simple high level modeling language,
* it is independent from the underlying simulator (which will perform the simulations).

# Requirements
* Python 3.6+
* PLY 3.9+

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
