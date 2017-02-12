#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# testkeywords.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module tests the mechanism for handling ADL types.
#
# Usage: 
# $ python3 -m unittest -v parser_test.py
# -----------------------------------------------------------------------------

import sys
import enum
import unittest

sys.path.insert(0,"../adl/")
import adl as adl

class TestParser(unittest.TestCase):
    """
    Tests for the parser.
    """
    
    def setUp(self):
        """
        Sets up the test.
        """
        self.source = """
            scenario {

                variable var00
                variable var01 = 1
                variable var02 = "layer0.field0"
                variable var03 = 0.3
                packet pkt01
                filter flt01 = ((var02 > var01) && ("layer1.field0" == var01)) || (var02 < var03)
                list lst01 = [var01, 1, "string", 1.2]

                from 200.0 s {}

            }
            """

    def tearDown(self):
        """
        Tears down the test.
        """
        
    def test_parser(self):
        """
        Tests the parser.
        """
        # Parses the source string
        try:
            scenario = adl.ADL.parse(self.source)
        except (ValueError, RuntimeError) as e:
            self.fail(e)
        

if __name__ == '__main__':
    unittest.main()

