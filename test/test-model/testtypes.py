#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# testkeywords.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module tests the mechanism for handling ADL types.
#
# Usage: 
# $ python3 -m unittest -v testtypes.py
# -----------------------------------------------------------------------------

import sys
import enum
import unittest

sys.path.insert(0,"../../adl/")
import model.types as types
import lexer.lexer as lexer
import lexer.keywords as keywords

class TestTypes(unittest.TestCase):
    """
    Tests for the mechanism to handle ADL types.
    """
    
    def setUp(self):
        """
        Sets up the test.
        """
        # Builds the control list of tuples
        self.tuples = list(keywords.Type.view().items())
        self.tuples.append((lexer.BasicSymbol.OPERATOR.name, lexer.BasicSymbol.OPERATOR.value))

    def tearDown(self):
        """
        Tears down the test.
        """
        del self.tuples[:]
        
    def test_class_symbol(self):
        """
        Tests the method _reserved()
        """
        for i, e in enumerate(types.Symbol.Type):
            self.assertIn((e.name, e.value), self.tuples)
        self.assertEqual(i + 1, len(self.tuples))
        
    def test_class_operator(self):
        """
        Tests the class types.Operator.
        """
        # Tests the type of the symbol
        self.assertEqual(types.Operator.symboltype, types.Symbol.Type.OPERATOR)
        # Tests the argument guards
        operator = None
        self.assertRaises(ValueError, types.Operator, operator)
        operator = ''
        self.assertRaises(ValueError, types.Operator, operator)
        # Tests the initializer
        operator = '=='
        obj = types.Operator(operator)
        identifier = types.Symbol._Symbol__prefix + operator
        self.assertEqual(obj.identifier, identifier)
        self.assertEqual(obj.operator, operator)
         
    def test_class_variable(self):
        """
        Tests the class types.Variable.
        """       
        # Tests the type of the symbol
        self.assertEqual(types.Variable.symboltype, types.Symbol.Type.VARIABLE)
        # Tests the argument guards
        identifier = None
        variabletype = types.Variable.Type.INTEGER
        value = 10
        self.assertRaises(ValueError, types.Variable, identifier, variabletype, value)
        identifier = ''
        self.assertRaises(ValueError, types.Variable, identifier, variabletype, value)
        identifier = 'var'
        variabletype = None
        self.assertRaises(ValueError, types.Variable, identifier, variabletype, value)
        variabletype = types.Symbol.Type.OPERATOR
        self.assertRaises(ValueError, types.Variable, identifier, variabletype, value)
        # Tests the initializer
        variabletype = types.Variable.Type.INTEGER
        obj = types.Variable(identifier, variabletype, value)
        self.assertEqual(obj.identifier, identifier)
        self.assertEqual(obj.variabletype, variabletype)
        self.assertEqual(obj.value, value)

    def test_class_packet(self):
        """
        Tests the class types.Packet.
        """       
        # Tests the type of the symbol
        self.assertEqual(types.Packet.symboltype, types.Symbol.Type.PACKET)
        # Tests the argument guards
        identifier = None
        self.assertRaises(ValueError, types.Packet, identifier)
        identifier = ''
        self.assertRaises(ValueError, types.Packet, identifier)
        # Tests the initializer
        identifier = 'pkt'
        obj = types.Packet(identifier)
        self.assertEqual(obj.identifier, identifier)
    
    def test_class_filter(self):
        """
        Tests the class types.Filter.
        """       
        # Tests the type of the symbol
        self.assertEqual(types.Filter.symboltype, types.Symbol.Type.FILTER)
        # Tests the argument guards
        identifier = None
        items = ('id1', 'id2', '__id3')
        self.assertRaises(ValueError, types.Filter, identifier, items)
        identifier = ''
        self.assertRaises(ValueError, types.Filter, identifier, items)
        identifier = 'flt'
        items = ()
        self.assertRaises(ValueError, types.Filter, identifier, items)
        # Tests the initializer
        items = ('id1', 'id2', '__id3')
        obj = types.Filter(identifier, items)
        self.assertEqual(obj.identifier, identifier)
        self.assertTupleEqual(obj.items, items)
    
    def test_class_list(self):
        """
        Tests the class types.List.
        """       
        # Tests the type of the symbol
        self.assertEqual(types.List.symboltype, types.Symbol.Type.LIST)
        # Tests the argument guards
        identifier = None
        items = ('id1', 'id2', 'id3')
        self.assertRaises(ValueError, types.List, identifier, items)
        identifier = ''
        self.assertRaises(ValueError, types.List, identifier, items)
        identifier = 'flt'
        items = ()
        self.assertRaises(ValueError, types.List, identifier, items)
        # Tests the initializer
        items = ('id1', 'id2', 'id3')
        obj = types.List(identifier, items)
        self.assertEqual(obj.identifier, identifier)
        self.assertTupleEqual(obj.items, items)

    def test_class_symboltable(self):
        """
        Tests the class types.SymbolTable.
        """       


class TestSymbolTable(unittest.TestCase):
    """
    Tests for the ADL SymbolTable.
    """
    
    def setUp(self):
        """
        Sets up a symbol table.
        """        
        # Builds a symbol table 
        self.symboltable = types.SymbolTable(0)
        self.assertTrue(self.symboltable.empty())

    def tearDown(self):
        """
        Tears down the test class.
        """
        self.symboltable.clear()
        self.assertTrue(self.symboltable.empty())

    def test_declare(self):
        """
        Tests the method SymbolTable::declare.
        """
        # Tries to declare undefinible objects
        self.assertRaises(ValueError, self.symboltable.declare, None, types.Symbol.Type.VARIABLE)
        self.assertRaises(ValueError, self.symboltable.declare, '', types.Symbol.Type.VARIABLE)
        self.assertRaises(ValueError, self.symboltable.declare, 'obj', None)
        self.assertRaises(ValueError, self.symboltable.declare, 'obj', types.Variable.Type.STRING)
        self.assertRaises(ValueError, self.symboltable.declare, 'obj', types.Symbol.Type.FILTER)
        self.assertRaises(ValueError, self.symboltable.declare, 'obj', types.Symbol.Type.LIST)
        self.assertRaises(ValueError, self.symboltable.declare, 'obj', types.Symbol.Type.OPERATOR)
        self.assertFalse(self.symboltable.exist(None))
        self.assertFalse(self.symboltable.exist(''))
        self.assertFalse(self.symboltable.exist('obj'))
        # Tests double declaration guard
        self.assertTrue(self.symboltable.declare('var', types.Symbol.Type.VARIABLE))
        self.assertFalse(self.symboltable.declare('var', types.Symbol.Type.VARIABLE))
        self.assertTrue(self.symboltable.declare('pkt', types.Symbol.Type.PACKET))
        self.assertFalse(self.symboltable.declare('pkt', types.Symbol.Type.PACKET))
        # Checks the existance of the declared objects
        self.assertTrue(self.symboltable.exist('var'))
        self.assertEqual(self.symboltable.type('var'), types.Symbol.Type.VARIABLE)
        self.assertIsNotNone(self.symboltable.object('var'))
        self.assertTrue(self.symboltable.exist('pkt'))
        self.assertEqual(self.symboltable.type('pkt'), types.Symbol.Type.PACKET)
        self.assertIsNotNone(self.symboltable.object('pkt'))

    def test_define(self):
        """
        Tests the method SymbolTable::define.
        """
        # Checks the argument guards
        class Test(object):
            """
            Test class.
            """
            def __init__(self, identifier, symboltype):
                self.identifier = identifier
                self.symboltype = symboltype
            
        obj = Test(None, 'MYTYPE')
        self.assertRaises(ValueError, self.symboltable.define, obj)
        obj = Test('', 'MYTYPE')
        self.assertRaises(ValueError, self.symboltable.define, obj)
        obj = Test('obj', None)
        self.assertRaises(ValueError, self.symboltable.define, obj)
        obj = Test('obj', 'MYTYPE')
        self.assertRaises(ValueError, self.symboltable.define, obj)
        self.assertFalse(self.symboltable.exist(None))
        self.assertFalse(self.symboltable.exist(''))
        self.assertFalse(self.symboltable.exist('obj'))
        # Tests double definition guard
        operator = '=='
        obj = types.Operator(operator)
        identifier_operator = obj.identifier
        self.assertTrue(self.symboltable.define(obj))
        self.assertFalse(self.symboltable.define(obj))
        identifier_variable = 'var'
        obj = types.Variable(identifier_variable, types.Variable.Type.INTEGER, 10)
        self.assertTrue(self.symboltable.define(obj))
        self.assertFalse(self.symboltable.define(obj))
        identifier_packet = 'pkt'
        obj = types.Packet(identifier_packet)
        self.assertTrue(self.symboltable.define(obj))
        self.assertFalse(self.symboltable.define(obj))
        identifier_filter = 'flt'
        obj = types.Filter(identifier_filter, [1,2,3,4])
        self.assertTrue(self.symboltable.define(obj))
        self.assertFalse(self.symboltable.define(obj))
        identifier_list = 'lst'
        obj = types.List(identifier_list, [1,2,3,4])
        self.assertTrue(self.symboltable.define(obj))
        self.assertFalse(self.symboltable.define(obj))
        # Checks the existance of the defined objects
        self.assertTrue(self.symboltable.exist(identifier_operator))
        self.assertEqual(self.symboltable.type(identifier_operator), types.Symbol.Type.OPERATOR)
        self.assertTrue(self.symboltable.exist(identifier_variable))
        self.assertEqual(self.symboltable.type(identifier_variable), types.Symbol.Type.VARIABLE)
        self.assertIsNotNone(self.symboltable.object(identifier_variable))
        self.assertTrue(self.symboltable.exist(identifier_packet))
        self.assertEqual(self.symboltable.type(identifier_packet), types.Symbol.Type.PACKET)
        self.assertIsNotNone(self.symboltable.object(identifier_packet))
        self.assertTrue(self.symboltable.exist(identifier_filter))
        self.assertEqual(self.symboltable.type(identifier_filter), types.Symbol.Type.FILTER)
        self.assertIsNotNone(self.symboltable.object(identifier_filter))
        self.assertTrue(self.symboltable.exist(identifier_list))
        self.assertEqual(self.symboltable.type(identifier_list), types.Symbol.Type.LIST)
        self.assertIsNotNone(self.symboltable.object(identifier_list))
        
    def test_object(self):
        """
        Tests the method SymbolTable::object.
        """
        # Tries to get undeclared objects
        self.assertIsNone(self.symboltable.object('var'))
        self.assertIsNone(self.symboltable.object('pkt'))
        # Declare objects
        self.symboltable.declare('var', types.Symbol.Type.VARIABLE)
        self.symboltable.declare('pkt', types.Symbol.Type.PACKET)
        # Gets the declared objects
        self.assertIsNotNone(self.symboltable.object('var'))
        self.assertIsNotNone(self.symboltable.object('pkt'))

    def test_type(self):
        """
        Tests the method SymbolTable::type.
        """
        # Defines an operator
        operator = '=='
        obj = types.Operator(operator)
        identifier_operator = obj.identifier
        self.assertTrue(self.symboltable.define(obj))
        # Defines a variable
        identifier_variable = 'var'
        obj = types.Variable(identifier_variable, types.Variable.Type.INTEGER, 10)
        self.assertTrue(self.symboltable.define(obj))
        # Defines a packet
        identifier_packet = 'pkt'
        obj = types.Packet(identifier_packet)
        self.assertTrue(self.symboltable.define(obj))
        # Defines a filter
        identifier_filter = 'flt'
        obj = types.Filter(identifier_filter, [1,2,3,4])
        self.assertTrue(self.symboltable.define(obj))
        # Defines a list
        identifier_list = 'lst'
        obj = types.List(identifier_list, [1,2,3,4])
        self.assertTrue(self.symboltable.define(obj))
        # Checks the type of the objects previously defined
        self.assertEqual(self.symboltable.type(identifier_operator), types.Symbol.Type.OPERATOR)
        self.assertEqual(self.symboltable.type(identifier_variable), types.Symbol.Type.VARIABLE)
        self.assertEqual(self.symboltable.type(identifier_packet), types.Symbol.Type.PACKET)
        self.assertEqual(self.symboltable.type(identifier_filter), types.Symbol.Type.FILTER)
        self.assertEqual(self.symboltable.type(identifier_list), types.Symbol.Type.LIST)

    def test_exist(self):
        """
        Tests the method SymbolTable::exist.
        """
        # Defines an operator
        operator = '=='
        obj = types.Operator(operator)
        identifier_operator = obj.identifier
        self.assertTrue(self.symboltable.define(obj))
        # Defines a variable
        identifier_variable = 'var'
        obj = types.Variable(identifier_variable, types.Variable.Type.INTEGER, 10)
        self.assertTrue(self.symboltable.define(obj))
        # Defines a packet
        identifier_packet = 'pkt'
        obj = types.Packet(identifier_packet)
        self.assertTrue(self.symboltable.define(obj))
        # Defines a filter
        identifier_filter = 'flt'
        obj = types.Filter(identifier_filter, [1,2,3,4])
        self.assertTrue(self.symboltable.define(obj))
        # Defines a list
        identifier_list = 'lst'
        obj = types.List(identifier_list, [1,2,3,4])
        self.assertTrue(self.symboltable.define(obj))
        # Checks if the defined objects exist
        self.assertTrue(self.symboltable.exist(identifier_operator))
        self.assertTrue(self.symboltable.exist(identifier_variable))
        self.assertTrue(self.symboltable.exist(identifier_packet))
        self.assertTrue(self.symboltable.exist(identifier_filter))
        self.assertTrue(self.symboltable.exist(identifier_list))
        
    def test_empty(self):
        """
        Tests the method SymbolTable::empty.
        """
        # Checks if the symbol table is empty
        self.assertTrue(not any(self.symboltable.identifier_symboltype_dict))
        self.assertTrue(not any(self.symboltable.identifier_object_dict))
        self.assertTrue(self.symboltable.empty())
        # Declares an objects
        self.symboltable.declare('var', types.Symbol.Type.VARIABLE)
        # Checks if the symbol table is not empty
        self.assertTrue(any(self.symboltable.identifier_symboltype_dict))
        self.assertTrue(any(self.symboltable.identifier_object_dict))
        self.assertFalse(self.symboltable.empty())

    def test_clear(self):
        """
        Tests the method SymbolTable::clear.
        """
        # Defines an operator
        operator = '=='
        obj = types.Operator(operator)
        identifier_operator = obj.identifier
        self.assertTrue(self.symboltable.define(obj))
        # Defines a variable
        identifier_variable = 'var'
        obj = types.Variable(identifier_variable, types.Variable.Type.INTEGER, 10)
        self.assertTrue(self.symboltable.define(obj))
        # Defines a packet
        identifier_packet = 'pkt'
        obj = types.Packet(identifier_packet)
        self.assertTrue(self.symboltable.define(obj))
        # Defines a filter
        identifier_filter = 'flt'
        obj = types.Filter(identifier_filter, [1,2,3,4])
        self.assertTrue(self.symboltable.define(obj))
        # Defines a list
        identifier_list = 'lst'
        obj = types.List(identifier_list, [1,2,3,4])
        self.assertTrue(self.symboltable.define(obj))
        # Clears the symbol table
        self.symboltable.clear()
        # Checks if the symbol table is empty
        self.assertTrue(self.symboltable.empty())
        

class TestSymbolHandler(unittest.TestCase):
    """
    Tests for the ADL SymbolHandler.
    """
    
    def setUp(self):
        """
        Sets up a symbol table.
        """        
        # Builds a symbol handler
        self.symbolhandler = types.SymbolHandler()
        # Tests empty
        self.assertEqual(len(self.symbolhandler.scope_symboltable_dict), 0)

    def tearDown(self):
        """
        Tears down the test class.
        """
        self.symbolhandler.dump()

    def test_allocate(self):
        """
        Tests the method SymbolHandler::allocate.
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
        Tests the method SymbolHandler::dump.
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
        
    def test_declare(self):
        """
        Tests the method SymbolHandler::declare.
        """
        # Tests declare out of scope
        scopes = 5
        self.symbolhandler.allocate(0, scopes - 1)
        self.assertFalse(self.symbolhandler.declare(10, 'var', types.Symbol.Type.VARIABLE))
        # Populates the symbol handler
        identifier_operand = '__=='
        identifier_variable = 'var'
        identifier_packet = 'pkt'
        identifier_filter = 'flt'
        identifier_list = 'lst'
        for scope in range(0, scopes, 1):
            self.assertRaises(ValueError, self.symbolhandler.declare, 
                    scope, identifier_operand + str(scope), types.Symbol.Type.OPERATOR)
            self.assertTrue(self.symbolhandler.declare(
                    scope, identifier_variable + str(scope), types.Symbol.Type.VARIABLE))
            self.assertTrue(self.symbolhandler.declare(
                    scope, identifier_packet + str(scope), types.Symbol.Type.PACKET))
            self.assertRaises(ValueError, self.symbolhandler.declare, 
                    scope, identifier_filter + str(scope), types.Symbol.Type.FILTER)
            self.assertRaises(ValueError, self.symbolhandler.declare, 
                    scope, identifier_list + str(scope), types.Symbol.Type.LIST)
        # Tests double declaration guard
        for scope in range(0, scopes, 1):
            self.assertFalse(self.symbolhandler.declare(
                    scope, identifier_variable + str(scope), types.Symbol.Type.VARIABLE))
            self.assertFalse(self.symbolhandler.declare(
                    scope, identifier_packet + str(scope), types.Symbol.Type.PACKET))       

    def test_define(self):
        """
        Tests the method SymbolHandler::define.
        """
        scopes = 5
        self.symbolhandler.allocate(0, scopes - 1)
        # Test out of scope guard
        operator = '=='
        obj = types.Operator(operator)
        identifier_operator = obj.identifier
        self.assertFalse(self.symbolhandler.define(-1, obj))
        self.assertFalse(self.symbolhandler.define(10, obj))
        self.assertFalse(self.symbolhandler.exist(identifier_operator))
        # Defines an operator and test double definition guard
        self.assertTrue(self.symbolhandler.define(0, obj))
        self.assertFalse(self.symbolhandler.define(0, obj))
        # Defines a variable and test double definition guard
        identifier_variable = 'var'
        obj = types.Variable(identifier_variable, types.Variable.Type.INTEGER, 10)
        self.assertTrue(self.symbolhandler.define(0, obj))
        self.assertFalse(self.symbolhandler.define(0, obj))
        # Defines a packet and test double definition guard
        identifier_packet = 'pkt'
        obj = types.Packet(identifier_packet)
        self.assertTrue(self.symbolhandler.define(0, obj))
        self.assertFalse(self.symbolhandler.define(0, obj))
        # Defines a filter and test double definition guard
        identifier_filter = 'flt'
        obj = types.Filter(identifier_filter, [1,2,3,4])
        self.assertTrue(self.symbolhandler.define(0, obj))
        self.assertFalse(self.symbolhandler.define(0, obj))
        # Defines a list and test double definition guard
        identifier_list = 'lst'
        obj = types.List(identifier_list, [1,2,3,4])
        self.assertTrue(self.symbolhandler.define(0, obj))
        self.assertFalse(self.symbolhandler.define(0, obj))

    def test_exist(self):
        """
        Tests the method SymbolHandler::exist.
        """
        scopes = 5
        self.symbolhandler.allocate(0, scopes - 1)
        # Defines an operator
        operator = '=='
        obj = types.Operator(operator)
        identifier_operator = obj.identifier
        self.assertTrue(self.symbolhandler.define(0, obj))
        # Defines a variable
        identifier_variable = 'var'
        obj = types.Variable(identifier_variable, types.Variable.Type.INTEGER, 10)
        self.assertTrue(self.symbolhandler.define(1, obj))
        # Defines a packet
        identifier_packet = 'pkt'
        obj = types.Packet(identifier_packet)
        self.assertTrue(self.symbolhandler.define(2, obj))
        # Defines a filter
        identifier_filter = 'flt'
        obj = types.Filter(identifier_filter, [1,2,3,4])
        self.assertTrue(self.symbolhandler.define(3, obj))
        # Defines a list
        identifier_list = 'lst'
        obj = types.List(identifier_list, [1,2,3,4])
        self.assertTrue(self.symbolhandler.define(4, obj))
        # Checks the existance of the objects previously defined
        self.assertTrue(self.symbolhandler.exist(identifier_operator))
        self.assertTrue(self.symbolhandler.exist(identifier_variable))
        self.assertTrue(self.symbolhandler.exist(identifier_packet))
        self.assertTrue(self.symbolhandler.exist(identifier_filter))
        self.assertTrue(self.symbolhandler.exist(identifier_list))
     
    def test_clear(self):
        """
        Tests the method SymbolHandler::clear.
        """
        # Test clear on unexisting scope
        self.assertFalse(self.symbolhandler.clear(-1))
        self.assertFalse(self.symbolhandler.clear(0))
        self.assertFalse(self.symbolhandler.clear(1))
        # Populates the symbol handler
        scopes = 5
        self.symbolhandler.allocate(0, scopes - 1)
        # Defines an operator
        operator = '=='
        obj = types.Operator(operator)
        identifier_operator = obj.identifier
        self.assertTrue(self.symbolhandler.define(0, obj))
        # Defines a variable
        identifier_variable = 'var'
        obj = types.Variable(identifier_variable, types.Variable.Type.INTEGER, 10)
        self.assertTrue(self.symbolhandler.define(1, obj))
        # Defines a packet
        identifier_packet = 'pkt'
        obj = types.Packet(identifier_packet)
        self.assertTrue(self.symbolhandler.define(2, obj))
        # Defines a filter
        identifier_filter = 'flt'
        obj = types.Filter(identifier_filter, [1,2,3,4])
        self.assertTrue(self.symbolhandler.define(3, obj))
        # Defines a list
        identifier_list = 'lst'
        obj = types.List(identifier_list, [1,2,3,4])
        self.assertTrue(self.symbolhandler.define(4, obj))    
        # Clears an existing symbol table
        scope_target = 0
        self.assertEqual(len(self.symbolhandler.scope_symboltable_dict), scopes)
        self.assertTrue(self.symbolhandler.clear(scope_target))
        self.assertEqual(len(self.symbolhandler.scope_symboltable_dict), scopes)
        self.assertTrue(self.symbolhandler.scope_symboltable_dict[scope_target].empty())
        

if __name__ == '__main__':
    unittest.main()

