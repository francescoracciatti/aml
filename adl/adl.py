# -----------------------------------------------------------------------------
# adl.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module provides the ADL parser.
# -----------------------------------------------------------------------------


import ply.yacc as yacc
from lexer.lexer import *
from parser.parser import *


class ADL(object):
    """
    ADL parser.
    """
        
    @staticmethod
    def parse(source):
        """
        Parses the source string and returns the scenario.
        
        :param source: the string to be parsed
        :type source: str
        
        :return: the scenario
        """
        
        # Initializes the yacc
        yacc.yacc(debug = 0, start = 'entry')
        # Parses the source file
        return yacc.parse(source)
