#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# testkeywords.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module tests the ADL keywords.
#
# Usage: 
# $ python3 -m unittest -v testkeywords.py
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
        def keywords(cls):
            return keywords._keywords(cls)
    
        @classmethod
        def tokens(cls):
            return keywords._tokens(cls)
    
        @classmethod
        def view(cls):
            return keywords._view(cls)
            
        @classmethod
        def rview(cls):
            return keywords._rview(cls)
    
    def setUp(self):
        """
        Sets up the test.
        """        
        # Builds the expected structures
        self.keywords = []
        self.tokens = []
        self.view = {}
        self.rview = {}
        for e in self.TestEnum:
            # Builds keywords
            self.keywords.append(e.value)
            # Builds tokens
            self.tokens.append(e.name)
            # Builds view
            self.view[e.name] = e.value
            # Builds rview
            self.rview[e.value] = e.name
        
    def tearDown(self):
        """
        Tears down the test.
        """
        del self.keywords[:]
        del self.tokens[:]
        self.view.clear()
        self.rview.clear()

    def test_method__keywords(self):
        """
        Tests the method _keywords()
        """
        self.assertListEqual(self.TestEnum.keywords(), self.keywords)
    
    def test_method__tokens(self):
        """
        Tests the method _tokens()
        """
        self.assertListEqual(self.TestEnum.tokens(), self.tokens)

    def test_method__view(self):
        """
        Tests the method _view()
        """
        self.assertDictEqual(self.TestEnum.view(), self.view)

    def test_method__view(self):
        """
        Tests the method _rview()
        """
        self.assertDictEqual(self.TestEnum.rview(), self.rview)


if __name__ == '__main__':
    unittest.main()

