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

    def test_not_exists(self):
        """
        Test the not existance of a not declared symbol.
        """
        self.assertFalse(self.symboltable.exist('var'))
        
    def test_none_type(self):
        """
        Test the not existance of a not declared symbol.
        """
        self.assertIsNone(self.symboltable.type('var'))

    def test_none_object(self):
        """
        Test the not existance of a not declared symbol.
        """
        self.assertIsNone(self.symboltable.object('var'))

    def test_declare_identifier_none(self):
        """
        Tests the declaration of a symbol with None identifier.
        """
        self.assertRaises(ValueError, self.symboltable.declare, None, SymbolTypes.VARIABLE)

    def test_declare_identifier_empty(self):
        """
        Tests the declaration of a symbol with empty identifier.
        """
        self.assertRaises(ValueError, self.symboltable.declare, '', SymbolTypes.VARIABLE)
    
    def test_declare_type_None(self):
        """
        Tests the declaration of a symbol with None type.
        """
        identifier = 'var'
        self.assertRaises(ValueError, self.symboltable.declare, identifier, None)
    
    def test_declare_type_not_recognized(self):
        """
        Tests the declaration of a symbol with not recognized type.
        """
        identifier = 'var'
        self.assertRaises(TypeError, self.symboltable.declare, identifier, 'QWERTY')

    @patch('model.types.Variable')
    def test_declare_variable(self, mock):
        """
        Tests the declaration of a variable.
        """
        identifier = 'var'
        self.assertTrue(self.symboltable.declare(identifier, SymbolTypes.VARIABLE))
    
    @patch('model.types.Packet')
    def test_declare_packet(self, mock):
        """
        Tests the declaration of a packet.
        """
        identifier = 'pkt'
        self.assertTrue(self.symboltable.declare(identifier, SymbolTypes.PACKET))
    
    @patch('model.types.Filter')
    def test_declare_filter(self, mock):
        """
        Tests the declaration of a filter.
        """
        identifier = 'flt'
        self.assertTrue(self.symboltable.declare(identifier, SymbolTypes.FILTER))
    
    @patch('model.types.List')
    def test_declare_list(self, mock):
        """
        Tests the declaration of a list.
        """
        identifier = 'lst'
        self.assertTrue(self.symboltable.declare(identifier, SymbolTypes.LIST))
        
    @patch('model.types.Variable')
    def test_declare_variable_exist_type_object(self, mock):
        """
        Tests the declaration and the existance of a variable.
        """
        identifier = 'var'
        self.symboltable.declare(identifier, SymbolTypes.VARIABLE)
        self.assertTrue(self.symboltable.exist(identifier))
        self.assertEqual(self.symboltable.type(identifier), SymbolTypes.VARIABLE)
        self.assertIsNotNone(self.symboltable.object(identifier))
    
    @patch('model.types.Packet')
    def test_declare_packet_exist_type_object(self, mock):
        """
        Tests the declaration and the existance of a packet.
        """
        identifier = 'pkt'
        self.symboltable.declare(identifier, SymbolTypes.PACKET)
        self.assertTrue(self.symboltable.exist(identifier))
        self.assertEqual(self.symboltable.type(identifier), SymbolTypes.PACKET)
        self.assertIsNotNone(self.symboltable.object(identifier))
    
    @patch('model.types.Filter')
    def test_declare_filter_exist_type_object(self, mock):
        """
        Tests the declaration and the existance of a filter.
        """
        identifier = 'flt'
        self.symboltable.declare(identifier, SymbolTypes.FILTER)
        self.assertTrue(self.symboltable.exist(identifier))
        self.assertEqual(self.symboltable.type(identifier), SymbolTypes.FILTER)
        self.assertIsNotNone(self.symboltable.object(identifier))
    
    @patch('model.types.List')
    def test_declare_list_exist_type_object(self, mock):
        """
        Tests the declaration and the existance of a list.
        """
        identifier = 'lst'
        self.symboltable.declare(identifier, SymbolTypes.LIST)
        self.assertTrue(self.symboltable.exist(identifier))
        self.assertEqual(self.symboltable.type(identifier), SymbolTypes.LIST)
        self.assertIsNotNone(self.symboltable.object(identifier))

    @patch('model.types.Variable')
    def test_double_declare_variable_error(self, mock):
        """
        Tests the double declaration of a variable.
        """
        identifier = 'var'
        self.symboltable.declare(identifier, SymbolTypes.VARIABLE)
        self.assertFalse(self.symboltable.declare(identifier, SymbolTypes.VARIABLE))
    
    @patch('model.types.Packet')
    def test_double_declare_packet_error(self, mock):
        """
        Tests the double declaration of a packet.
        """
        identifier = 'pkt'
        self.symboltable.declare(identifier, SymbolTypes.PACKET)
        self.assertFalse(self.symboltable.declare(identifier, SymbolTypes.PACKET))
    
    @patch('model.types.Filter')
    def test_double_declare_filter_error(self, mock):
        """
        Tests the double declaration of a filter.
        """
        identifier = 'flt'
        self.symboltable.declare(identifier, SymbolTypes.FILTER)
        self.assertFalse(self.symboltable.declare(identifier, SymbolTypes.FILTER))
    
    @patch('model.types.List')
    def test_double_declare_list_error(self, mock):
        """
        Tests the double declaration of a list.
        """
        identifier = 'lst'
        self.symboltable.declare(identifier, SymbolTypes.LIST)
        self.assertFalse(self.symboltable.declare(identifier, SymbolTypes.LIST))


    @patch('model.types.Variable')
    def test_define_variable_identifier_none(self, mock):
        """
        Tests the definition of a variable having a None identifier.
        """
        with patch.dict(mock.__dict__, {'identifier': None, 'type' : SymbolTypes.VARIABLE}, clear=True):
            self.assertRaises(ValueError, self.symboltable.define, mock)
    
    @patch('model.types.Packet')
    def test_define_packet_identifier_none(self, mock):
        """
        Tests the definition of a packet having a None identifier.
        """
        with patch.dict(mock.__dict__, {'identifier': None, 'type' : SymbolTypes.PACKET}, clear=True):
            self.assertRaises(ValueError, self.symboltable.define, mock)
            
    @patch('model.types.Filter')
    def test_define_filter_identifier_none(self, mock):
        """
        Tests the definition of a filter having a None identifier.
        """
        with patch.dict(mock.__dict__, {'identifier': None, 'type' : SymbolTypes.FILTER}, clear=True):
            self.assertRaises(ValueError, self.symboltable.define, mock)
            
    @patch('model.types.List')
    def test_define_list_identifier_none(self, mock):
        """
        Tests the definition of a variable having a None identifier.
        """
        with patch.dict(mock.__dict__, {'identifier': None, 'type' : SymbolTypes.LIST}, clear=True):
            self.assertRaises(ValueError, self.symboltable.define, mock)

    @patch('model.types.Variable')
    def test_define_variable_identifier_empty(self, mock):
        """
        Tests the definition of a variable having an empty identifier.
        """
        with patch.dict(mock.__dict__, {'identifier': '', 'type' : SymbolTypes.VARIABLE}, clear=True):
            self.assertRaises(ValueError, self.symboltable.define, mock)
    
    @patch('model.types.Packet')
    def test_define_packet_identifier_empty(self, mock):
        """
        Tests the definition of a packet having an empty identifier.
        """
        with patch.dict(mock.__dict__, {'identifier': '', 'type' : SymbolTypes.PACKET}, clear=True):
            self.assertRaises(ValueError, self.symboltable.define, mock)
            
    @patch('model.types.Filter')
    def test_define_filter_identifier_empty(self, mock):
        """
        Tests the definition of a filter having an empty identifier.
        """
        with patch.dict(mock.__dict__, {'identifier': '', 'type' : SymbolTypes.FILTER}, clear=True):
            self.assertRaises(ValueError, self.symboltable.define, mock)
            
    @patch('model.types.List')
    def test_define_list_identifier_empty(self, mock):
        """
        Tests the definition of a list having an empty identifier.
        """
        with patch.dict(mock.__dict__, {'identifier': '', 'type' : SymbolTypes.LIST}, clear=True):
            self.assertRaises(ValueError, self.symboltable.define, mock)

    @patch('model.types.Variable')
    def test_define_variable_type_none(self, mock):
        """
        Tests the definition of a variable having a None type.
        """
        with patch.dict(mock.__dict__, {'identifier': 'var', 'type' : None}, clear=True):
            self.assertRaises(ValueError, self.symboltable.define, mock)
    
    @patch('model.types.Packet')
    def test_define_packet_type_none(self, mock):
        """
        Tests the definition of a packet having a None type.
        """
        with patch.dict(mock.__dict__, {'identifier': 'pkt', 'type' : None}, clear=True):
            self.assertRaises(ValueError, self.symboltable.define, mock)
            
    @patch('model.types.Filter')
    def test_define_filter_type_none(self, mock):
        """
        Tests the definition of a filter having a None type.
        """
        with patch.dict(mock.__dict__, {'identifier': 'flt', 'type' : None}, clear=True):
            self.assertRaises(ValueError, self.symboltable.define, mock)
            
    @patch('model.types.List')
    def test_define_list_type_none(self, mock):
        """
        Tests the definition of a list having a not recognized type.
        """
        with patch.dict(mock.__dict__, {'identifier': 'lst', 'type' : None}, clear=True):
            self.assertRaises(ValueError, self.symboltable.define, mock)

    @patch('model.types.Variable')
    def test_define_variable_type_not_recognized(self, mock):
        """
        Tests the definition of a variable having a not recognized type.
        """
        with patch.dict(mock.__dict__, {'identifier': 'var', 'type' : 'QWERTY'}, clear=True):
            self.assertRaises(TypeError, self.symboltable.define, mock)
    
    @patch('model.types.Packet')
    def test_define_packet_type_not_recognized(self, mock):
        """
        Tests the definition of a packet having a not recognized type.
        """
        with patch.dict(mock.__dict__, {'identifier': 'pkt', 'type' : 'QWERTY'}, clear=True):
            self.assertRaises(TypeError, self.symboltable.define, mock)
            
    @patch('model.types.Filter')
    def test_define_filter_type_not_recognized(self, mock):
        """
        Tests the definition of a filter having a not recognized type.
        """
        with patch.dict(mock.__dict__, {'identifier': 'flt', 'type' : 'QWERTY'}, clear=True):
            self.assertRaises(TypeError, self.symboltable.define, mock)
            
    @patch('model.types.List')
    def test_define_list_type_not_recognized(self, mock):
        """
        Tests the definition of a list having a None type.
        """
        with patch.dict(mock.__dict__, {'identifier': 'lst', 'type' : 'QWERTY'}, clear=True):
            self.assertRaises(TypeError, self.symboltable.define, mock)

    @patch('model.types.Variable')
    def test_define_variable(self, mock):
        """
        Tests the definintion of a variable.
        """
        with patch.dict(mock.__dict__, {'identifier': 'var', 'type' : SymbolTypes.VARIABLE}, clear=True):
            self.assertTrue(self.symboltable.define(mock))
    
    @patch('model.types.Packet')
    def test_define_packet(self, mock):
        """
        Tests the definintion of a packet.
        """
        with patch.dict(mock.__dict__, {'identifier': 'pkt', 'type' : SymbolTypes.PACKET}, clear=True):
            self.assertTrue(self.symboltable.define(mock))
            
    @patch('model.types.Filter')
    def test_define_filter(self, mock):
        """
        Tests the definintion of a filter.
        """
        with patch.dict(mock.__dict__, {'identifier': 'flt', 'type' : SymbolTypes.FILTER}, clear=True):
            self.assertTrue(self.symboltable.define(mock))
            
    @patch('model.types.List')
    def test_define_list(self, mock):
        """
        Tests the definintion of a list.
        """
        with patch.dict(mock.__dict__, {'identifier': 'lst', 'type' : SymbolTypes.LIST}, clear=True):
            self.assertTrue(self.symboltable.define(mock))

    @patch('model.types.Variable')
    def test_define_variable_exist_type_value(self, mock):
        """
        Tests the definintion of a variable and its existance.
        """
        with patch.dict(mock.__dict__, {'identifier': 'var', 'type' : SymbolTypes.VARIABLE}, clear=True):
            self.symboltable.define(mock)
            self.assertTrue(self.symboltable.exist('var'))
            self.assertEqual(self.symboltable.type('var'), SymbolTypes.VARIABLE)
            self.assertIsNotNone(self.symboltable.object('var'))
    
    @patch('model.types.Packet')
    def test_define_packet(self, mock):
        """
        Tests the definintion of a packet and its existance.
        """
        with patch.dict(mock.__dict__, {'identifier': 'pkt', 'type' : SymbolTypes.PACKET}, clear=True):
            self.symboltable.define(mock)
            self.assertTrue(self.symboltable.exist('pkt'))
            self.assertEqual(self.symboltable.type('pkt'), SymbolTypes.PACKET)
            self.assertIsNotNone(self.symboltable.object('pkt'))
            
    @patch('model.types.Filter')
    def test_define_filter(self, mock):
        """
        Tests the definintion of a filter and its existance.
        """
        with patch.dict(mock.__dict__, {'identifier': 'flt', 'type' : SymbolTypes.FILTER}, clear=True):
            self.symboltable.define(mock)
            self.assertTrue(self.symboltable.exist('flt'))
            self.assertEqual(self.symboltable.type('flt'), SymbolTypes.FILTER)
            self.assertIsNotNone(self.symboltable.object('flt'))
            
    @patch('model.types.List')
    def test_define_list(self, mock):
        """
        Tests the definintion of a list and its existance.
        """
        with patch.dict(mock.__dict__, {'identifier': 'lst', 'type' : SymbolTypes.LIST}, clear=True):
            self.symboltable.define(mock)
            self.assertTrue(self.symboltable.exist('lst'))
            self.assertEqual(self.symboltable.type('lst'), SymbolTypes.LIST)
            self.assertIsNotNone(self.symboltable.object('lst'))

    @patch('model.types.Variable')
    def test_double_define_variable(self, mock):
        """
        Tests the double definintion of a variable.
        """
        with patch.dict(mock.__dict__, {'identifier': 'var', 'type' : SymbolTypes.VARIABLE}, clear=True):
            self.symboltable.define(mock)
            self.assertFalse(self.symboltable.define(mock))
    
    @patch('model.types.Packet')
    def test_double_define_packet(self, mock):
        """
        Tests the double definintion of a packet.
        """
        with patch.dict(mock.__dict__, {'identifier': 'pkt', 'type' : SymbolTypes.PACKET}, clear=True):
            self.symboltable.define(mock)
            self.assertFalse(self.symboltable.define(mock))
                        
    @patch('model.types.Filter')
    def test_double_define_filter(self, mock):
        """
        Tests the double definintion of a filter.
        """
        with patch.dict(mock.__dict__, {'identifier': 'flt', 'type' : SymbolTypes.FILTER}, clear=True):
            self.symboltable.define(mock)
            self.assertFalse(self.symboltable.define(mock))
            
    @patch('model.types.List')
    def test_double_define_list(self, mock):
        """
        Tests the double definintion of a list.
        """
        with patch.dict(mock.__dict__, {'identifier': 'lst', 'type' : SymbolTypes.LIST}, clear=True):
            self.symboltable.define(mock)
            self.assertFalse(self.symboltable.define(mock))

    @patch('model.types.Variable')
    @patch('model.types.Packet')
    @patch('model.types.Filter')
    @patch('model.types.List')
    def test_clear(self, mock_variable, mock_packet, mock_filter, mock_list):
        """
        Tests the method *SymbolTable::clear*
        """
        identifier = 'var'
        self.symboltable.declare(identifier, SymbolTypes.VARIABLE)
        identifier = 'pkt'
        self.symboltable.declare(identifier, SymbolTypes.PACKET)
        identifier = 'flt'
        self.symboltable.declare(identifier, SymbolTypes.FILTER)
        identifier = 'lst'    
        self.symboltable.declare(identifier, SymbolTypes.LIST)
        self.symboltable.clear()
        self.assertTrue(self.symboltable.empty())
        self.assertTrue(not any(self.symboltable.identifier_type_dict))
        self.assertTrue(not any(self.symboltable.identifier_object_dict))
        
        
    @patch('model.types.Variable')
    @patch('model.types.Packet')
    @patch('model.types.Filter')
    @patch('model.types.List')
    def test_empty(self, mock_variable, mock_packet, mock_filter, mock_list):
        """
        Tests if an empty symbol table is empty.
        """
        self.assertTrue(not any(self.symboltable.identifier_type_dict))
        self.assertTrue(not any(self.symboltable.identifier_object_dict))
        self.assertTrue(self.symboltable.empty())
        identifier = 'var'
        self.symboltable.declare(identifier, SymbolTypes.VARIABLE)
        identifier = 'pkt'
        self.symboltable.declare(identifier, SymbolTypes.PACKET)
        identifier = 'flt'
        self.symboltable.declare(identifier, SymbolTypes.FILTER)
        identifier = 'lst'    
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
        identifier = 'var'
        self.symboltable.declare(identifier, SymbolTypes.VARIABLE)
        identifier = 'pkt'
        self.symboltable.declare(identifier, SymbolTypes.PACKET)
        identifier = 'flt'
        self.symboltable.declare(identifier, SymbolTypes.FILTER)
        identifier = 'lst'    
        self.symboltable.declare(identifier, SymbolTypes.LIST)
        self.symboltable.clear()
        self.assertTrue(self.symboltable.empty())
    
    
if __name__ == '__main__':
    unittest.main()

