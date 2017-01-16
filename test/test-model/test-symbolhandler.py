#!/usr/bin/env python3

import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,"../../adl/")
from model.support import SymbolHandler, SymbolTable
from model.types import SymbolTypes


class TestSymbolHandler(unittest.TestCase):
    """
    Tests for the ADL SymbolHandler.
    """
    
    def setUp(self):
        """
        Sets up a symbol table.
        """        
        # Makes the SymbolHandler and the SymbolTable not verbose
        SymbolHandler.verbose = False
        SymbolTable.verbose = False
        # Builds a symbol handler
        self.symbolhandler = SymbolHandler()
        # Tests empty
        self.assertEqual(len(self.symbolhandler.scope_symboltable_dict), 0)

    def tearDown(self):
        """
        Tears down the test class.
        """
        self.symbolhandler.dump()

    def test_allocate(self):
        """
        Tests the method *SymbolHandler::allocate*.
        """
        # Tests argument check
        self.assertRaises(ValueError, self.symbolhandler.allocate, -1, 0)
        self.assertRaises(ValueError, self.symbolhandler.allocate, 0, -1)
        self.assertRaises(ValueError, self.symbolhandler.allocate, 1, 0)
        scopes = 5    
        self.symbolhandler.allocate(0, scopes - 1)
        self.assertEqual(len(self.symbolhandler.scope_symboltable_dict), scopes)

    def test_dump(self):
        """
        Tests the method *SymbolHandler::dump*.
        """
        # Tests dump with an empty symbol handler
        self.assertEqual(len(self.symbolhandler.scope_symboltable_dict), 0)
        self.symbolhandler.dump()
        self.assertEqual(len(self.symbolhandler.scope_symboltable_dict), 0)
        # Tests dump with a full symbol handler
        scopes = 10
        self.symbolhandler.allocate(0, scopes - 1)
        self.assertEqual(len(self.symbolhandler.scope_symboltable_dict), scopes)
        self.symbolhandler.dump()
        self.assertEqual(len(self.symbolhandler.scope_symboltable_dict), 0)
        
    @patch('model.types.Variable')
    @patch('model.types.Packet')
    @patch('model.types.Filter')
    @patch('model.types.List')
    def test_declare(self, mock_variable, mock_packet, mock_filter, mock_list):
        """
        Tests the method *SymbolHandler::declare*.
        """
        # Tests declare out of scope
        scopes = 5
        self.symbolhandler.allocate(0, scopes - 1)
        self.assertFalse(self.symbolhandler.declare(10, 'var', SymbolTypes.VARIABLE))
        # Populates the symbol handler
        id_var = 'var'
        id_pkt = 'pkt'
        id_flt = 'flt'
        id_lst = 'lst'
        for scope in range(0, scopes, 1):
            self.symbolhandler.declare(scope, id_var + str(scope), SymbolTypes.VARIABLE)
            self.symbolhandler.declare(scope, id_pkt + str(scope), SymbolTypes.PACKET)
            self.symbolhandler.declare(scope, id_flt + str(scope), SymbolTypes.FILTER)
            self.symbolhandler.declare(scope, id_lst + str(scope), SymbolTypes.LIST)
        # Test declare already exists
        for scope in range(0, scopes, 1):
            self.assertFalse(self.symbolhandler.declare(scope, id_var + str(scope), SymbolTypes.VARIABLE))
            self.assertFalse(self.symbolhandler.declare(scope, id_pkt + str(scope), SymbolTypes.PACKET))
            self.assertFalse(self.symbolhandler.declare(scope, id_flt + str(scope), SymbolTypes.FILTER))
            self.assertFalse(self.symbolhandler.declare(scope, id_lst + str(scope), SymbolTypes.LIST))
        
    @patch('model.types.Variable')
    @patch('model.types.Packet')
    @patch('model.types.Filter')
    @patch('model.types.List')
    def test_exist(self, mock_variable, mock_packet, mock_filter, mock_list):
        """
        Tests the method *SymbolHandler::exist*.
        """
        scopes = 5
        self.symbolhandler.allocate(0, scopes - 1)
        # Tests the not existance of undeclared symbols
        id_var = 'var'
        id_pkt = 'pkt'
        id_flt = 'flt'
        id_lst = 'lst'
        self.assertFalse(self.symbolhandler.exist(id_var))
        self.assertFalse(self.symbolhandler.exist(id_pkt))
        self.assertFalse(self.symbolhandler.exist(id_flt))
        self.assertFalse(self.symbolhandler.exist(id_lst))
        # Populates the symbol handler
        for scope in range(0, scopes, 1):
            self.symbolhandler.declare(scope, id_var + str(scope), SymbolTypes.VARIABLE)
            self.symbolhandler.declare(scope, id_pkt + str(scope), SymbolTypes.PACKET)
            self.symbolhandler.declare(scope, id_flt + str(scope), SymbolTypes.FILTER)
            self.symbolhandler.declare(scope, id_lst + str(scope), SymbolTypes.LIST)
        # Test declare already exists
        for scope in range(0, scopes, 1):
            self.assertTrue(self.symbolhandler.exist(id_var + str(scope)))
            self.assertTrue(self.symbolhandler.exist(id_pkt + str(scope)))
            self.assertTrue(self.symbolhandler.exist(id_flt + str(scope)))
            self.assertTrue(self.symbolhandler.exist(id_lst + str(scope)))
     
    @patch('model.types.Variable')
    @patch('model.types.Packet')
    @patch('model.types.Filter')
    @patch('model.types.List')
    def test_clear(self, mock_variable, mock_packet, mock_filter, mock_list):
        """
        Tests the method *SymbolHandler::clear*.
        """
        # Test clear on unexisting scope
        self.assertFalse(self.symbolhandler.clear(-1))
        self.assertFalse(self.symbolhandler.clear(0))
        self.assertFalse(self.symbolhandler.clear(1))

        # Populates the symbol handler
        scopes = 5
        self.symbolhandler.allocate(0, scopes - 1)
        id_var = 'var'
        id_pkt = 'pkt'
        id_flt = 'flt'
        id_lst = 'lst'
        for scope in range(0, scopes, 1):
            self.symbolhandler.declare(scope, id_var + str(scope), SymbolTypes.VARIABLE)
            self.symbolhandler.declare(scope, id_pkt + str(scope), SymbolTypes.PACKET)
            self.symbolhandler.declare(scope, id_flt + str(scope), SymbolTypes.FILTER)
            self.symbolhandler.declare(scope, id_lst + str(scope), SymbolTypes.LIST)

        # Clears an existing symbol table
        scope_target = 0
        self.assertEqual(len(self.symbolhandler.scope_symboltable_dict), scopes)
        self.assertTrue(self.symbolhandler.clear(scope_target))
        self.assertEqual(len(self.symbolhandler.scope_symboltable_dict), scopes)
        self.assertTrue(self.symbolhandler.scope_symboltable_dict[scope_target].empty())
        
    @patch('model.types.Variable')
    @patch('model.types.Packet')
    @patch('model.types.Filter')
    @patch('model.types.List')
    def test_define(self, mock_variable, mock_packet, mock_filter, mock_list):
        """
        Tests the method *SymbolHandler::define*.
        """
        scopes = 5
        self.symbolhandler.allocate(0, scopes - 1)
        # Tries to define a VARIABLE out of scope
        with patch.dict(mock_variable.__dict__, {'identifier': 'var', 'type' : SymbolTypes.VARIABLE}, clear=False):
            self.assertFalse(self.symbolhandler.define(-1, mock_variable))
            self.assertFalse(self.symbolhandler.define(10, mock_variable))
            self.assertFalse(self.symbolhandler.exist('var'))
            # Defines the VARIABLE
            self.assertTrue(self.symbolhandler.define(0, mock_variable))
            # Tries to define the VARIABLE another time
            self.assertFalse(self.symbolhandler.define(0, mock_variable))
        # Defines the PACKET
        with patch.dict(mock_packet.__dict__, {'identifier' : 'pkt', 'type' : SymbolTypes.PACKET}, clear=False):
            self.assertTrue(self.symbolhandler.define(0, mock_packet))
        # Defines the FILTER
        with patch.dict(mock_filter.__dict__, {'identifier' : 'flt', 'type' : SymbolTypes.FILTER}, clear=False):
            self.assertTrue(self.symbolhandler.define(0, mock_filter))
        # Defines the LIST
        with patch.dict(mock_list.__dict__, {'identifier' : 'lst', 'type' : SymbolTypes.LIST}, clear=False):
            self.assertTrue(self.symbolhandler.define(0, mock_list))
        # Checks the existance of the objects previously defined
        self.assertTrue(self.symbolhandler.exist('var'))
        self.assertTrue(self.symbolhandler.exist('pkt'))
        self.assertTrue(self.symbolhandler.exist('flt'))
        self.assertTrue(self.symbolhandler.exist('lst'))

                
if __name__ == '__main__':
    unittest.main()

