# -----------------------------------------------------------------------------
# types.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module contains the model of the ADL types.
# -----------------------------------------------------------------------------


from abc import ABCMeta, abstractmethod
import copy


class Type(metaclass=ABCMeta):
    """
    Models an abstract type.
    """
    
    @abstractmethod
    def __init__(self, *args):
        pass


class SymbolTable(Type):
    """
    Models a symbol table.
    """
    
    # Types supported by the symbol table
    TYPE = {
        'VARIABLE' : 'variable',
        'FILTER' : 'filter',
        'PACKET' : 'packet',
        'LIST' : 'list',
    }
    
    def __init__(self, level):
        """
        Initializes the *SymbolTable* object.
        
        :param level: the scope level of the symbol table
        :type level: int
        
        :param types: the dictionary binding each identifier with its type
        :type types: dict
        
        :param variables: the dictionary binding each identifier 
                          with its variable
        :type values: dict

        :param lists: the dictionary binding each identifier with its value
        :type lists: dict
        """

        if level < 0:
            print("[Error] the scope level of a symbol table cannot be less than 0")
            raise ValueError
            
        self.level = level
        self.types = {}
        self.variables = {}
        self.filters = {}
        self.packets = {}
        self.lists = {}

        
    def declare(self, identifier, type):
        """
        Declares the given type having the given identifier.
        
        :param identifier: the identifier to be declared
        :type identifier: str
        
        :param type: the type of the identifier
        :type type: str
        
        :raise: ValueError
        """
        if identifier is None:
            print("[Error] the identifier '" + identifier + "' cannot be None")
            raise ValueError
        if not identifier: 
            print("[Error] the identifier '" + identifier + "' cannot be an empty string")
            raise ValueError
        if type is None:
            print("[Error] the type '" + type + "' cannot be None")
            raise ValueError
            
        # Declares the Variable
        if type == SymbolTable.TYPE['VARIABLE']:
            self.types[identifier] = SymbolTable.TYPE['VARIABLE']
            variable = Variable(identifier, Variable.TYPE['NONE'], None)
            self.variables[identifier] = copy.deepcopy(variable)
        
        # Declares the Packet
        elif type == SymbolTable.TYPE['PACKET']:
            self.types[identifier] = SymbolTable.TYPE['PACKET']
            packet = Packet(identifier)
            self.packets[identifier] = copy.deepcopy(packet)
        
        # Type not supported for declaration
        else:
            print("[Error] type '" + type + "' cannot be declared")
            raise ValueError

        
    def define(self, obj):
        """
        Defines the given obj.
        
        :param obj: the object
        :type obj: Variable, PacketFilter, List
        
        :raise: ValueError
        """
    
        # Defines the Variable
        if isinstance(obj, Variable):
            self.types[obj.identifier] = SymbolTable.TYPE['VARIABLE']
            self.variables[obj.identifier] = copy.deepcopy(obj)
        
        # Defines the PacketFilter
        elif isinstance(obj, PacketFilter):
            self.types[obj.identifier] = SymbolTable.TYPE['FILTER']
            self.filters[obj.identifier] = copy.deepcopy(obj)
            
        # Defines the List
        elif isinstance(obj, List):
            self.types[obj.identifier] = SymbolTable.TYPE['LIST']
            self.lists[obj.identifier] = copy.deepcopy(obj.variables)
        
        # Object not supported
        else:
            print("[Error] '" + type(obj) + "' cannot be defined")
            raise SyntaxError

    
    def exist(self, identifier):
        """
        Checks if the given identifier exists inside the symbol table.
        
        :param identifier: the identifier
        :type identifier: str

        :return: True if the identifier exists inside the symbol table, 
                 False otherwise
        """
        
        if self.types.get(identifier, None) is None:
            return False
        return True
    

    def type(self, identifier):
        """
        Gets the type of a given identifier, if it exists inside 
        the symbol table.
        
        :param identifier: the identifier
        :type identifier: str
        
        :return: The type of the identifier, None otherwise
        """

        return self.types.get(identifier, None)


    def variable(self, identifier):
        """
        Gets the variable having a given identifier, if it exists inside 
        the symbol table.

        :param identifier: the identifier
        :type identifier: str
        
        :return: the variable if it exists, None otherwise
        """
        
        return self.variables.get(identifier, None)
    
    
    def list(self, identifier):
        """
        Gets the list having a given identifier, if it exists 
        inside the symbol table.

        :param identifier: the identifier
        :type identifier: str
        
        :return: the list if it exists, None otherwise
        """
        
        return self.lists.get(identifier, None)
    
    
    def clear(self):
        """
        Clears the symbol table.
        """
        
        self.types.clear()
        self.variables.clear()
        self.filters.clear()
        self.packets.clear()
        self.lists.clear()


class Variable(Type):
    """
    A variable is a generic container.
    """
    
    TYPE = {
        'RESERVED' : 'reserved',
        'INTEGER' : 'integer',        
        'STRING' : 'string',
        'REAL' : 'real',
        'NONE' : 'none',
    }
    
    def __init__(self, identifier, type, value):
        """
        Initializes the *Variable* object.
        
        :param identifier: The identifier of the variable
        :type identifier: str

        :param type: The type of the variable
        :type type: str

        :param value: The value of the variable
        :type value: str
        """
        
        if identifier is None:
            print("[Error] the argument 'identifier' cannot be 'None'")
            raise ValueError
        if not identifier: 
            print("[Error] the argument 'identifier' cannot be an empty string")
            raise ValueError
        if type is None:
            print("[Error] the argument 'type' cannot be 'None'")
            raise ValueError
        if type not in list(Variable.TYPE.values()):
            print("[Error] type '" + type + "' not supported")
            raise ValueError

        # TODO checks the value against the type

        self.identifier = identifier
        self.type = type
        self.value = value


class List(Type):
    """
    A list contains the references of its variables.
    """
    
    def __init__(self, identifier, variables):
        """
        Initializes the *List* object.

        :param identifier: the identifier of the list
        :type identifier: str
        
        :param variables: the list of references of variables
        :type variables: list
        """
        
        self.identifier = identifier
        self.variables = variables


class Packet(Type):
    """
    Models a packet.
    """

    def __init__(self, identifier):
        """
        Initializes the *Packet* object.
        
        :param identifier: the identifier of the list
        :type identifier: str
        """
        
        self.identifier = identifier
    


class PacketFilterElement(Type):
    """
    Models the packet filter basic element. It contains:
    + one left operand,
    + one comparison operator,
    + one right operand.
    """
    
    def __init__(self, left_operand, comparison_operator, right_operand):
        """
        Initializes the *PacketFilterElement* object.
        
        :param left_operand: the identifier of the left operand
        :type left_operand: str
        
        :param comparison_operator: the comparison operator
        :type comparison_operator: str
        
        :param right_operand: the identifier of the right operand
        :type right_operand: str
        """
        
        self.left_operand = left_operand
        self.comparison_operator = comparison_operator
        self.right_operand = right_operand


class PacketFilter(Type):
    """
    Models the packet filter, i.e. the conditional statement inside a conditional attack. 
    It contains a list of *FilterElement*s stored in RPN order.
    """
    
    def __init__(self, identifier, rpn):
        """
        Initializes the *PacketFilter* object.
        
        :param identifier: the identifier of the filter
        :type identifier: str
        
        :param rpn: the list of *FilterElements* stored in RPN order
        :type rpn: list
        """
        
        self.identifier = identifier
        self.rpn = copy.deepcopy(rpn)

