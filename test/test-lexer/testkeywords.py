#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# testkeywords.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module tests the ADL keywords.
# -----------------------------------------------------------------------------

import sys
import enum
import unittest

sys.path.insert(0,"../../adl/")
import lexer.keywords as keywords


class TestKeywords(unittest.TestCase):
    """
    Tests for the ADL keywords.
    """
    
    @enum.unique 
    class TestEnum(enum.Enum):
        ENUM0 = 'enum0'
        ENUM1 = 'enum1'
        ENUM2 = 'enum2'
        ENUM3 = 'enum3'
        ENUM4 = 'enum4'
    
        @classmethod
        def reserved(cls):
            return keywords._reserved(cls)
    
        @classmethod
        def tokens(cls):
            return keywords._tokens(cls)
    
        @classmethod
        def dictionary(cls):
            return keywords._dictionary(cls)
    
    def setUp(self):
        """
        Sets up the test.
        """        
        # Builds the expected structures
        self.reserved = []
        self.tokens = []
        self.dictionary = {}
        for e in self.TestEnum:
            # Builds reserved
            self.reserved.append(e.value)
            # Builds tokens
            self.tokens.append(e.name)
            # Builds dictionary
            self.dictionary[e.value] = e.name
        
        
    def tearDown(self):
        """
        Tears down the test.
        """
        del self.reserved[:]
        del self.tokens[:]
        self.dictionary.clear()


    def test_method__reserved(self):
        """
        Tests the method _reserved()
        """
        self.assertListEqual(self.TestEnum.reserved(), self.reserved)
    
    
    def test_method__tokens(self):
        """
        Tests the method _tokens()
        """
        self.assertListEqual(self.TestEnum.tokens(), self.tokens)


    def test_method__dictionary(self):
        """
        Tests the method _dictionary()
        """
        self.assertDictEqual(self.TestEnum.dictionary(), self.dictionary)


if __name__ == '__main__':
    unittest.main()

