# -----------------------------------------------------------------------------
# types.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module contains the mechanism for handling the AML types.
# -----------------------------------------------------------------------------

import abc
import copy
import enum
import lexer.lexer as lexer
import lexer.keywords as keywords


# TODO embed into Symbol
def _tuples():
        """
        Builds the types of an enum.Enum class.
        """
        tuples = list(keywords.Type.view().items())
        tuples.append((lexer.BasicSymbol.RESERVED.name, lexer.BasicSymbol.RESERVED.value))
        return tuples


class Symbol(metaclass=abc.ABCMeta):
    """
    Abstract base class to build up symbols.
    
    :param __prefix: the prefix used to build the reserved identifier
    :type __prefix: str
    """

    # The symbol types
    Type = enum.Enum('Type', _tuples())

    # The prefix for name mangling
    __prefix = '__'

    @abc.abstractmethod
    def __init__(self, *args):
        pass


class Reserved(Symbol):
    """
    Container for reserved keywords.

    :param symboltype: the type of the symbol
    :type symboltype: Symbol.Type
    """
    
    symboltype = Symbol.Type.RESERVED
    
    def __init__(self, reserved):
        """
        Initializes the object. It stores the reserved keyword and assigns to it 
        a mangled identifier.

        :param reserved: the reserved keyword
        :type reserved: str

        :raise ValueError: the argument 'reserved' is None or empty
        """
        if reserved is None:
            raise ValueError("None passed as an argument")
        if not reserved:
            raise ValueError("Empty string passed as an argument")
        # TODO check if the reserved is recognized
        self.identifier = Symbol._Symbol__prefix + reserved
        self.reserved = reserved


# TODO embed into Variable
# The entry for the undefined variables
_undefined = ('NONE', 'none')

# TODO embed into Variable
def _build_variable_types():
    """
    Builds the types of this enum.Enum class.
    """
    tuples = (
        (lexer.BasicOperandType.INTEGER.name, lexer.BasicOperandType.INTEGER.value),
        (lexer.BasicOperandType.STRING.name, lexer.BasicOperandType.STRING.value),
        (lexer.BasicOperandType.REAL.name, lexer.BasicOperandType.REAL.value),
        _undefined)
    return tuples


class Variable(Symbol):
    """
    Container for variables. It can store a single string, integer or real
    value or it can be left undefined.

    :param symboltype: the type of the symbol
    :type symboltype: Symbol.Type
    """
    
    # The type of the symbol
    symboltype = Symbol.Type.VARIABLE
    
    # The variable types
    Type = enum.Enum('Type', _build_variable_types())
    
    
    @classmethod
    def autoidentifier(cls, value):
        """
        Builds an identifier from the value.
        """
        if value is None:
            raise ValueError("Cannot handle None")
        return Symbol._Symbol__prefix + str(value)
        
    
    def __init__(self, identifier, variabletype, value):
        """
        Initializes the Variable object.
        
        :param identifier: The identifier of the variable
        :type identifier: str

        :param variabletype: The type of the variable
        :type variabletype: str

        :param value: The value of the variable
        :type value: str
        """
        if identifier is None:
            raise ValueError("None passed as an identifier")
        if not identifier: 
            raise ValueError("Empty string passed as an identifier")
        if variabletype is None:
            raise ValueError("None passed as a variable type")
        if variabletype not in Variable.Type:
            raise ValueError("Variable type not recognized")

        # TODO checks the value against the type

        self.identifier = identifier
        self.variabletype = variabletype
        self.value = value


class Packet(Symbol):
    """
    Container for packets. It stores only the identifier of the packet.

    :param symboltype: the type of the symbol
    :type symboltype: Symbol.Type
    """
    
    # The type of the symbol
    symboltype = Symbol.Type.PACKET
    
    def __init__(self, identifier):
        """
        Initializes the Packet object.

        :param identifier: The identifier of the packet
        :type identifier: str
        """
        if identifier is None:
            raise ValueError("None passed as an identifier")
        if not identifier: 
            raise ValueError("Empty string passed as an identifier")
        self.identifier = identifier


class Filter(Symbol):
    """
    Container for filters. It stores the packet filter, i.e. a list of 
    identifiers that refer the filter's operands and operators.

    :param symboltype: the type of the symbol
    :type symboltype: Symbol.Type
    """
    
    # The type of the symbol
    symboltype = Symbol.Type.FILTER
    
    def __init__(self, identifier, items):
        """
        Initializes the Packet object.

        :param identifier: The identifier of the filter
        :type identifier: str
        
        :param items: The tuple of the filter's items
        :type items: tuple
        """
        if identifier is None:
            raise ValueError("None passed as an identifier")
        if not identifier: 
            raise ValueError("Empty string passed as an identifier")
        if not items: 
            raise ValueError("Empty tuple passed as items")
        self.identifier = identifier
        self.items = copy.deepcopy(items)


class List(Symbol):
    """
    Container for lists. It stores the list of 
    identifiers that refer the items owned by the list.

    :param symboltype: the type of the symbol
    :type symboltype: Symbol.Type
    """
    
    # The type of the symbol
    symboltype = Symbol.Type.LIST
    
    @classmethod
    def autoidentifier(cls, items):
        """
        Builds an identifier form the items.
        """
        if not items:
            raise ValueError("Cannot handle empty lists")
        if items is None:
            raise ValueError("Cannot handle None")
        identifier = Symbol._Symbol__prefix
        for i in items:
            identifier += i
        return identifier
    
    
    def __init__(self, identifier, items):
        """
        Initializes the List object.

        :param identifier: The identifier of the list
        :type identifier: str
        
        :param items: The tuple of the list's items
        :type items: tuple
        """
        if identifier is None:
            raise ValueError("None passed as an identifier")
        if not identifier: 
            raise ValueError("Empty string passed as an identifier")
        if not items: 
            raise ValueError("Empty tuple passed as items")
        self.identifier = identifier
        self.items = copy.deepcopy(items)


class SymbolTable(object):
    """
    A symbol table that supports AML types.
    """
    
    def __init__(self, scope):
        """
        Initializes the SymbolTable object.
        
        :param self: the reference to the instance
        :type self: model.types.SymbolTable
        
        :param scope: the scope scope of the symbol table
        :type scope: int
        
        :param identifier_symboltype_dict: the dictionary that binds an identifier with a type
        :type types: dict
        
        :param identifier_object_dict: the dictionary that binds an identifier with an object
        :type identifier_object_dict: dict
        """
        self.scope = scope
        self.identifier_symboltype_dict = {}
        self.identifier_object_dict = {}

    def empty(self):
        """
        Checks if the symbol table is empty.
        
        :param self: the reference to the instance
        :type self: model.types.SymbolTable

        :return: True if the symbol table is empty, False otherwise
        """
        return not any(self.identifier_symboltype_dict)
    
    def exist(self, identifier):
        """
        Checks if the given identifier exists.
        
        :param self: the reference to the instance
        :type self: model.types.SymbolTable
        
        :param identifier: the identifier
        :type identifier: str

        :return: True if the identifier exists, False otherwise
        """
        return identifier in self.identifier_symboltype_dict
    
    def type(self, identifier):
        """
        Gets the type of the given identifier, if it exists.
        
        :param self: the reference to the instance
        :type self: model.types.SymbolTable
        
        :param identifier: the identifier
        :type identifier: str
        
        :return: the type, None otherwise
        """
        return self.identifier_symboltype_dict.get(identifier, None)

    def object(self, identifier):
        """
        Gets the object having the given identifier, if it exists.
        
        :param self: the reference to the instance
        :type self: model.types.SymbolTable
        
        :param identifier: the identifier
        :type identifier: str
        
        :return: the object, None otherwise
        """
        return self.identifier_object_dict.get(identifier, None)
    
    def declare(self, identifier, type):
        """
        Declares the given identifier having the given type.
        
        :param self: the reference to the instance
        :type self: model.types.SymbolTable
        
        :param identifier: the identifier to be declared
        :type identifier: str
        
        :param type: the type
        :type type: model.types.Symbol.Type
        
        :return: True on success, False otherwise
        """
        if identifier is None:
            raise ValueError("identifier cannot be None")
        if not identifier: 
            raise ValueError("identifier cannot be empty")
        if type is None:
            raise ValueError("type cannot be None")
        if type not in Symbol.Type:
            raise ValueError("type " + str(type) + " not recognized")
        if type == Symbol.Type.FILTER:
            raise ValueError("filter cannot be declared (only defined)")
        if type == Symbol.Type.LIST:
            raise ValueError("list cannot be declared (only defined)")
        if type == Symbol.Type.RESERVED:
            raise ValueError("reserved cannot be explicitly declared")

        # Checks if the identifier already exists
        if identifier in self.identifier_symboltype_dict:
            return False
            
        # Stores the type into the symbol table
        self.identifier_symboltype_dict[identifier] = type
        # Builds an empty VARIABLE
        if type == Symbol.Type.VARIABLE:
            obj = Variable(identifier, Variable.Type.NONE, None)
        # Builds an empty PACKET
        elif type == Symbol.Type.PACKET:
            obj = Packet(identifier)

        # Stores the object into the symbol table
        self.identifier_object_dict[identifier] = copy.deepcopy(obj)
        return True

    def define(self, obj):
        """
        Defines the given obj.
        
        :param self: the reference to the instance
        :type self: model.types.SymbolTable
        
        :param obj: the object
        :type obj: model.types.Symbol.Type
        
        :return: True on success, False otherwise
        """
        if obj.identifier is None:
            raise ValueError("object's identifier cannot be None")
        if not obj.identifier: 
            raise ValueError("object's identifier cannot be empty")
        if obj.symboltype is None:
            raise ValueError("object's type cannot be None")
        if obj.symboltype not in Symbol.Type:
            raise ValueError("object's type not recognized")
        
        # Checks if the identifier already exists
        if obj.identifier in self.identifier_symboltype_dict:
            return False
        # Stores the type into the symbol table
        self.identifier_symboltype_dict[obj.identifier] = obj.symboltype
        # Stores the object into the symbol table
        self.identifier_object_dict[obj.identifier] = copy.deepcopy(obj)
        return True

    def clear(self):
        """
        Clears the symbol table.
        
        :param self: the reference to the instance
        :type self: model.types.Symbol.Type
        """
        self.identifier_symboltype_dict.clear()
        self.identifier_object_dict.clear()


class SymbolHandler(object):
    """
    A multi-scope symbols handler. It provides an high level mechanism to 
    handle the declaration and the definition of objects over a number of 
    nested scopes.
    """
    
    
    def __init__(self, scopes):
        """
        Initializes the SymbolHandler object. Each instance owns a dictionary 
        that contains a symbol table (value) per scope (key).
        
        :param self: the reference to the instance
        :type self: model.types.SymbolHandler

        :param scopes: the number of scopes
        :type scopes: int        
        """
        if scopes < 0:
            raise ValueError("scopes cannot be negative")
        self.scope_symboltable_dict = {}
        for scope in range(0, scopes):
            self.scope_symboltable_dict[scope] = SymbolTable(scope)
    
    def dump(self):
        """
        Dumps all the symbol tables
        """
        self.scope_symboltable_dict.clear()

    def declare(self, scope, identifier, type):
        """
        Declares the given identifier of the given type inside the symbol table 
        of the given scope.
        
        :param self: the reference to the instance
        :type self: model.types.SymbolHandler

        :param scope: the scope
        :type scope: int

        :param identifier: the identifier
        :type identifier: str

        :param type: the type
        :type type: model.types.Symbol.Type
        """
        # Checks if a symbol table exists for the given scope
        if scope not in self.scope_symboltable_dict:
            return False
        # Checks if the identifier does not already exist
        if self.exist(scope, identifier):
            return False
        # Declares the identifier
        return self.scope_symboltable_dict[scope].declare(identifier, type)
        
    def define(self, scope, obj):
        """
        Defines the given objet inside the symbol table of the given scope.
        
        :param self: the reference to the instance
        :type self: model.types.SymbolHandler

        :param scope: the scope
        :type scope: int
        
        :param obj: the object
        :type obj: model.types.Reserved
                 | model.types.Variable
                 | model.types.Filter
                 | model.types.Packet
                 | model.types.List
        """
        # Checks if a symbol table exists for the given scope
        if scope not in self.scope_symboltable_dict:
            return False
        # Defines the object into the given scope
        return self.scope_symboltable_dict[scope].define(obj)
    
    def clear(self, scope):
        """
        Clears the symbol table related to the given scope.
        
        :param self: the reference to the instance
        :type self: model.types.SymbolHandler

        :param scope: the scope
        :type scope: int
        
        :return: the symbol table if it exists, otherwise *None*
        """
        if scope not in self.scope_symboltable_dict:
            return False
        self.scope_symboltable_dict[scope].clear()
        return True
   
    def exist(self, outer, identifier):
        """
        Checks if the given identifier exists in the range [0, outer].
        
        :param self: the reference to the instance
        :type self: model.types.SymbolHandler
        
        :param outer: the outer scoper
        :type outer: int

        :param identifier: the identifier
        :type identifier: str
        """
        if outer not in self.scope_symboltable_dict:
            raise ValueError("out of scope")
        for scope in range(0, outer + 1):
            if self.scope_symboltable_dict[scope].exist(identifier):
                return True
        return False

    def object(self, identifier):
        """
        Gets the object having the given identifier, if it exists.
        
        :param self: the reference to the instance
        :type self: model.types.SymbolTable
        
        :param identifier: the identifier
        :type identifier: str
        
        :return: the object, None otherwise
        """
        for symboltable in list(self.scope_symboltable_dict.values()):
            obj = symboltable.object(identifier)
            if obj is not None:
                return obj
        return None

