#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# statements_test.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module tests the mechanism for handling AML types.
#
# Usage: 
# $ python3 -m unittest -v statements_test.py
# -----------------------------------------------------------------------------

import sys
import enum
import unittest
from unittest.mock import patch

sys.path.insert(0,"../aml/")
import model.statements as statements

class TestPrimitive(unittest.TestCase):
    """
    Tests for the AML primitives.
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
        pass
        
    def test_class_disable_component(self):
        """
        Tests the class DisableComponend.
        """
        node = 'identifier'
        component = 'identifier'
        obj = statements.DisableComponent(node, component)
        self.assertIsInstance(obj, statements.Primitive)
        self.assertEqual(obj.node, node)
        self.assertEqual(obj.component, component)
        
    def test_class_deceive_component(self):
        """
        Tests the class DeceiveComponent.
        """
        node = 'identifier'
        component = 'identifier'
        value = 'identifier'
        obj = statements.DeceiveComponent(node, component, value)
        self.assertIsInstance(obj, statements.Primitive)
        self.assertEqual(obj.node, node)
        self.assertEqual(obj.component, component)
        self.assertEqual(obj.value, value)

    def test_class_destroy_component(self):
        """
        Tests the class DestroyComponent.
        """
        node = 'identifier'
        component = 'identifier'
        obj = statements.DestroyComponent(node, component)
        self.assertIsInstance(obj, statements.Primitive)
        self.assertEqual(obj.node, node)
        self.assertEqual(obj.component, component)

    def test_class_deceive_component(self):
        """
        Tests the class DeceiveComponent.
        """
        node = 'identifier'
        component = 'identifier'
        value = 'identifier'
        obj = statements.DeceiveComponent(node, component, value)
        self.assertIsInstance(obj, statements.Primitive)
        self.assertEqual(obj.node, node)
        self.assertEqual(obj.component, component)
        self.assertEqual(obj.value, value)

    def test_class_misplace_node(self):
        """
        Tests the class MisplaceNode.
        """
        node = 'identifier'
        position = 'identifier'
        obj = statements.MisplaceNode(node, position)
        self.assertIsInstance(obj, statements.Primitive)
        self.assertEqual(obj.node, node)
        self.assertEqual(obj.position, position)

    def test_class_destroy_node(self):
        """
        Tests the class DestroyNode.
        """
        node = 'identifier'
        obj = statements.DestroyNode(node)
        self.assertIsInstance(obj, statements.Primitive)
        self.assertEqual(obj.node, node)

    def test_class_write_field(self):
        """
        Tests the class WriteField.
        """
        packet = 'identifier'
        path = 'identifier'
        source = 'identifier'
        obj = statements.WriteField(packet, path, source)
        self.assertIsInstance(obj, statements.Primitive)
        self.assertEqual(obj.packet, packet)
        self.assertEqual(obj.path, path)
        self.assertEqual(obj.source, source)

    def test_class_read_field(self):
        """
        Tests the class ReadField.
        """
        destination = 'identifier'
        packet = 'identifier'
        path = 'identifier'
        obj = statements.ReadField(destination, packet, path)
        self.assertIsInstance(obj, statements.Primitive)
        self.assertEqual(obj.destination, destination)
        self.assertEqual(obj.packet, packet)
        self.assertEqual(obj.path, path)

    def test_class_forward_packet(self):
        """
        Tests the class ForwardPacket.
        """
        packet = 'identifier'
        delay = 'identifier'
        unit = 'identifier'
        obj = statements.ForwardPacket(packet, delay, unit)
        self.assertIsInstance(obj, statements.Primitive)
        self.assertEqual(obj.packet, packet)
        self.assertEqual(obj.delay, delay)
        self.assertEqual(obj.unit, unit)

    def test_class_create_packet(self):
        """
        Tests the class CreatePacket.
        """
        packet = 'identifier'
        protocol = 'identifier'
        obj = statements.CreatePacket(packet, protocol)
        self.assertIsInstance(obj, statements.Primitive)
        self.assertEqual(obj.packet, packet)
        self.assertEqual(obj.protocol, protocol)

    def test_class_inject_packet(self):
        """
        Tests the class InjectPacket.
        """
        packet = 'identifier'
        node = 'identifier'
        direction = 'identifier'
        delay = 'identifier'
        unit = 'identifier'
        obj = statements.InjectPacket(packet, node, direction, delay, unit)
        self.assertIsInstance(obj, statements.Primitive)
        self.assertEqual(obj.packet, packet)
        self.assertEqual(obj.node, node)
        self.assertEqual(obj.direction, direction)
        self.assertEqual(obj.delay, delay)
        self.assertEqual(obj.unit, unit)

    def test_class_clone_packet(self):
        """
        Tests the class ClonePacket.
        """
        destination = 'identifier'
        source = 'identifier'
        obj = statements.ClonePacket(destination, source)
        self.assertIsInstance(obj, statements.Primitive)
        self.assertEqual(obj.destination, destination)
        self.assertEqual(obj.source, source)

    def test_class_drop_packet(self):
        """
        Tests the class DropPacket.
        """
        packet = 'identifier'
        obj = statements.DropPacket(packet)
        self.assertIsInstance(obj, statements.Primitive)
        self.assertEqual(obj.packet, packet)

    def test_class_expression(self):
        """
        Tests the class Expression.
        """
        destination = 'identifier'
        expression = ['id1', 'id2', '__+']
        obj = statements.Expression(destination, expression)
        self.assertIsInstance(obj, statements.Primitive)
        self.assertEqual(obj.destination, destination)
        self.assertListEqual(obj.expression, expression)


class TestCodeblockTable(unittest.TestCase):
    """
    Tests for the AML codeblock table.
    """
    
    def setUp(self):
        """
        Sets up the test.
        """
        self.scope = 0
        self.assertRaises(ValueError, statements.CodeblockTable, -1)
        self.codeblocktable = statements.CodeblockTable(self.scope)
        self.assertEqual(len(self.codeblocktable.codeblocks), 0)
        self.assertEqual(self.codeblocktable.scope, self.scope)

    def tearDown(self):
        """
        Tears down the test.
        """
        self.codeblocktable.clear()

    @patch('model.statements.Codeblock')
    def test_append(self, mock_codeblock):
        """
        Tests the method CodeblockTable::append.
        """
        self.codeblocktable.append(mock_codeblock)
        self.assertEqual(len(self.codeblocktable.codeblocks), 1)
        self.assertIs(self.codeblocktable.codeblocks[0], mock_codeblock)
    
    @patch('model.statements.Codeblock')
    def test_clear(self, mock_codeblock):
        """
        Tests the method CodeblockTable::clear.
        """
        self.codeblocktable.append(mock_codeblock)
        self.assertEqual(len(self.codeblocktable.codeblocks), 1)
        self.codeblocktable.clear()
        self.assertEqual(len(self.codeblocktable.codeblocks), 0)


class TestCodeblockHandler(unittest.TestCase):
    """
    Tests for the AML codeblock handler.
    """
    
    def setUp(self):
        """
        Sets up the test.
        """
        self.scopes = 3
        self.assertRaises(ValueError, statements.CodeblockHandler, -1)
        self.codeblockhandler = statements.CodeblockHandler(self.scopes)
        self.assertEqual(len(self.codeblockhandler.scope_codeblocktable_dict), self.scopes)

    def tearDown(self):
        """
        Tears down the test.
        """
        self.codeblockhandler.dump()

    @patch('model.statements.Codeblock')
    def test_append(self, mock_codeblock):
        """
        Tests the method CodeblockHandler::append.
        """
        self.assertRaises(ValueError, self.codeblockhandler.append, -1, mock_codeblock)
        self.assertRaises(ValueError, self.codeblockhandler.append, 0, None)
        self.codeblockhandler.append(0, mock_codeblock)
        self.assertEqual(len(self.codeblockhandler.scope_codeblocktable_dict[0].codeblocks), 1)
    
    @patch('model.statements.Codeblock')
    def test_clear(self, mock_codeblock):
        """
        Tests the method CodeblockHandler::clear.
        """
        self.assertRaises(ValueError, self.codeblockhandler.clear, -1)
        for scope in range(0, self.scopes):
            self.codeblockhandler.append(scope, mock_codeblock)
            self.codeblockhandler.clear(scope)
            self.assertEqual(len(self.codeblockhandler.scope_codeblocktable_dict[scope].codeblocks), 0)

    @patch('model.statements.Codeblock')
    def test_dump(self, mock_codeblock):
        """
        Tests the method CodeblockHandler::dump.
        """
        self.assertRaises(ValueError, self.codeblockhandler.clear, -1)
        for scope in range(0, self.scopes):
            self.codeblockhandler.append(scope, mock_codeblock)
        self.codeblockhandler.dump()
        self.assertEqual(len(self.codeblockhandler.scope_codeblocktable_dict), 0)

