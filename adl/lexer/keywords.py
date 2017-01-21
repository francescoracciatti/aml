# -----------------------------------------------------------------------------
# keywords.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module contains the ADL keywords.
# -----------------------------------------------------------------------------

import enum


def reserved():
    """
    Builds the dictionary of the ADL reserved keywords.

    :return: the dictionary of the ADL reserved keywords
    """
    return {
        **Type.dictionary(),
        **Primitive.dictionary(),
        **Statement.dictionary(),
        **Accessor.dictionary(),
        **WellKnown.dictionary()
    }


@enum.unique
class Type(enum.Enum):
    """
    Types supported by ADL.
    """
    VARIABLE = 'variable'
    PACKET = 'packet'
    FILTER = 'filter'
    LIST = 'list'

    @classmethod
    def dictionary(cls):
        """
        Builds the dictionary that represents the class.

        :return: the dictionary that represents the class
        """
        return _dictionary(cls)
    
    
@enum.unique
class Primitive(enum.Enum):
    """
    ADL actions.
    """
    # Physical primitives on nodes' components
    DISABLECOMPONENT = 'disableComponent'
    DECEIVECOMPONENT = 'deceiveComponent'
    DESTROYCOMPONENT = 'destroyComponent'
    # Physical primitives on nodes
    MISPLACENODE = 'misplaceNode'
    DESTROYNODE = 'destroyNode'
    # Logical primitives on packets' fields
    WRITEFIELD = 'writeField'
    READFIELD = 'readField'
    # Logical primitives on packets
    FORWARDPACKET = 'forwardPacket'
    CREATEPACKET = 'createPacket'
    INJECTPACKET = 'injectPacket'
    CLONEPACKET = 'clonePacket'
    DROPPACKET = 'dropPacket'

    @classmethod
    def dictionary(cls):
        """
        Builds the dictionary that represents the class.

        :return: the dictionary that represents the class
        """
        return _dictionary(cls)


@enum.unique
class Statement(enum.Enum):
    """
    ADL statements.
    """
    SCENARIO = 'scenario'
    PACKETS = 'packets'
    EVERY = 'every'
    NODES = 'nodes'
    FROM = 'from'
    ONCE = 'once'

    @classmethod
    def dictionary(cls):
        """
        Builds the dictionary that represents the class.

        :return: the dictionary that represents the class
        """
        return _dictionary(cls)


@enum.unique
class Accessor(enum.Enum):
    """
    ADL accessors.
    """
    MATCHING = 'matching'
    FOR = 'for'
    IN = 'in'

    @classmethod
    def dictionary(cls):
        """
        Builds the dictionary that represents the class.

        :return: the dictionary that represents the class
        """
        return _dictionary(cls)


@enum.unique    
class WellKnown(enum.Enum):
    """
    ADL well known values.
    """
    CAPTURED = 'captured'
    SELF = 'self'
    TX = 'tx'
    RX = 'rx'
    US = 'us'
    MS = 'ms'
    S = 's'
    
    @classmethod
    def dictionary(cls):
        """
        Builds the dictionary that represents the class.

        :return: the dictionary that represents the class
        """
        return _dictionary(cls)


def _dictionary(cls):
    """
    Builds the dictionary of an enum.Enum class.
    For each enum in the class (derived from enum.Enum) it 
    uses its value as a dict's key and its name as a dict's value.
    
    :returns: the dictionary representing the class
    """
    dic = {}
    for entry in cls:
       dic[entry.value] = entry.name
    return dic

