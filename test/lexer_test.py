#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# lexer_test.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module tests the AML lexer.
#
# Usage: 
# $ python3 -m unittest -v lexer_test.py
# -----------------------------------------------------------------------------

import sys
import enum
import unittest

sys.path.insert(0,"../aml/")
import lexer.lexer as lexer


class TestLexer(unittest.TestCase):
    """
    Tests for the AML lexer.
    """
    
    @enum.unique 
    class TestEnum(enum.Enum):
        ENUM0 = 'enum0'
        ENUM1 = 'enum1'
        ENUM2 = 'enum2'
        ENUM3 = 'enum3'
        ENUM4 = 'enum4'
    
        @classmethod
        def tokens(cls):
            return lexer._tokens(cls)


    def setUp(self):
        """
        Sets up the test.
        """        
        # Builds the expected structures
        self.tokens = []
        for e in self.TestEnum:
            # Builds tokens
            self.tokens.append(e.name)
        
    def tearDown(self):
        """
        Tears down the test.
        """
        del self.tokens[:]

    def test_method__tokens(self):
        """
        Tests the method _tokens()
        """
        self.assertListEqual(self.TestEnum.tokens(), self.tokens)

