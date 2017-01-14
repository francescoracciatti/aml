# -----------------------------------------------------------------------------
# actions.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module contains the model for the ADL actions.
# -----------------------------------------------------------------------------

from abc import ABCMeta, abstractmethod
import copy


class Action(metaclass=ABCMeta):
    """
    Abstract base class for Actions.
    """

    @abstractmethod
    def __init__(self, *args):
        pass


class DisableComponent(Action):
    """
    Models the 'disableComponent(node, component)' action.
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


class DeceiveComponent(Action):
    """
    Models the 'deceiveComponent(node, component, value)' action.
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


class DestroyComponent(Action):
    """
    Models the 'destroyComponent(node, component)' action.
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


class MisplaceNode(Action):
    """
    Models the 'misplaceNode(node, position)' action.
    """
    
    def __init__(self, node, position):
        """
        Initializes the *MisplaceNode* object.

        :param node: the identifier of the variable in the symbol table 
                     referring the node
        :type node: str

        :param component: the identifier of the variable in the symbol table 
                          referring the position
        :type component: str
        """
        self.node = node
        self.position = position
    

class DestroyNode(Action):
    """
    Models the 'destroyNode(node)' action.
    """
    
    def __init__(self, node):
        """
        Initializes the *DestroyNode* object.

        :param node: the identifier of the variable in the symbol table 
                     referring the node
        :type node: str
        """

        self.node = node


class WriteField(Action):
    """
    Models the 'writeField(packet, path, source)' action.
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


class ReadField(Action):
    """
    Models the 'readField(destination, packet, path)' action.
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


class ForwardPacket(Action):
    """
    Models the 'forwardPacket(packet, delay, unit)' action.
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


class CreatePacket(Action):
    """
    Models the 'createPacket(packet, protocol)' action.
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


class InjectPacket(Action):
    """
    Models the 'injectPacket(packet, node, direction, delay, unit)' action.
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
        

class ClonePacket(Action):
    """
    Models the 'clonePacket(destination, source)' action.
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


class DropPacket(Action):
    """
    Models the 'dropPacket(packet)' action.
    """

    def __init__(self, packet):
        """
        Initializes the *DropPacket* object.
        
        :param packet: the identifier of the variable in the symbol table 
                       referring the packet
        :type packet: str
        """
        
        self.packet = packet


class Expression(Action):
    """
    Models an arithmetical expression.
    """
    
    def __init__(self, destination, rpn):
        """
        Initializes the *Expression* object.
        
        :param destination: the identifier of the destination variable
        :type destination: str
        
        :param rpn: the arithmetical expression represented in rpn order
        :type rpn: list
        """
        self.destination = destination
        self.rpn = copy.deepcopy(rpn)
        

