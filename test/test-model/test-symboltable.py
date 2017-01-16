#!/usr/bin/env python3

import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,"../../adl/")
from model.support import SymbolTable
from model.types import SymbolTypes


class TestSymbolTable(unittest.TestCase):
    """
    Tests for the ADL SymbolTable.
    """
    
    def setUp(self):
        """
        Sets up a symbol table.
        """        
        # Makes the SymbolTable not verbose
        SymbolTable.verbose = False
        # Builds a symbol table 
        self.symboltable = SymbolTable(0)
        self.assertTrue(self.symboltable.empty())

    def tearDown(self):
        """
        Tears down the test class.
        """
        self.symboltable.clear()
        self.assertTrue(self.symboltable.empty())

    @patch('model.types.Variable')
    @patch('model.types.Packet')
    @patch('model.types.Filter')
    @patch('model.types.List')
    def test_declare(self, mock_variable, mock_packet, mock_filter, mock_list):
        """
        Tests the method *SymbolTable::declare*
        """
        # Tries to declare undefinible objects
        self.assertRaises(ValueError, self.symboltable.declare, None, SymbolTypes.VARIABLE)
        self.assertRaises(ValueError, self.symboltable.declare, '', SymbolTypes.VARIABLE)
        self.assertRaises(ValueError, self.symboltable.declare, 'obj', None)
        self.assertRaises(TypeError, self.symboltable.declare, 'obj', 'QWERTY')
        self.assertFalse(self.symboltable.exist(None))
        self.assertFalse(self.symboltable.exist(''))
        self.assertFalse(self.symboltable.exist('obj'))
        # Tests double declaration objects
        self.assertTrue(self.symboltable.declare('var', SymbolTypes.VARIABLE))
        self.assertFalse(self.symboltable.declare('var', SymbolTypes.VARIABLE))
        self.assertTrue(self.symboltable.declare('pkt', SymbolTypes.PACKET))
        self.assertFalse(self.symboltable.declare('pkt', SymbolTypes.PACKET))
        self.assertTrue(self.symboltable.declare('flt', SymbolTypes.FILTER))
        self.assertFalse(self.symboltable.declare('flt', SymbolTypes.FILTER))
        self.assertTrue(self.symboltable.declare('lst', SymbolTypes.LIST))
        self.assertFalse(self.symboltable.declare('lst', SymbolTypes.LIST))
        # Checks the existance of the declared objects
        self.assertTrue(self.symboltable.exist('var'))
        self.assertEqual(self.symboltable.type('var'), SymbolTypes.VARIABLE)
        self.assertIsNotNone(self.symboltable.object('var'))
        self.assertTrue(self.symboltable.exist('pkt'))
        self.assertEqual(self.symboltable.type('pkt'), SymbolTypes.PACKET)
        self.assertIsNotNone(self.symboltable.object('pkt'))
        self.assertTrue(self.symboltable.exist('flt'))
        self.assertEqual(self.symboltable.type('flt'), SymbolTypes.FILTER)
        self.assertIsNotNone(self.symboltable.object('flt'))
        self.assertTrue(self.symboltable.exist('lst'))
        self.assertEqual(self.symboltable.type('lst'), SymbolTypes.LIST)
        self.assertIsNotNone(self.symboltable.object('lst'))

    @patch('model.types.Variable')
    @patch('model.types.Packet')
    @patch('model.types.Filter')
    @patch('model.types.List')
    def test_define(self, mock_variable, mock_packet, mock_filter, mock_list):
        """
        Tests the method *SymbolTable::define*
        """
        # Tries to define undefinible objects
        with patch.dict(mock_variable.__dict__, {'identifier': None, 'type' : SymbolTypes.VARIABLE}, clear=False):
            self.assertRaises(ValueError, self.symboltable.define, mock_variable)
        with patch.dict(mock_variable.__dict__, {'identifier': '', 'type' : SymbolTypes.VARIABLE}, clear=False):
            self.assertRaises(ValueError, self.symboltable.define, mock_variable)
        with patch.dict(mock_variable.__dict__, {'identifier': 'obj', 'type' : None}, clear=False):
            self.assertRaises(ValueError, self.symboltable.define, mock_variable)
        with patch.dict(mock_variable.__dict__, {'identifier': 'obj', 'type' : 'QWERTY'}, clear=False):
            self.assertRaises(TypeError, self.symboltable.define, mock_variable)
        self.assertFalse(self.symboltable.exist(None))
        self.assertFalse(self.symboltable.exist(''))
        self.assertFalse(self.symboltable.exist('obj'))
        # Tests double definition
        with patch.dict(mock_variable.__dict__, {'identifier': 'var', 'type' : SymbolTypes.VARIABLE}, clear=False):
            self.assertTrue(self.symboltable.define(mock_variable))
            self.assertFalse(self.symboltable.define(mock_variable))
        with patch.dict(mock_packet.__dict__, {'identifier': 'pkt', 'type' : SymbolTypes.PACKET}, clear=False):
            self.assertTrue(self.symboltable.define(mock_packet))
            self.assertFalse(self.symboltable.define(mock_packet))
        with patch.dict(mock_filter.__dict__, {'identifier': 'flt', 'type' : SymbolTypes.FILTER}, clear=False):
            self.assertTrue(self.symboltable.define(mock_filter))
            self.assertFalse(self.symboltable.define(mock_filter))
        with patch.dict(mock_list.__dict__, {'identifier': 'lst', 'type' : SymbolTypes.LIST}, clear=False):
            self.assertTrue(self.symboltable.define(mock_list))
            self.assertFalse(self.symboltable.define(mock_list))
        # Checks the existance of the defined objects
        self.assertTrue(self.symboltable.exist('var'))
        self.assertEqual(self.symboltable.type('var'), SymbolTypes.VARIABLE)
        self.assertIsNotNone(self.symboltable.object('var'))
        self.assertTrue(self.symboltable.exist('pkt'))
        self.assertEqual(self.symboltable.type('pkt'), SymbolTypes.PACKET)
        self.assertIsNotNone(self.symboltable.object('pkt'))
        self.assertTrue(self.symboltable.exist('flt'))
        self.assertEqual(self.symboltable.type('flt'), SymbolTypes.FILTER)
        self.assertIsNotNone(self.symboltable.object('flt'))
        self.assertTrue(self.symboltable.exist('lst'))
        self.assertEqual(self.symboltable.type('lst'), SymbolTypes.LIST)
        self.assertIsNotNone(self.symboltable.object('lst'))

    @patch('model.types.Variable')
    @patch('model.types.Packet')
    @patch('model.types.Filter')
    @patch('model.types.List')
    def test_object(self, mock_variable, mock_packet, mock_filter, mock_list):
        """
        Tests the method *SymbolTable::object*
        """
        # Tries to get undeclared objects
        self.assertIsNone(self.symboltable.object('var'))
        self.assertIsNone(self.symboltable.object('pkt'))
        self.assertIsNone(self.symboltable.object('flt'))
        self.assertIsNone(self.symboltable.object('lst'))
        # Declare objects
        self.symboltable.declare('var', SymbolTypes.VARIABLE)
        self.symboltable.declare('pkt', SymbolTypes.PACKET)
        self.symboltable.declare('flt', SymbolTypes.FILTER)
        self.symboltable.declare('lst', SymbolTypes.LIST)
        # Gets the declared objects
        self.assertIsNotNone(self.symboltable.object('var'))
        self.assertIsNotNone(self.symboltable.object('pkt'))
        self.assertIsNotNone(self.symboltable.object('flt'))
        self.assertIsNotNone(self.symboltable.object('lst'))

    @patch('model.types.Variable')
    @patch('model.types.Packet')
    @patch('model.types.Filter')
    @patch('model.types.List')
    def test_type(self, mock_variable, mock_packet, mock_filter, mock_list):
        """
        Tests the method *SymbolTable::type*
        """
        # Checks the type of undeclared objects
        self.assertIsNone(self.symboltable.type('var'))
        self.assertIsNone(self.symboltable.type('pkt'))
        self.assertIsNone(self.symboltable.type('flt'))
        self.assertIsNone(self.symboltable.type('lst'))
        # Declares objects
        self.symboltable.declare('var', SymbolTypes.VARIABLE)
        self.symboltable.declare('pkt', SymbolTypes.PACKET)
        self.symboltable.declare('flt', SymbolTypes.FILTER)
        self.symboltable.declare('lst', SymbolTypes.LIST)
        # Checks the type of the declared objects
        self.assertEqual(self.symboltable.type('var'), SymbolTypes.VARIABLE)
        self.assertEqual(self.symboltable.type('pkt'), SymbolTypes.PACKET)
        self.assertEqual(self.symboltable.type('flt'), SymbolTypes.FILTER)
        self.assertEqual(self.symboltable.type('lst'), SymbolTypes.LIST)

    @patch('model.types.Variable')
    @patch('model.types.Packet')
    @patch('model.types.Filter')
    @patch('model.types.List')
    def test_exist(self, mock_variable, mock_packet, mock_filter, mock_list):
        """
        Tests the method *SymbolTable::exist*
        """
        # Checks if undeclared objects exist
        self.assertFalse(self.symboltable.exist('var'))
        self.assertFalse(self.symboltable.exist('pkt'))
        self.assertFalse(self.symboltable.exist('flt'))
        self.assertFalse(self.symboltable.exist('lst'))
        # Declares objects
        self.symboltable.declare('var', SymbolTypes.VARIABLE)
        self.symboltable.declare('pkt', SymbolTypes.PACKET)
        self.symboltable.declare('flt', SymbolTypes.FILTER)
        self.symboltable.declare('lst', SymbolTypes.FILTER)
        # Checks if the declared objects exist
        self.assertTrue(self.symboltable.exist('var'))
        self.assertTrue(self.symboltable.exist('pkt'))
        self.assertTrue(self.symboltable.exist('flt'))
        self.assertTrue(self.symboltable.exist('lst'))
        
    @patch('model.types.Variable')
    @patch('model.types.Packet')
    @patch('model.types.Filter')
    @patch('model.types.List')
    def test_empty(self, mock_variable, mock_packet, mock_filter, mock_list):
        """
        Tests the method *SymbolTable::empty*
        """
        # Checks if the symbol table is empty
        self.assertTrue(not any(self.symboltable.identifier_type_dict))
        self.assertTrue(not any(self.symboltable.identifier_object_dict))
        self.assertTrue(self.symboltable.empty())
        # Declares objects
        self.symboltable.declare('var', SymbolTypes.VARIABLE)
        self.symboltable.declare('pkt', SymbolTypes.PACKET)
        self.symboltable.declare('flt', SymbolTypes.FILTER)
        self.symboltable.declare('lst', SymbolTypes.LIST)
        # Checks if the symbol table is not empty
        self.assertTrue(any(self.symboltable.identifier_type_dict))
        self.assertTrue(any(self.symboltable.identifier_object_dict))
        self.assertFalse(self.symboltable.empty())

    @patch('model.types.Variable')
    @patch('model.types.Packet')
    @patch('model.types.Filter')
    @patch('model.types.List')
    def test_clear(self, mock_variable, mock_packet, mock_filter, mock_list):
        """
        Tests the method *SymbolTable::clear*
        """
        # Declares objects
        self.symboltable.declare('var', SymbolTypes.VARIABLE)
        self.symboltable.declare('pkt', SymbolTypes.PACKET)
        self.symboltable.declare('flt', SymbolTypes.FILTER)
        self.symboltable.declare('lst', SymbolTypes.LIST)
        # Clears the symbol table
        self.symboltable.clear()
        # Checks if the symbol table is empty
        self.assertTrue(self.symboltable.empty())
    
    
if __name__ == '__main__':
    unittest.main()

