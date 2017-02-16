# -----------------------------------------------------------------------------
# actions.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module contains the model for the ADL codeblocks and primitives.
# -----------------------------------------------------------------------------

import abc
import copy


class Primitive(metaclass=abc.ABCMeta):
    """
    Abstract base class for primitives.
    """

    @abc.abstractmethod
    def __init__(self, *args):
        pass


class DisableComponent(Primitive):
    """
    Models the 'disableComponent(node, component)' primitive.
    """
    
    def __init__(self, node, component):
        """
        Initializes the *DisableComponent* object.

        :param node: the identifier of the variable in the symbol table 
                     referring the node
        :type node: str
        
        :param component: the identifier of the variable in the symbol table 
                          referring the component
        :type component: str
        """
        self.node = node
        self.component = component


class DeceiveComponent(Primitive):
    """
    Models the 'deceiveComponent(node, component, value)' primitive.
    """
    
    def __init__(self, node, component, value):
        """
        Initializes the *DeceiveComponent* object.

        :param node: the identifier of the variable in the symbol table 
                     referring the node
        :type node: str

        :param component: the identifier of the variable in the 
                          symbol table referring the component
        :type component: str

        :param value: the identifier of the variable in the symbol table 
                      referring the value
        :type value: str
        """
        self.node = node
        self.component = component
        self.value = value


class DestroyComponent(Primitive):
    """
    Models the 'destroyComponent(node, component)' primitive.
    """
    
    def __init__(self, node, component):
        """
        Initializes the *DestroyComponent* object.

        :param node: the identifier of the variable in the symbol table 
                     referring the node
        :type node: str

        :param component: the identifier of the variable in the symbol table 
                          referring the component
        :type component: str
        """
        self.node = node
        self.component = component


class MisplaceNode(Primitive):
    """
    Models the 'misplaceNode(node, position)' primitive.
    """
    
    def __init__(self, node, position):
        """
        Initializes the *MisplaceNode* object.

        :param node: the identifier of the variable in the symbol table 
                     referring the node
        :type node: str

        :param position: the identifier of the list containing the coordinates 
        :type position: str
        """
        self.node = node
        self.position = position
    

class DestroyNode(Primitive):
    """
    Models the 'destroyNode(node)' primitive.
    """
    
    def __init__(self, node):
        """
        Initializes the *DestroyNode* object.

        :param node: the identifier of the variable in the symbol table 
                     referring the node
        :type node: str
        """
        self.node = node


class WriteField(Primitive):
    """
    Models the 'writeField(packet, path, source)' primitive.
    """

    def __init__(self, packet, path, source):
        """
        Initializes the *WriteField* object.

        :param packet: the identifier of the variable in the symbol table 
                       referring the packet
        :type packet: str
        
        :param path: the identifier of the variable in the symbol table 
                     referring the field
        :type path: str
        
        :param source: the identifier of the variable in the symbol table 
                       referring the source
        :type source: str
        """
        self.packet = packet
        self.path = path
        self.source = source


class ReadField(Primitive):
    """
    Models the 'readField(destination, packet, path)' primitive.
    """
    
    def __init__(self, destination, packet, path):
        """
        Initializes the *ReadField* object.

        :param packet: the identifier of the variable in the symbol table 
                       referring the destination
        :type packet: str

        :param packet: the identifier of the variable in the symbol table 
                       referring the packet
        :type packet: str
        
        :param path: the identifier of the variable in the symbol table 
                     referring the field
        :type path: str
        """
        self.destination = destination
        self.packet = packet
        self.path = path


class ForwardPacket(Primitive):
    """
    Models the 'forwardPacket(packet, delay, unit)' primitive.
    """
    
    def __init__(self, packet, delay, unit):
        """
        Initializes the *ForwardPacket* object.
        
        :param packet: the identifier of the variable in the symbol table 
                       referring the packet
        :type packet: str
        
        :param delay: the identifier of the variable in the symbol table 
                      referring the delay
        :type delay: str
        
        :param unit: the identifier of the variable in the symbol table 
                     referring the time unit
        :type unit: str
        """
        self.packet = packet
        self.delay = delay
        self.unit = unit


class CreatePacket(Primitive):
    """
    Models the 'createPacket(packet, protocol)' primitive.
    """

    def __init__(self, packet, protocol):
        """
        Initializes the *CreatePacket* object.
        
        :param packet: the identifier of the variable in the symbol table 
                       referring the packet
        :type packet: str
        
        :param protocol: the identifier of the variable in the symbol table 
                         referring the protocol
        :type protocol: str
        """
        self.packet = packet
        self.protocol = protocol


class InjectPacket(Primitive):
    """
    Models the 'injectPacket(packet, node, direction, delay, unit)' primitive.
    """

    def __init__(self, packet, node, direction, delay, unit):
        """
        Initializes the *InjectPacket* object.
        
        :param packet: the identifier of the variable in the symbol table 
                       referring the packet
        :type packet: str
        
        :param node: the identifier of the variable in the symbol table 
                     referring the node
        :type node: str
        
        :param direction: the identifier of the variable in the symbol table 
                          referring the direction
        :type direction: str
        
        :param delay: the identifier of the variable in the symbol table 
                      referring the delay
        :type delay: str
        
        :param unit: the identifier of the variable in the symbol table 
                     referring the time unit
        :type unit: str
        """
        self.packet = packet
        self.node = node
        self.direction = direction
        self.delay = delay
        self.unit = unit
        

class ClonePacket(Primitive):
    """
    Models the 'clonePacket(destination, source)' primitive.
    """
    
    def __init__(self, destination, source):
        """
        Initializes the *ClonePacket* object.
        
        :param destination: the identifier of the variable in the symbol table 
                            referring the destination packet
        :type destination: str
        
        :param souce: the identifier of the variable in the symbol table 
                      referring the source packet
        :type source: str
        """
        self.destination = destination
        self.source = source


class DropPacket(Primitive):
    """
    Models the 'dropPacket(packet)' primitive.
    """

    def __init__(self, packet):
        """
        Initializes the *DropPacket* object.
        
        :param packet: the identifier of the variable in the symbol table 
                       referring the packet
        :type packet: str
        """
        self.packet = packet


class Expression(Primitive):
    """
    Models an arithmetical expression.
    """
    
    def __init__(self, destination, expression):
        """
        Initializes the *Expression* object.
        
        :param destination: the identifier of the destination variable
        :type destination: str
        
        :param expression: the list of the identifiers composing the expression
        :type expression: list
        """
        self.destination = destination
        self.expression = copy.deepcopy(expression)


class Codeblock(metaclass=abc.ABCMeta):
    """
    Abstract model for codeblocks.
    """
    
    @abc.abstractmethod
    def __init__(self, symboltable, codeblocktable, *args):
        """
        Initializes the base object Codeblock.
        
        :param symboltable: the symbol table
        :type symboltable: model.types.SymbolTable
        
        :param codeblocktable: the codeblock table
        :type codeblocktable: model.statements.CodeblockTable
        """
        self.symboltable = copy.deepcopy(symboltable)
        self.codeblocktable = copy.deepcopy(codeblocktable)


class Scenario(Codeblock):
    """
    The scenario is made by a symbol table and a set of compound attacks.
    """
    
    def __init__(self, symboltable, codeblocktable):
        """
        Initializes the Scenario object.
        
        :param symboltable: the symbol table 
        :type symboltable: model.types.SymbolTable
        
        :param codeblocktable: the codeblock table
        :type codeblocktable: model.statements.CodeblockTable
        """
        super(Scenario, self).__init__(symboltable, codeblocktable)


class Compound(Codeblock):
    """
    The compound attack is made by a symbol table and a set of simple attacks.
    It starts at the given time.
    """
    
    def __init__(self, symboltable, codeblocktable, time, unit):
        """
        Initializes the Compound object.
        
        :param symboltable: the symbol table 
        :type symboltable: model.types.SymbolTable
        
        :param codeblocktable: the codeblock table
        :type codeblocktable: model.statements.CodeblockTable
        
        :param time: the identifier that refers the variable containing the starting time
        :type time: str
        
        :param unit: the identifier that refers the variable containing the measure unit
        :type unit: str
        """
        super(Compound, self).__init__(symboltable, codeblocktable)
        self.time = time
        self.unit = unit


class Once(Codeblock):
    """
    The once attack is made by a symbol table and a set of primitives.
    """
    
    def __init__(self, symboltable, codeblocktable):
        """
        Initializes the Once object.
        
        :param symboltable: the symbol table 
        :type symboltable: model.types.SymbolTable
        
        :param codeblocktable: the codeblock table
        :type codeblocktable: model.statements.CodeblockTable
        """
        super(Once, self).__init__(symboltable, codeblocktable)


class Periodic(Codeblock):
    """
    The periodic attack is made by a symbol table and a set of primitives.
    Is repeats itself periodically.
    """

    def __init__(self, symboltable, codeblocktable, period, unit):
        """
        Initializes the Periodic object.
        
        :param symboltable: the symbol table 
        :type symboltable: model.types.SymbolTable
        
        :param codeblocktable: the codeblock table
        :type codeblocktable: model.statements.CodeblockTable
        
        :param period: the identifier that refers the variable containing the period
        :type period: str
        
        :param unit: the identifier that refers the variable containing the measure unit
        :type unit: str
        """
        super(Periodic, self).__init__(symboltable, codeblocktable)
        self.period = period
        self.unit = unit


class Conditional(Codeblock):
    """
    The conditional attack is made by a symbol table and a set of primitives.
    It takes place when a packet of a target node matches the filter.
    """
    
    def __init__(self, symboltable, codeblocktable, nodes, filter):
        """
        Initializes the Periodic object.
        
        :param symboltable: the symbol table 
        :type symboltable: model.types.SymbolTable
        
        :param codeblocktable: the codeblock table
        :type codeblocktable: model.statements.CodeblockTable
        
        :param nodes: the identifier that refers the list containing the target nodes
        :type nodes: str
        
        :param filter: the identifier that refers the filter
        :type filter: str
        """
        super(Conditional, self).__init__(symboltable, codeblocktable)
        self.nodes = nodes
        self.filter = filter


class CodeblockTable(object):
    """
    A codeblock table that supports ADL codelbocks.
    """
    
    def __init__(self, scope):
        """
        Initializes the CodeblockTable object.
        
        :param self: the reference to the instance
        :type self: model.statements.CodeblockTable
        
        :param scope: the scope scope of the codeblock table
        :type scope: int
        
        :param codeblocks: the list of codeblocks
        :type codeblocks: list
        """
        if scope < 0:
            raise ValueError("Negative scope passed")
        self.scope = scope
        self.codeblocks = []


    def clear(self):
        """
        Clears the codeblock table.
        
        :param self: the reference to the instance
        :type self: model.statements.CodeblockTable
        """
        del self.codeblocks[:]

    
    def append(self, codeblock):
        """
        Appends the given codeblock to the list containing codeblocks.
        
        :param self: the reference to the instance
        :type self: model.statements.CodeblockTable
        
        :param codeblock: the codeblock
        :type codeblock: model.statements.Codeblock
                         model.statements.Primitive
        """
        if not codeblock:
            raise ValueError("None codeblock passed")
        self.codeblocks.append(codeblock)


class CodeblockHandler(object):
    """
    A multi-scope codeblock handler.
    """
    
    def __init__(self, scopes):
        """
        Initializes the CodeblockHandler object. Each instance owns a dictionary 
        that contains a codeblock table (value) per scope (key).
        
        :param self: the reference to the instance
        :type self: model.statements.CodeblockHandler
        
        :param scopes: the number of scopes
        :type scopes: int
        """
        if scopes < 0 :
            raise ValueError("scopes cannot be negative")
        self.scope_codeblocktable_dict = {}
        for scope in range(0, scopes):
            self.scope_codeblocktable_dict[scope] = CodeblockTable(scope)        

    def dump(self):
        """
        Dumps all the codeblock tables
        """
        self.scope_codeblocktable_dict.clear()

    def clear(self, scope):
        """
        Clears the codeblcok table related to the given scope.
        
        :param self: the reference to the instance
        :type self: model.statements.CodeblockTable

        :param scope: the scope
        :type scope: int
        """
        if scope not in self.scope_codeblocktable_dict:
            raise ValueError("out of scope")
        self.scope_codeblocktable_dict[scope].clear()
   
    def append(self, scope, codeblock):
        """
        Appends the given codeblock to the given scope.
        
        :param self: the reference to the instance
        :type self: model.statements.CodeblockTable

        :param scope: the scope
        :type scope: int
        
        :param codeblock: the codeblock
        :type codeblock: model.statements.Codeblock
                         model.statements.Primitive
        """
        if scope not in self.scope_codeblocktable_dict:
            raise ValueError("out of scope")
        if not codeblock:
            raise ValueError("codeblock passed cannot be None")
        self.scope_codeblocktable_dict[scope].append(codeblock)
