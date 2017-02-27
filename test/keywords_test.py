#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# keywords_test.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module tests the AML keywords.
#
# Usage: 
# $ python3 -m unittest -v keywords_test.py
# -----------------------------------------------------------------------------

import sys
import enum
import unittest

sys.path.insert(0,"../aml/")
import lexer.keywords as keywords


class TestKeywords(unittest.TestCase):
    """
    Tests for the AML keywords.
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
        Tests the method _keywords().
        """
        self.assertListEqual(self.TestEnum.keywords(), self.keywords)

    def test_method_keywords(self):
        """
        Test the method keywords().
        """
        test = []
        for e in keywords.Type:
            test.append(e.value)
        for e in keywords.Primitive:
            test.append(e.value)
        for e in keywords.Statement:
            test.append(e.value)
        for e in keywords.Accessor:
            test.append(e.value)
        for e in keywords.WellKnown:
            test.append(e.value)
        self.assertListEqual(keywords.keywords(), test)
    
    def test_method__tokens(self):
        """
        Tests the method _tokens().
        """
        self.assertListEqual(self.TestEnum.tokens(), self.tokens)

    def test_method_tokens(self):
        """
        Tests the method tokens().
        """
        test = []
        for e in keywords.Type:
            test.append(e.name)
        for e in keywords.Primitive:
            test.append(e.name)
        for e in keywords.Statement:
            test.append(e.name)
        for e in keywords.Accessor:
            test.append(e.name)
        for e in keywords.WellKnown:
            test.append(e.name)
        self.assertListEqual(keywords.tokens(), test)

    def test_method__view(self):
        """
        Tests the method _view().
        """
        self.assertDictEqual(self.TestEnum.view(), self.view)
    
    def test_method_view(self):
        """
        Tests the method view().
        """
        test = {}
        for e in keywords.Type:
            test[e.name] = e.value
        for e in keywords.Primitive:
            test[e.name] = e.value
        for e in keywords.Statement:
            test[e.name] = e.value
        for e in keywords.Accessor:
            test[e.name] = e.value
        for e in keywords.WellKnown:
            test[e.name] = e.value
        self.assertDictEqual(keywords.view(), test)

    def test_method__rview(self):
        """
        Tests the method _rview().
        """
        self.assertDictEqual(self.TestEnum.rview(), self.rview)
    
    def test_method_rview(self):
        """
        Tests the method rview().
        """
        test = {}
        for e in keywords.Type:
            test[e.value] = e.name
        for e in keywords.Primitive:
            test[e.value] = e.name
        for e in keywords.Statement:
            test[e.value] = e.name
        for e in keywords.Accessor:
            test[e.value] = e.name
        for e in keywords.WellKnown:
            test[e.value] = e.name
        self.assertDictEqual(keywords.rview(), test)

