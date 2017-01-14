# -----------------------------------------------------------------------------
# lexer.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module contains the lexer for ADL.
# -----------------------------------------------------------------------------

import ply.lex as lex

# Reserved keywords
reserved = {
    # Physical actions on nodes' components
    'disableComponent' : 'DISABLECOMPONENT',
    'deceiveComponent' : 'DECEIVECOMPONENT',
    'destroyComponent' : 'DESTROYCOMPONENT',
    # Physical actions on nodes
    'misplaceNode' : 'MISPLACENODE',
    'destroyNode' : 'DESTROYNODE',
    # Logical actions on packets' fields
    'writeField' : 'WRITEFIELD',
    'readField' : 'READFIELD',
    # Logical actions on packets
    'forwardPacket' : 'FORWARDPACKET',
    'createPacket' : 'CREATEPACKET',
    'injectPacket' : 'INJECTPACKET',
    'clonePacket' : 'CLONEPACKET',
    'dropPacket' : 'DROPPACKET',
    # Cycles
    'scenario' : 'SCENARIO',
    'packets' : 'PACKETS',
    'every' : 'EVERY',
    'nodes' : 'NODES',
    'from' : 'FROM',
    'once' : 'ONCE',
    'for' : 'FOR',
    # Structure accessors
    'in' : 'IN',
    'matching' : 'MATCHING',
    # Well known values
    'captured' : 'CAPTURED',
    'self' : 'SELF',
    'tx' : 'TX',
    'rx' : 'RX',
    'us' : 'US',
    'ms' : 'MS',
    's' : 'S',
    # Logical operators
    'and' : 'AND',
    'or' : 'OR',
    # Structures
    'variable' : 'VARIABLE',
    'packet' : 'PACKET',
    'filter' : 'FILTER',
    'list' : 'LIST',
}

# List of tokens
tokens = [
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
    # Punctuation
    'LROUND',
    'RROUND',
    'LBRACK',
    'RBRACK',
    'LCURVY',
    'RCURVY',
    'COMMA',
    # Types
    'STRING',
    'REAL',
    'INTEGER',
    # Identifiers
    'IDENTIFIER',
] + list(reserved.values())
 
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
        print("[Error] Error occurred during the parsing of a real number")
        raise SyntaxError
    return t


# Regex rule for signed integer number
def t_INTEGER(t):
    r'-?\d+'
    try:
	    t.value = int(t.value)
    except ValueError:
        print("[Error] Error occurred during the parsing of an integer number")
        raise SyntaxError
    return t

# Regex rule for identifiers
def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    # Checks if the identifier is a reserved keyword
    t.type = reserved.get(t.value,'IDENTIFIER')
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
    t.lexer.lineno += t.value.count("\n")
    pass    

# Regex rule for wrong statement or characters
def t_error(t):
    print('[Error] illegal character ' + str(t.value[0]))
    t.lexer.skip(1)
	
# Builds the lexer
lexer = lex.lex()
