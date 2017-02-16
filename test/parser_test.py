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

import os
import sys
import enum
import unittest

sys.path.insert(0,"../adl/")
import adl as adl

class TestParser(unittest.TestCase):
    """
    Tests for the parser.
    """

    filename = "source.adl"
    
    def setUp(self):
        """
        Sets up the test.
        """
        if not os.path.exists(self.filename):
            self.fail(self.filename + "does not exist")
        if not os.path.isfile(self.filename):
            self.fail(self.filename + "is a directory")
        sourcefile = open(self.filename, 'r')
        self.source = sourcefile.read()
        sourcefile.close()

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
        
