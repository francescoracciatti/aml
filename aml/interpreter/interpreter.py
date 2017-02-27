# -----------------------------------------------------------------------------
# xml.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module contains the interpreting services for AML.
# -----------------------------------------------------------------------------

import abc
import enum

import model.types as types
import model.statements as statements


class Interpreter(metaclass=abc.ABCMeta):
    """
    Abstract base class for interpreters.
    """
    
    @abc.abstractclassmethod
    def interpret(cls, aml, type):
        """
        Interprets the given AML source string.
        """
        pass


class Xml(Interpreter):
    """
    Provides an XML interpreter for AML.
    """

    @classmethod
    def interpret(cls, aml, type):
        xml = ''
        xml += '<?xml version="1.0"?>'
        xml += cls.codeblock(aml, type)
        return xml

    @classmethod
    def codeblock(cls, codeblock, indent):
        """
        Provides the XML representation of the AML codeblocks.
        """
        xml = ''
        # Gets the name of the codeblock's base class
        codeblock_namebaseclass = codeblock.__class__.__bases__[0].__name__.lower()
        xml += '\t' * indent + '<' + codeblock_namebaseclass + '>\n'
        # Gets the name of the codeblock's class
        codeblock_nameclass = codeblock.__class__.__name__.lower()
        xml += '\t' * (indent + 1) + '<' + codeblock_nameclass + '>\n'
        # Gets the codeblock's attributes
        for attribute in codeblock.__dict__.keys():
            value = codeblock.__dict__[attribute]
            # Handles the symbol-table
            if isinstance(value, types.SymbolTable):
                xml += cls.symboltable(value, indent + 2)
            # Handles the codeblock-table
            elif isinstance(value, statements.CodeblockTable):
                xml += cls.codeblocktable(value, indent + 2)
            # Handles a simple attribute
            else:
                attribute_name = attribute.lower()
                xml += '\t' * (indent + 2) + '<' + attribute_name + '>'
                xml += str(value)
                xml += '</' + attribute_name + '>\n'
        xml += '\t' * (indent + 1) + '</' + codeblock_nameclass + '>\n'
        xml += '\t' * indent + '</' + codeblock_namebaseclass + '>\n'
        return xml

    @classmethod
    def codeblocktable(cls, codeblocktable, indent):
        """
        Provides the XML representation of the AML codeblock-tables.
        """
        xml = ''
        # Gets the name of the codeblocktable's class
        codeblocktable_nameclass = codeblocktable.__class__.__name__.lower()
        xml += '\t' * indent + '<' + codeblocktable_nameclass + '>\n'
        # Scans the codeblock-table codeblock by codeblock
        for codeblock in codeblocktable.codeblocks:
            # Calls recursively the method Xml.codeblock()
            xml += Xml.codeblock(codeblock, indent + 1)
        xml += '\t' * indent + '</' + codeblocktable_nameclass + '>\n'
        return xml

    @classmethod
    def symboltable(cls, symboltable, indent):
        """
        Provides the XML representation of the AML symbol-tables.
        """
        xml = ''
        # Gets the name of the symboltable's class
        symboltable_nameclass = symboltable.__class__.__name__.lower()
        xml += '\t' * indent + '<' + symboltable_nameclass + '>\n'
        # Scans the symbol-table symbol by symbol
        for symbol in symboltable.identifier_object_dict.values():
            # Gets the name of the symbol's base class
            symbol_namebaseclass = symbol.__class__.__bases__[0].__name__.lower()
            xml += '\t' * (indent + 1) + '<' + symbol_namebaseclass + '>\n'
            # Gets the name of the symbol's class
            symbol_nameclass = symbol.__class__.__name__.lower()
            xml += '\t' * (indent + 2) + '<' + symbol_nameclass + '>\n'
            # Gets the attributes
            for attribute in symbol.__dict__.keys():
                attribute_name = attribute.lower()
                xml += '\t' * (indent + 3) + '<' + attribute_name + '>'
                xml += str(symbol.__dict__[attribute])
                xml += '</' + attribute_name + '>\n'
            xml += '\t' * (indent + 2) + '</' + symbol_nameclass + '>\n'
            xml += '\t' * (indent + 1) + '</' + symbol_namebaseclass + '>\n'
        xml += '\t' * indent + '</' + symboltable_nameclass + '>\n'
        return xml


class InterpreterService(object):
    """
    Provides the XML interpreting service.
    """
    
    @enum.unique
    class Type(enum.Enum):
        """
        Interpreting services.
        """
        XML = 'xml'
        JSON = 'json'
        YAML = 'yaml'

    @classmethod
    def interpret(cls, aml, type):
        """
        Interprets the given AML source string.
        """
        if type == Type.XML:
            return xml.Xml.intepret(aml, 0)
        elif type == Type.YAML:
            raise NotImplementedError("not implemented yet")
        elif type == Type.JSON:
            raise NotImplementedError("not implemented yet")
        else:
            raise ValueError("type not supported")
