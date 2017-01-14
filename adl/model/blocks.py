# -----------------------------------------------------------------------------
# blocks.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module contains the model of the ADL blocks.
# -----------------------------------------------------------------------------


from abc import ABCMeta, abstractmethod
import copy


class Model(metaclass=ABCMeta):
    """
    Abstract model for attacks.
    """
    
    @abstractmethod
    def __init__(self, *args):
        pass


class Attack(metaclass=ABCMeta):
    """
    Models an abstract attack.
    """
    
    @abstractmethod
    def __init__(self, *args):
        pass


class Codeblock(metaclass=ABCMeta):
    """
    Models an abstract codeblock.
    """
    
    @abstractmethod
    def __init__(self, *args):
        pass


class Scenario(Model):
    """
    Models the scenario.
    
    :param compounds: the list of compound attacks
    :type compounds: list
    """
    
    def __init__(self, compounds):
        self.compounds = copy.deepcopy(compounds)


class AttackCompound(Attack):
    """
    A compound attack is made by a list of simple attacks.
    """
    
    def __init__(self, time, unit, codeblock):
        """
        Initializes the *AttackCompound* object.
        
        :param time: the starting time of the compound attack
        :type time: str

        :param unit: the unit of time
        :type unit: str
        
        :param codeblock: the codeblock of the compound attack
        :type codeblock: CodeblockAttackCompound
        """

        self.time = time
        self.unit = unit
        self.codeblock = copy.deepcopy(codeblock)


class CodeblockAttackCompound(Codeblock):
    """
    The codeblock of a compound attack is made by a symbol table 
    and a list of simple attacks.
    """
    
    def __init__(self, symbols, attacks):
        """
        Initializes the *CodeblockAttackCompound* object.

        :param symbols: the symbol table
        :type symbols: SymbolTable
        
        :param attacks: the list of simple attacks
        :type attacks: list
        """

        self.symbols = copy.deepcopy(symbols)
        self.attacks = copy.deepcopy(attacks)


class AttackOnce(Attack):
    """
    The once attack is a simple attack that take place once.
    """
    
    def __init__(self, codeblock):
        """
        Initializes the *AttackOnce* object.
        
        :param codeblock: the codeblock of the once attack
        :type codeblok: CodeblockAttackOnce
        """
        self.codeblock = copy.deepcopy(codeblock)


class CodeblockAttackOnce(Codeblock):
    """
    The codeblock of an once attack in made by a list of actions 
    and symbol tables.
    """

    def __init__(self, symbols, actions):
        """
        Initializes the *CodeblockAttackOnce* object.

        :param symbols: the symbol table
        :type symbols: SymbolTable
        
        :param actions: the list of actions composing the attack
        :type actions: list
        """

        self.symbols = copy.deepcopy(symbols)        
        self.actions = copy.deepcopy(actions)


class AttackPeriodic(Attack):
    """
    The periodic attack is an attack that takes place periodically.
    """
    
    def __init__(self, period, unit, codeblock):
        """
        Initializes the *AttackPeriodic* object.
        
        :param period: the period
        :type period: str
        
        :param unit: the unit of time
        :type unit: str

        :param codeblock: the codeblock of the periodic attack
        :type codeblok: CodeblockAttackPeriodic
        """
        
        self.period = period
        self.unit = unit
        self.codeblock = copy.deepcopy(codeblock)

  
class CodeblockAttackPeriodic(Codeblock):
    """
    The codeblock of a periodic attack is made by a list of actions 
    and symbol tables.
    """
    
    def __init__(self, symbols, actions):
        """
        Initializes the *CodeblockAttackPeriodic* object.
  
        :param symbols: the symbol table
        :type symbols: SymbolTable
      
        :param actions: the list of actions composing the attack
        :type actions: list
        """

        self.symbols = copy.deepcopy(symbols)        
        self.actions = copy.deepcopy(actions)
    


class AttackConditional(Attack):
    """
    The conditional attack is an attack that takes place when a condition
    is satisfied.
    """
    
    def __init__(self, nodes, codeblock):
        """
        Initializes the *AttackConditional* object.
        
        :param nodes: the identifier of the list containing the target nodes
        :type nodes: str
        
        :param codeblock: the codeblock of the periodic attack
        :type codeblok: CodeblockAttackConditional
        """
        
        self.nodes = nodes
        self.codeblock = copy.deepcopy(codeblock)
        

class CodeblockAttackConditional(Codeblock):
    """
    The codeblock of a conditional attack is made by a packet filter, 
    a list of actions and symbol tables.
    """

    def __init__(self, symbols, packet_filter, actions):
        """
        Initializes the *CodeblockAttackConditional* object.
        
        :param symbols: the symbol table
        :type symbols: SymbolTable
        
        :param packet_filter: the packet filter
        :type packet_filter: str
        
        :param actions: the list of actions composing the attack
        :type actions: list
        """

        self.symbols = copy.deepcopy(symbols)        
        self.packet_filter = packet_filter
        self.actions = copy.deepcopy(actions)
