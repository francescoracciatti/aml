# -----------------------------------------------------------------------------
# aml.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module provides the AML parser.
# -----------------------------------------------------------------------------

import ply.yacc as yacc
from lexer.lexer import *
from parser.parser import *

class AML(object):
    """
    AML parser and interpreter.
    """
    
    @staticmethod
    def parse(source):
        """
        Parses the source string and builds the object representing the scenario.
        """
        # Builds the lexer object
        lexer = lex.lex()
        # Parses the source file
        parser = yacc.yacc(start = 'entry')
        aml = parser.parse(source, lexer=lexer)
        parser.restart()
        return aml
        
        
    @staticmethod
    def intepret(aml, type):
        """
        Interprets the aml source string.
        """
        raise NotImplementedError("not implemented yet")
        
        
        
        
        
        
        
        
        
        
        
