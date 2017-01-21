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
    
    def setUp(self):
        """
        Sets up the test.
        """        
        pass
        
    def tearDown(self):
        """
        Tears down the test.
        """

    def test_method_dictionary(self):
        """
        Tests the method _dictionary()
        """
        @enum.unique 
        class TestEnum(enum.Enum):
            ENUM0 = 'enum0'
            ENUM1 = 'enum1'
            ENUM2 = 'enum2'
            ENUM3 = 'enum3'
            ENUM4 = 'enum4'
        
            @classmethod
            def dictionary(cls):
                return keywords._dictionary(cls)

        expected = {
            'ENUM0' : 'enum0',
            'ENUM1' : 'enum1',
            'ENUM2' : 'enum2',
            'ENUM3' : 'enum3',
            'ENUM4' : 'enum4',
        }
        self.assertDictEqual(TestEnum.dictionary(), expected)


if __name__ == '__main__':
    unittest.main()

