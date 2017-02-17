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
    AML parser.
    """
        
    @staticmethod
    def parse(source):
        """
        Parses the source string and builds the object representing the scenario.
        
        :param source: the string to be parsed
        :type source: str
        
        :return: the scenario
        """
        
        # Initializes the yacc
        yacc.yacc(debug = 0, start = 'entry')
        # Parses the source file
        return yacc.parse(source)
