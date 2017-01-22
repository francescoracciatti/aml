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
    Builds the list of the reserved keywords.
    
    :return: the list of the reserved keywords
    """
    reserved = []
    reserved += Type.reserved()
    reserved += Primitive.reserved() 
    reserved += Statement.reserved()
    reserved += Accessor.reserved() 
    reserved += WellKnown.reserved()
    return reserved


def tokens():
    """
    Builds the list of the tokens.
    
    :return: the list of the tokens
    """
    tokens = []
    tokens += Type.tokens()
    tokens += Primitive.tokens() 
    tokens += Statement.tokens()
    tokens += Accessor.tokens() 
    tokens += WellKnown.tokens()
    return tokens


def view():
    """
    Builds the dictionary of the ADL keywords.
    
    :return: the dictionary of the ADL keywords
    """
    return {
        **Type.view(),
        **Primitive.view(),
        **Statement.view(),
        **Accessor.view(),
        **WellKnown.view()
    }


def rview():
    """
    Builds the reverse dictionary of the ADL keywords.
    
    :return: the reverse dictionary of the ADL keywords
    """
    return {
        **Type.rview(),
        **Primitive.rview(),
        **Statement.rview(),
        **Accessor.rview(),
        **WellKnown.rview()
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
    def reserved(cls):
        """
        Builds the list of the reserved keywords.
        
        :return: the list of the reserved keywords
        """
        return _reserved(cls)
        
    @classmethod
    def tokens(cls):
        """
        Builds the list of the tokens.
        
        :return: the list of the tokens
        """
        return _tokens(cls)
    
    @classmethod
    def view(cls):
        """
        Builds the dictionary that represents the class.

        :return: the dictionary that represents the class
        """
        return _view(cls)


    @classmethod
    def rview(cls):
        """
        Builds the reverse dictionary that represents the class.

        :return: the reverse dictionary that represents the class
        """
        return _rview(cls)



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
    def reserved(cls):
        """
        Builds the list of the reserved keywords.
        
        :return: the list of the reserved keywords
        """
        return _reserved(cls)
        
    @classmethod
    def tokens(cls):
        """
        Builds the list of the tokens.
        
        :return: the list of the tokens
        """
        return _tokens(cls)
    
    @classmethod
    def view(cls):
        """
        Builds the dictionary that represents the class.

        :return: the dictionary that represents the class
        """
        return _view(cls)


    @classmethod
    def rview(cls):
        """
        Builds the reverse dictionary that represents the class.

        :return: the reverse dictionary that represents the class
        """
        return _rview(cls)


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
    def reserved(cls):
        """
        Builds the list of the reserved keywords.
        
        :return: the list of the reserved keywords
        """
        return _reserved(cls)
        
    @classmethod
    def tokens(cls):
        """
        Builds the list of the tokens.
        
        :return: the list of the tokens
        """
        return _tokens(cls)
    
    @classmethod
    def view(cls):
        """
        Builds the dictionary that represents the class.

        :return: the dictionary that represents the class
        """
        return _view(cls)


    @classmethod
    def rview(cls):
        """
        Builds the reverse dictionary that represents the class.

        :return: the reverse dictionary that represents the class
        """
        return _rview(cls)


@enum.unique
class Accessor(enum.Enum):
    """
    ADL accessors.
    """
    MATCHING = 'matching'
    FOR = 'for'
    IN = 'in'

    @classmethod
    def reserved(cls):
        """
        Builds the list of the reserved keywords.
        
        :return: the list of the reserved keywords
        """
        return _reserved(cls)
        
    @classmethod
    def tokens(cls):
        """
        Builds the list of the tokens.
        
        :return: the list of the tokens
        """
        return _tokens(cls)
    
    @classmethod
    def view(cls):
        """
        Builds the dictionary that represents the class.

        :return: the dictionary that represents the class
        """
        return _view(cls)


    @classmethod
    def rview(cls):
        """
        Builds the reverse dictionary that represents the class.

        :return: the reverse dictionary that represents the class
        """
        return _rview(cls)


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
    def reserved(cls):
        """
        Builds the list of the reserved keywords.
        
        :return: the list of the reserved keywords
        """
        return _reserved(cls)
        
    @classmethod
    def tokens(cls):
        """
        Builds the list of the tokens.
        
        :return: the list of the tokens
        """
        return _tokens(cls)
    
    @classmethod
    def view(cls):
        """
        Builds the dictionary that represents the class.

        :return: the dictionary that represents the class
        """
        return _view(cls)


    @classmethod
    def rview(cls):
        """
        Builds the reverse dictionary that represents the class.

        :return: the reverse dictionary that represents the class
        """
        return _rview(cls)


def _reserved(cls):
    """
    Builds the list of the reserved keywords of an enum.Enum class.
        
    :return: the list of the reserved keywords
    """
    if not isinstance(cls, enum.EnumMeta):
        raise TypeError(str(cls.__class__.__name__) + " not supported")
    reserved = []
    for e in cls:
        reserved.append(e.value)
    return reserved


def _tokens(cls):
    """
    Builds the list of the names of an enum.Enum class.
        
    :return: the list of the reserved keywords
    """
    if not isinstance(cls, enum.EnumMeta):
        raise TypeError(str(cls.__class__.__name__) + " not supported")
    tokens = []
    for e in cls:
        tokens.append(e.name)
    return tokens


def _view(cls):
    """
    Builds the dictionary mapping the names with the related values of an enum.Enum class. 
    
    :returns: the dictionary mapping the reserved keywords with the releated tokens
    """
    if not isinstance(cls, enum.EnumMeta):
        raise TypeError(str(cls.__class__.__name__) + " not supported")
    view = {}
    for e in cls:
       view[e.name] = e.value
    return view


def _rview(cls):
    """
    Builds the reverse dictionary mapping the names with the related values of an enum.Enum class. 
    
    :returns: the dictionary mapping the reserved keywords with the releated tokens
    """
    if not isinstance(cls, enum.EnumMeta):
        raise TypeError(str(cls.__class__.__name__) + " not supported")
    rview = {}
    for e in cls:
       rview[e.value] = e.name
    return rview
    
    
