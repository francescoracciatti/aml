# -----------------------------------------------------------------------------
# parser.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module contains the grammar rules for the ADL parser.
# -----------------------------------------------------------------------------

import lexer.lexer as adllexer
import model.types as adltypes
import model.statements as adlstatements


# -----------------------------------------------------------------------------
# Support structures used to store objects during the parsing.
# -----------------------------------------------------------------------------

# The number of scopes
scopes = 3

# The symbol handler
symbolhandler = adltypes.SymbolHandler(scopes)

# The codeblock handler
codeblockhandler = adlstatements.CodeblockHandler(scopes)

# The list of temporary objects to be stored inside the symbolhandler
temporaries = []

# -----------------------------------------------------------------------------
# General parsing rule precedence and parsing entry point.
# -----------------------------------------------------------------------------

# Parsing rules precedence
precedence = (
    ('left','ADD','SUB'),
    ('left','MUL','DIV'),
    ('left', 'EXP'),
    ('right', 'ASSIGN')
    #('right','UMINUS', 'ASSIGN'),
)

# Grammar rule for the entry point
def p_entry(p):
    """
    entry : scenario
    """
    p[0] = p[1]


# -----------------------------------------------------------------------------
# Grammar rules for the scenario scope.
# -----------------------------------------------------------------------------

# Grammar rule for the statement scenario
def p_scenario(p):
    """
    scenario : SCENARIO LCURVY scenario_content RCURVY
    """
    symboltable = symbolhandler.scope_symboltable_dict[0]
    codeblocktable = codeblockhandler.scope_codeblocktable_dict[0]
    scenario = adlstatements.Scenario(symboltable, codeblocktable)
    symbolhandler.dump()
    codeblockhandler.dump()
    p[0] = scenario


# Grammar rule for the content of the scenario
def p_scenario_content(p):
    """
    scenario_content : scenario_variable_declaration
                     | scenario_variable_definition
                     | scenario_packet_declaration
                     | scenario_filter_definition
                     | scenario_list_definition
                     | compound
                     | scenario_content scenario_content
    """


# Grammar rule for the declaration of a variable inside the scenario scope
def p_scenario_variable_declaration(p):
    """
    scenario_variable_declaration : VARIABLE IDENTIFIER
    """
    identifier = p[2]
    if not symbolhandler.declare(0, identifier, adltypes.Symbol.Type.VARIABLE):
        raise RuntimeError("cannot declare the variable - line " + str(p.lineno(1)))

# Grammar rule for the definition of a variale inside the scenario scope
def p_scenario_variable_definition(p):
    """
    scenario_variable_definition : variable_definition
    """
    store_temporaries(0)


# Grammar rule for the declaration of a packet inside the scenario scope
def p_scenario_packet_declaration(p):
    """
    scenario_packet_declaration : PACKET IDENTIFIER
    """
    identifier = p[2]
    if not symbolhandler.declare(0, identifier, adltypes.Symbol.Type.PACKET):
        raise RuntimeError("cannot declare the packet - line " + str(p.lineno(1)))


# Grammar rule for the definition of a filter inside the scenario scope
def p_scenario_filter_definition(p):
    """
    scenario_filter_definition : filter_definition
    """
    store_temporaries(0)


# Grammar rule for the definition of a list inside the scenario scope
def p_scenario_list_definition(p):
    """
    scenario_list_definition : list_definition
    """
    store_temporaries(0)


# -----------------------------------------------------------------------------
# Grammar rules for the compound scope.
# -----------------------------------------------------------------------------

# Grammar rule for compounds
def p_compound(p):
    """
    compound : FROM IDENTIFIER unit LCURVY RCURVY
    """
    identifier = p[2]
    if not symbolhandler.exist(scope - 1, identifier):
        raise RuntimeError("identifier not defined - line " + str(p.lineno(1)))
    obj = adltypes.Reserved(p[3])
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        symbolhandler.define(0, obj)

    # TODO TBI

    symbolhandler.clear(1)
    codeblockhandler.clear(1)


# Grammar rule for compounds
def p_compound(p):
    """
    compound : FROM INTEGER unit LCURVY RCURVY
             | FROM REAL unit LCURVY RCURVY
    """
    value = p[2]
    if value < 0:
        raise RuntimeError("time cannot be negative - line " + str(p.lineno(1)))
    obj = adltypes.AutoVariable(adltypes.Variable.Type.REAL, float(value))
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        temporaries.append(obj)
    obj = adltypes.Reserved(p[3])
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        symbolhandler.define(0, obj)
    
    # TODO TBI
    symbolhandler.clear(1)
    codeblockhandler.clear(1)


# -----------------------------------------------------------------------------
# Grammar rules for the attack scope.
# -----------------------------------------------------------------------------

# TODO TBI


# -----------------------------------------------------------------------------
# Grammar rules for the primitive statements.
# -----------------------------------------------------------------------------

# TODO TBI


# -----------------------------------------------------------------------------
# Grammar rule for compound, attacks and primitive parameters.
# -----------------------------------------------------------------------------

# Grammar rule for the measure unit
def p_unit(p):
    """
    unit : US
         | MS
         | S
    """
    p[0] = p[1]
    

# -----------------------------------------------------------------------------
# Grammar rule for the definition of variables.
# -----------------------------------------------------------------------------

# Grammar rule for the definition of a variale
def p_variable_definition(p):
    """
    variable_definition : variable_definition_integer
                        | variable_definition_string
                        | variable_definition_real
    """


# Grammar rule for the definition of a variable (integer)
def p_variable_definition_integer(p):
    """
    variable_definition_integer : VARIABLE IDENTIFIER ASSIGN INTEGER
    """
    identifier = p[2]
    if symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("identifier already defined - line " + str(p.lineno(1)))        
    value = p[4]
    obj = adltypes.Variable(identifier, adltypes.Variable.Type.INTEGER, value)
    temporaries.append(obj)
    

# Grammar rule for the definition of a variable (string)
def p_variable_definition_string(p):
    """
    variable_definition_string : VARIABLE IDENTIFIER ASSIGN STRING
    """
    identifier = p[2]
    value = p[4]
    obj = adltypes.Variable(identifier, adltypes.Variable.Type.STRING, value)
    temporaries.append(obj)


# Grammar rule for the definition of a variable (real)
def p_variable_definition_real(p):
    """
    variable_definition_real : VARIABLE IDENTIFIER ASSIGN REAL
    """
    identifier = p[2]
    if symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("identifier already defined - line " + str(p.lineno(1)))        
    value = p[4]
    obj = adltypes.Variable(identifier, adltypes.Variable.Type.REAL, value)
    temporaries.append(obj)


# -----------------------------------------------------------------------------
# Grammar rule for the definition of filters.
# -----------------------------------------------------------------------------

# Grammar rule for the definition of a filter
def p_filter_definition(p):
    """
    filter_definition : FILTER IDENTIFIER ASSIGN filter_content
    """
    identifier = p[2]
    if symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("identifier already defined - line " + str(p.lineno(1)))
    flattened = list(flatten(p[4]))
    obj = adltypes.Filter(identifier, flattened)
    temporaries.append(obj)    


# Grammar rule for a filter made of compound elements
def p_filter_content_rounds(p):
    """
    filter_content : LROUND filter_content RROUND
    """
    p[0] = p[2]


# Grammar rule for a filter made of compound elements
def p_filter_content_compound(p):
    """
    filter_content : filter_content filter_logical_operator filter_content
    """
    p[0] = [p[1], p[3], p[2]]


# Grammar rule for a filter made of compound elements
def p_filter_content_compound_direct(p):
    """
    filter_content : filter_basic_element filter_logical_operator filter_content
    """
    p[0] = [p[1], p[3], p[2]]


# Grammar rule for a filter made of compound elements
def p_filter_content_compound_reverse(p):
    """
    filter_content : filter_content filter_logical_operator filter_basic_element
    """
    p[0] = [p[1], p[3], p[2]]


# Grammar rule for a filter made of a couple of elements
def p_filter_content_couple(p):
    """
    filter_content : filter_basic_element filter_logical_operator filter_basic_element
    """
    p[0] = [p[1], p[3], p[2]]


# Grammar rule for a filter made of a single basic element
def p_filter_content_mono(p):
    """
    filter_content : filter_basic_element
    """
    p[0] = p[1]


# Grammar rule for the basic element of filters
def p_filter_basic_element(p):
    """
    filter_basic_element : filter_operand filter_comparison_operator filter_operand
    """
    p[0] = [p[1], p[3], p[2]]
    

# Grammar rule for the filter operands
def p_filter_operand_value_integer(p):
    """
    filter_operand : INTEGER
    """
    value = p[1]
    obj = adltypes.AutoVariable(adltypes.Variable.Type.INTEGER, value)
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        temporaries.append(obj)
    p[0] = obj.identifier

# Grammar rule for the filter operands
def p_filter_operand_value_string(p):
    """
    filter_operand : STRING
    """
    value = p[1]
    obj = adltypes.AutoVariable(adltypes.Variable.Type.STRING, value)
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        temporaries.append(obj)
    p[0] = obj.identifier


# Grammar rule for the filter operands
def p_filter_operand_value_real(p):
    """
    filter_operand : REAL
    """
    value = p[1]
    obj = adltypes.AutoVariable(adltypes.Variable.Type.REAL, value)
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        temporaries.append(obj)
    p[0] = obj.identifier


# Grammar rule for the filter operands
def p_filter_operand_identifier(p):
    """
    filter_operand : IDENTIFIER
    """
    identifier = p[1]
    if not symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("identifier not declared - line " + str(p.lineno(1)))
    obj = symbolhandler.object(identifier)
    if obj.symboltype != adltypes.Symbol.Type.VARIABLE:
        raise RuntimeError("identifier does not refer a variable - line " + str(p.lineno(1)))
    if obj.variabletype == adltypes.Variable.Type.NONE:
        raise RuntimeError("identifier refers an uninitialized variable - line " + str(p.lineno(1)))
    p[0] = identifier


# Grammar rule for the filter comparison operators
def p_filter_comparison_operator(p):
    """
    filter_comparison_operator : NOTEQUALTO
                               | EQUALTO
                               | LSEQTHN
                               | GREQTHN
                               | LSTHN
                               | GRTHN
    """
    value = p[1]
    obj = adltypes.Reserved(value)
    identifier = obj.identifier
    if not symbolhandler.exist(scopes - 1, identifier):
        temporaries.append(obj)
    p[0] = identifier


# Grammar rule for the filter logical operators
def p_filter_logical_operator(p):
    """
    filter_logical_operator : LAND
                            | LOR
    """
    value = p[1]
    obj = adltypes.Reserved(value)
    identifier = obj.identifier
    if not symbolhandler.exist(scopes - 1, identifier):
        temporaries.append(obj)
    p[0] = [identifier]


# -----------------------------------------------------------------------------
# Grammar rule for the definition of lists.
# -----------------------------------------------------------------------------

# Grammar rule for the definition of lists
def p_list_definition(p):
    """
    list_definition : LIST IDENTIFIER ASSIGN LBRACK list_sequence RBRACK
    """
    identifier = p[2]
    if symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("identifier already defined - line " + str(p.lineno(1)))
    items = list(flatten(p[5]))
    obj = adltypes.List(identifier, items)
    temporaries.append(obj)    


# Grammar rule for a sequence of items
def p_list_sequence(p):
    """
    list_sequence : list_item COMMA list_sequence
    """
    p[0] = [p[1], p[3]]


# Grammar rule for a single item
def p_list_sequence_mono(p):
    """
    list_sequence : list_item
    """
    p[0] = [p[1]]


# Grammar rule for the list item
def p_list_item_integer(p):
    """
    list_item : INTEGER
    """
    value = p[1]
    obj = adltypes.AutoVariable(adltypes.Variable.Type.INTEGER, value)
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        temporaries.append(obj)
    p[0] = obj.identifier

# Grammar rule for the list item
def p_list_item_string(p):
    """
    list_item : STRING
    """
    value = p[1]
    obj = adltypes.AutoVariable(adltypes.Variable.Type.STRING, value)
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        temporaries.append(obj)
    p[0] = obj.identifier


# Grammar rule for the list item
def p_list_item_real(p):
    """
    list_item : REAL
    """
    value = p[1]
    obj = adltypes.AutoVariable(adltypes.Variable.Type.REAL, value)
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        temporaries.append(obj)
    p[0] = obj.identifier


# Grammar rule for the list item
def p_list_item_identifier(p):
    """
    list_item : IDENTIFIER
    """
    identifier = p[1]
    if not symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("identifier not declared - line " + str(p.lineno(1)))
    obj = symbolhandler.object(identifier)
    if obj.symboltype != adltypes.Symbol.Type.VARIABLE:
        raise RuntimeError("identifier does not refer a variable - line " + str(p.lineno(1)))
    if obj.variabletype == adltypes.Variable.Type.NONE:
        raise RuntimeError("identifier refers an uninitialized variable - line " + str(p.lineno(1)))
    p[0] = identifier
    

# -----------------------------------------------------------------------------
# Generic error handler.
# -----------------------------------------------------------------------------

# TODO TBI

# -----------------------------------------------------------------------------
# Helper functions.
# -----------------------------------------------------------------------------

def flatten(iterable):
    """
    Flattens multilevel lists and tuples.
    """
    for elm in iterable:
        if isinstance(elm, (list, tuple)):
            for relm in flatten(elm):
                yield relm
        else:
            yield elm


def store_temporaries(scope):
    """
    Stores the temporaries objects inside the symbol handler
    in the given scope.
    """
    for obj in temporaries:
        symbolhandler.define(0, obj)
    del temporaries[:]

