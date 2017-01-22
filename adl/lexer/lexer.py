# -----------------------------------------------------------------------------
# lexer.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module contains the lexer.
# -----------------------------------------------------------------------------

import lexer.keywords as keywords
import ply.lex as lex


# Dict of the ADL reserved keywords
reserved = keywords.rview()

# Tuple of generic language operands
operands = (
    # Basic yypes
    'STRING',
    'REAL',
    'INTEGER',
    # Identifiers
    'IDENTIFIER',
)

# Tuple of generic language operators and operators
operators = (
    # Compound assignment operators
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    'MODASSIGN',
    # Comparison operators
    'NOTEQUALTO',
    'EQUALTO',
    'GREQTHN',
    'LSEQTHN',
    'GRTHN',
    'LSTHN',
    # Basic assignment operator
    'ASSIGN',
    # Basic operators
    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'MOD',
    'EXP',
    # Logical operators
    'LAND',
    'LOR',
    # Punctuation
    'LROUND',
    'RROUND',
    'LBRACK',
    'RBRACK',
    'LCURVY',
    'RCURVY',
    'COMMA',
)

# List of the tokens
tokens = keywords.tokens() + list(operands) + list(operators)

# Regex rules for compound assignment operators
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_MODASSIGN = r'%='
# Regex rules for comparison operators
t_NOTEQUALTO = r'!='
t_EQUALTO = r'=='
t_GREQTHN = r'>='
t_LSEQTHN = r'<='
t_GRTHN = r'>'
t_LSTHN = r'<'
# Regex rule for basic assignment operator
t_ASSIGN = r'='
# Regex rules for basic operators
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_EXP = r'\*\*'
# Logical operators
t_LAND = r'\&\&'
t_LOR = r'\|\|'
# Regex rules for punctuation
t_LROUND = r'\('
t_RROUND = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LCURVY = r'\{'
t_RCURVY = r'\}'
t_COMMA = r'\,'
# Regex rule for string
t_STRING = r'\"([^\\"]|(\\.))*\"'


# Regex rule for signed real number
def t_REAL(t):
    r'-?\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        raise SyntaxError("real number badly defined")
    return t


# Regex rule for signed integer number
def t_INTEGER(t):
    r'-?\d+'
    try:
	    t.value = int(t.value)
    except ValueError:
        raise SyntaxError("integer number badly defined")
    return t


# Regex rule for identifiers
def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    # Checks if the identifier is a reserved keyword
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


# Regex rule to ignore tab occurrences
t_ignore = " \t"


# Regex rule to ignore comments
def t_comment(t):
    r'\#.*'
    pass


# Regex rule to increment the line counter when new lines occur
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')
    pass    


# Regex rule for wrong statement or characters
def t_error(t):
    raise SyntaxError("illegal character " + str(t.value[0]))
    # TODO check if the fix does work and remove the old code below
    #print("[Error] illegal character " + str(t.value[0]))
    #t.lexer.skip(1)
	
	
# Builds the lexer
lexer = lex.lex()
