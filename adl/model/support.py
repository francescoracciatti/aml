# -----------------------------------------------------------------------------
# support.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module contains the support structures to made the ADL parser able to
# handling objects.
# -----------------------------------------------------------------------------

import abc
import enum
import copy
import inspect
import model.types as adltypes


class Support(metaclass=abc.ABCMeta):
    """
    Abstract base class for support classes.
    """
    
    @abc.abstractmethod
    def __init__(self, *args):
        pass


class SymbolHandler(Support):
    """
    A multi-scope symbols handler. It provides an high level mechanism to 
    handle the declaration and the definition of objects over a number of 
    nested scopes.

    :param verbose: the verbose flag
    :type verbose: bool
    """
    
    verbose = False
    
    def __init__(self):
        """
        Initializes the *SymbolHandler* object. Each instance owns a dictionary 
        that contains a symbol table (value) per scope (key).
        
        :param self: the reference to the instance
        :type self: model.support.SymbolHandler
        
        :param scope_symboltable_dict: the dictionary that binds a scope with a symbol table
        :type scope_symboltable_dict: dict
        """
        self.scope_symboltable_dict = {}
    
    def allocate(self, outer, inner):
        """
        Allocates a new symbol table for each scope in the given range .
        
        :param self: the reference to the instance
        :type self: model.support.SymbolHandler

        :param outer: the outer scope, included
        :type outer: int
        
        :param inner: the outer scope, included
        :type inner: int

        :raise: ValueError if *outer* is negative
        :raise: ValueError if *inner* is negative
        :raise: ValueError if *outer* is greater than *inner*
        """
        if outer < 0:
            raise ValueError(self.__error("outer cannot be negative"))
        if inner < 0:
            raise ValueError(self.__error("inner cannot be negative"))
        if outer > inner:
            raise ValueError(self.__error("outer cannot be greater than inner"))
        for scope in range(outer, inner + 1):
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
        :type self: model.support.SymbolHandler

        :param scope: the scope
        :type scope: int

        :param identifier: the identifier
        :type identifier: str

        :param type: the type
        :type type: model.types.SymbolTypes
        """
        # Checks if a symbol table exists for the given scope
        if scope not in self.scope_symboltable_dict:
            msg = self.__info("The scope " + str(scope) + " does not refer any symbol table")
            self.__log(msg)
            return False
        # Checks if the identifier does not already exist
        if self.exist(identifier):
            msg = self.__info("The identifier already exists")
            self.__log(msg)
            return False
        # Declares the identifier
        return self.scope_symboltable_dict[scope].declare(identifier, type)
        
    def define(self, scope, obj):
        """
        Defines the given objet inside the symbol table of the given scope.
        
        :param self: the reference to the instance
        :type self: model.support.SymbolHandler

        :param scope: the scope
        :type scope: int
        
        :param obj: the object
        :type obj: model.types.Variable
                 | model.types.Filter
                 | model.types.Packet
                 | model.types.List
        """
        # Checks if a symbol table exists for the given scope
        if scope not in self.scope_symboltable_dict:
            msg = self.__info("The scope " + scope + " does not refer any symbol table")
            self.__log(msg)
            return False
        # Defines the object into the given scope
        return self.scope_symboltable_dict[scope].define(obj)
    
    def clear(self, scope):
        """
        Clears the symbol table related to the given scope.
        
        :param self: the reference to the instance
        :type self: model.support.SymbolHandler

        :param scope: the scope
        :type scope: int
        
        :return: the symbol table if it exists, otherwise *None*
        """
        if scope not in self.scope_symboltable_dict:
            msg = self.__info("The scope " + scope + " does not refer any symbol table")
            self.__log(msg)
            return False
        self.scope_symboltable_dict[scope].clear()
        return True
   
    def exist(self, identifier):
        """
        Checks if the given identifier exists.
        
        :param self: the reference to the instance
        :type self: model.support.SymbolHandler
        
        :param identifier: the identifier
        :type identifier: str
        """
        # Scans all the scopes
        for scope in list(self.scope_symboltable_dict.keys()):
            if self.scope_symboltable_dict[scope].exist(identifier):
                msg = self.__info(identifier + " already exists inside the scope " + scope)
                self.__log(msg)
                return True
        return False
    
    @classmethod
    def __log(cls, msg):
        """
        Logs the given message.
        """
        if cls.verbose:
            print(msg)

    @classmethod
    def __info(cls, msg):
        """
        Builds an info message.
                
        :param cls: the reference to the class
        :type cls: model.support.SymbolHandler
        
        :param msg: the message
        :type msg: str
        
        :return: the info string
        """
        status = "[INFO]"
        classname = cls.__name__
        callername = inspect.stack()[1][3]
        prefix = "(" + classname + "::" + callername + ")"
        info = status + " " + prefix + " " + msg
        return info
        
    @classmethod
    def __warn(cls, msg):
        """
        Builds a warning message.
        
        :param cls: the reference to the class
        :type cls: model.support.SymbolHandler
        
        :param msg: the message
        :type msg: str
        
        :return: the warning string
        """
        status = "[WARNING]"
        classname = cls.__name__
        callername = inspect.stack()[1][3]
        prefix = "(" + classname + "::" + callername + ")"
        warn = status + " " + prefix + " " + msg
        return warn

    @classmethod
    def __error(cls, msg):
        """
        Builds an error message.
                
        :param cls: the reference to the class
        :type cls: model.support.SymbolHandler
        
        :param msg: the message
        :type msg: str
        
        :return: the error string
        """
        classname = cls.__name__
        callername = inspect.stack()[1][3]
        status = "[ERROR]"
        prefix = "(" + classname + "::" + callername + ")"
        error = status + " " + prefix + " " + msg
        return error
      
class SymbolTable(Support):
    """
    A symbol table that supports ADL types.
    
    :param verbose: the verbose flag
    :type verbose: bool
    """
    
    verbose = False
    
    def __init__(self, scope):
        """
        Initializes the *SymbolTable* object.
        
        :param self: the reference to the instance
        :type self: model.support.SymbolTable
        
        :param scope: the scope scope of the symbol table
        :type scope: int
        
        :param identifier_type_dict: the dictionary that binds an identifier with a type
        :type types: dict
        
        :param identifier_object_dict: the dictionary that binds an identifier with an object
        :type identifier_object_dict: dict
        """
        self.scope = scope
        self.identifier_type_dict = {}
        self.identifier_object_dict = {}

    def empty(self):
        """
        Checks if the symbol table is empty.
        
        :param self: the reference to the instance
        :type self: model.support.SymbolTable

        :return: *True* if the symbol table is empty, *False* otherwise
        """
        return not any(self.identifier_type_dict)
    
    def exist(self, identifier):
        """
        Checks if the given identifier exists.
        
        :param self: the reference to the instance
        :type self: model.support.SymbolTable
        
        :param identifier: the identifier
        :type identifier: str

        :return: *True* if the identifier exists, *False* otherwise
        """
        return identifier in self.identifier_type_dict
    
    def type(self, identifier):
        """
        Gets the type of the given identifier, if it exists.
        
        :param self: the reference to the instance
        :type self: model.support.SymbolTable
        
        :param identifier: the identifier
        :type identifier: str
        
        :return: the type, *None* otherwise
        """
        return self.identifier_type_dict.get(identifier, None)

    def object(self, identifier):
        """
        Gets the object having the given identifier, if it exists.
        
        :param self: the reference to the instance
        :type self: model.support.SymbolTable
        
        :param identifier: the identifier
        :type identifier: str
        
        :return: the object, *None* otherwise
        """
        return self.identifier_object_dict.get(identifier, None)
    
    def declare(self, identifier, type):
        """
        Declares the given identifier having the given type.
        
        :param self: the reference to the instance
        :type self: model.support.SymbolTable
        
        :param identifier: the identifier to be declared
        :type identifier: str
        
        :param type: the type
        :type type: model.types.SymbolTypes
        
        :return: *True* on success, *False* otherwise

        :raise: ValueError if identifier is *None*
        :raise: ValueError if identifier is empty
        :raise: ValueError if type is None
        :raise: ValueError if type is not recognized
        """
        if identifier is None:
            raise ValueError(self.__error("identifier cannot be None"))
        if not identifier: 
            raise ValueError(self.__error("identifier cannot be empty"))
        if type is None:
            raise ValueError(self.__error("type cannot be None"))

        # Checks if the identifier already exists
        if identifier in self.identifier_type_dict:
            msg = self.__info(identifier + " already exists")
            self.__log(msg)
            return False
            
        # Stores the type into the symbol table
        self.identifier_type_dict[identifier] = type
        # Builds an empty adltypes.VARIABLE
        if type == adltypes.SymbolTypes.VARIABLE:
            obj = adltypes.Variable(identifier, adltypes.Variable.VariableType.NONE, None)
        # Builds an empty adltypes.PACKET
        elif type == adltypes.SymbolTypes.PACKET:
            obj = adltypes.Packet(identifier)
        # Builds an empty adltypes.FILTER
        elif type == adltypes.SymbolTypes.FILTER:
            obj = adltypes.Filter(identifier, None)
        # Builds an empty adltypes.LIST
        elif type == adltypes.SymbolTypes.LIST:
            obj = adltypes.List(identifier, None)
        else:
            raise TypeError(self.__error("type " + type + " not recognized"))
        # Stores the object into the symbol table
        self.identifier_object_dict[identifier] = copy.deepcopy(obj)
        return True

    def define(self, obj):
        """
        Defines the given obj.
        
        :param self: the reference to the instance
        :type self: model.support.SymbolTable
        
        :param obj: the object
        :type obj: model.types.Variable, 
                   model.types.Filter, 
                   model.types.Packet, 
                   model.types.List
        
        :return: *True* on success, *False* otherwise

        :raise: ValueError if the object is not an instance of model.types.Type
        :raise: ValueError if the object's type is not recognized
        """
        if obj.identifier is None:
            raise ValueError(self.__error("object's identifier cannot be None"))
        if not obj.identifier: 
            raise ValueError(self.__error("object's identifier cannot be empty"))
        if obj.type is None:
            raise ValueError(self.__error("object's type cannot be None"))
        if obj.type not in adltypes.SymbolTypes:
            raise TypeError("object's type not recognized")
        
        # Checks if the identifier already exists
        if obj.identifier in self.identifier_type_dict:
            msg = self.__info(obj.identifier + " already exists")
            self.__log(msg)
            return False
        # Stores the type into the symbol table
        self.identifier_type_dict[obj.identifier] = obj.type
        # Stores the object into the symbol table
        self.identifier_object_dict[obj.identifier] = copy.deepcopy(obj)
        return True

    def clear(self):
        """
        Clears the symbol table.
        
        :param self: the reference to the instance
        :type self: model.support.SymbolTable
        """
        self.identifier_type_dict.clear()
        self.identifier_object_dict.clear()

    @classmethod
    def __log(cls, msg):
        if cls.verbose:
            print(msg)
    
    @classmethod
    def __info(cls, msg):
        """
        Builds an info message.
                
        :param cls: the reference to the class
        :type cls: model.support.SymbolHandler
        
        :param msg: the message
        :type msg: str
        
        :return: the info string
        """
        status = "[INFO]"
        classname = cls.__name__
        callername = inspect.stack()[1][3]
        prefix = "(" + classname + "::" + callername + ")"
        info = status + " " + prefix + " " + msg
        return info

    @classmethod
    def __warn(cls, msg):
        """
        Builds a warning message.
        
        :param cls: the reference to the class
        :type cls: model.support.SymbolHandler
        
        :param msg: the message
        :type msg: str
        
        :return: the warning string
        """
        status = "[WARNING]"
        classname = cls.__name__
        callername = inspect.stack()[1][3]
        prefix = "(" + classname + "::" + callername + ")"
        warn = status + " " + prefix + " " + msg
        return warn

    @classmethod
    def __error(cls, msg):
        """
        Builds an error message.
                
        :param cls: the reference to the class
        :type cls: model.support.SymbolHandler
        
        :param msg: the message
        :type msg: str
        
        :return: the error string
        """
        classname = cls.__name__
        callername = inspect.stack()[1][3]
        status = "[ERROR]"
        prefix = "(" + classname + "::" + callername + ")"
        error = status + " " + prefix + " " + msg
        return error  
        
        
        
