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

# The list of temporary objects to be stored inside the handlers
temp_symbols = []

# -----------------------------------------------------------------------------
# General parsing rule precedence and parsing entry point.
# -----------------------------------------------------------------------------

# Parsing rules precedence
precedence = (
    ('left','ADD','SUB'),
    ('left','MUL','DIV'),
    ('left', 'EXP'),
    #('right', 'ASSIGN')
    ('right','UMINUS', 'ASSIGN'),
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
                     | compounds
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
    store_temp_symbols(0)


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
    store_temp_symbols(0)


# Grammar rule for the definition of a list inside the scenario scope
def p_scenario_list_definition(p):
    """
    scenario_list_definition : list_definition
    """
    store_temp_symbols(0)


# -----------------------------------------------------------------------------
# Grammar rules for the compound scope.
# -----------------------------------------------------------------------------

# Grammar rule for compounds
def p_compounds(p):
    """
    compounds : compound
              | compound compounds
    """


# Grammar rule for the compound scope
def p_compound_identifier(p):
    """
    compound : FROM IDENTIFIER unit LCURVY compound_content RCURVY
    """
    time_identifier = p[2]
    if not symbolhandler.exist(scopes - 1, time_identifier):
        raise RuntimeError("identifier not defined - line " + str(p.lineno(1)))
    obj = symbolhandler.object(time_identifier)
    if obj.variabletype not in (adltypes.Variable.Type.INTEGER, adltypes.Variable.Type.INTEGER):
        raise RuntimeError("identifier does not refer a number - line " + str(p.lineno(1)))
    obj = adltypes.Reserved(p[3])
    unit_identifier = obj.identifier
    if not symbolhandler.exist(scopes - 1, unit_identifier):
        symbolhandler.define(0, obj)
    # Builds the compound and stores it inside the codeblockhandler
    symboltable = symbolhandler.scope_symboltable_dict[1]
    codeblocktable = codeblockhandler.scope_codeblocktable_dict[1]
    compound = adlstatements.Compound(symboltable, codeblocktable, time_identifier, unit_identifier)
    codeblockhandler.append(0, compound)
    # Clears support structures
    symbolhandler.clear(1)
    codeblockhandler.clear(1)


# Grammar rule for the compound scope
def p_compound_value(p):
    """
    compound : FROM INTEGER unit LCURVY compound_content RCURVY
             | FROM REAL unit LCURVY compound_content RCURVY
    """
    time_value = p[2]
    if time_value < 0:
        raise RuntimeError("time cannot be negative - line " + str(p.lineno(1)))
    obj = adltypes.AutoVariable(adltypes.Variable.Type.REAL, float(time_value))
    time_identifier = obj.identifier
    if not symbolhandler.exist(scopes - 1, time_identifier):
        temp_symbols.append(obj)
    obj = adltypes.Reserved(p[3])
    unit_identifier = obj.identifier
    if not symbolhandler.exist(scopes - 1, unit_identifier):
        symbolhandler.define(0, obj)
    # Builds the compound and stores it inside the codeblockhandler
    symboltable = symbolhandler.scope_symboltable_dict[1]
    codeblocktable = codeblockhandler.scope_codeblocktable_dict[1]
    compound = adlstatements.Compound(symboltable, codeblocktable, time_identifier, unit_identifier)
    codeblockhandler.append(0, compound)
    # Clears support structures
    symbolhandler.clear(1)
    codeblockhandler.clear(1)


# Grammar rule for the content of compounds
def p_compound_content(p):
    """
    compound_content : compound_variable_declaration
                     | compound_variable_definition
                     | compound_packet_declaration
                     | compound_filter_definition
                     | compound_list_definition
                     | onces
                     | periodics
                     | conditionals
                     | compound_content compound_content
    """


# Grammar rule for the declaration of a variable inside the compound scope
def p_compound_variable_declaration(p):
    """
    compound_variable_declaration : VARIABLE IDENTIFIER
    """
    identifier = p[2]
    if not symbolhandler.declare(1, identifier, adltypes.Symbol.Type.VARIABLE):
        raise RuntimeError("cannot declare the variable - line " + str(p.lineno(1)))

# Grammar rule for the definition of a variale inside the compound scope
def p_compound_variable_definition(p):
    """
    compound_variable_definition : variable_definition
    """
    store_temp_symbols(1)


# Grammar rule for the declaration of a packet inside the compound scope
def p_compound_packet_declaration(p):
    """
    compound_packet_declaration : PACKET IDENTIFIER
    """
    identifier = p[2]
    if not symbolhandler.declare(1, identifier, adltypes.Symbol.Type.PACKET):
        raise RuntimeError("cannot declare the packet - line " + str(p.lineno(1)))


# Grammar rule for the definition of a filter inside the compound scope
def p_compound_filter_definition(p):
    """
    compound_filter_definition : filter_definition
    """
    store_temp_symbols(1)


# Grammar rule for the definition of a list inside the compound scope
def p_compound_list_definition(p):
    """
    compound_list_definition : list_definition
    """
    store_temp_symbols(1)


# -----------------------------------------------------------------------------
# Grammar rules for the once attack scope.
# -----------------------------------------------------------------------------

# Grammar rule for onces
def p_onces(p):
    """
    onces : once
          | once onces
    """


# Grammar rule for the once scope
def p_once(p):
    """
    once : ONCE LCURVY once_content RCURVY
    """
    #
    # Builds the compound and stores it inside the codeblockhandler
    symboltable = symbolhandler.scope_symboltable_dict[2]
    codeblocktable = codeblockhandler.scope_codeblocktable_dict[2]
    once = adlstatements.Once(symboltable, codeblocktable)
    codeblockhandler.append(1, once)
    # Clears support structures
    symbolhandler.clear(2)
    codeblockhandler.clear(2)


# Grammar rule for the content of once
def p_once_content(p):
    """
    once_content : once_variable_declaration
                 | once_variable_definition
                 | once_packet_declaration
                 | once_filter_definition
                 | once_list_definition
                 | once_primitives
                 | once_content once_content
    """


# Grammar rule for the declaration of a variable inside the compound scope
def p_once_variable_declaration(p):
    """
    once_variable_declaration : VARIABLE IDENTIFIER
    """
    identifier = p[2]
    if not symbolhandler.declare(2, identifier, adltypes.Symbol.Type.VARIABLE):
        raise RuntimeError("cannot declare the variable - line " + str(p.lineno(1)))

# Grammar rule for the definition of a variale inside the compound scope
def p_once_variable_definition(p):
    """
    once_variable_definition : variable_definition
    """
    store_temp_symbols(2)


# Grammar rule for the declaration of a packet inside the compound scope
def p_once_packet_declaration(p):
    """
    once_packet_declaration : PACKET IDENTIFIER
    """
    identifier = p[2]
    if not symbolhandler.declare(2, identifier, adltypes.Symbol.Type.PACKET):
        raise RuntimeError("cannot declare the packet - line " + str(p.lineno(1)))


# Grammar rule for the definition of a filter inside the compound scope
def p_once_filter_definition(p):
    """
    once_filter_definition : filter_definition
    """
    store_temp_symbols(2)


# Grammar rule for the definition of a list inside the compound scope
def p_once_list_definition(p):
    """
    once_list_definition : list_definition
    """
    store_temp_symbols(2)


# Grammar rule for the once primitives
def p_once_primitives(p):
    """
    once_primitives : primitive_disable_component
                    | primitive_deceive_component
                    | primitive_destroy_component
                    | primitive_misplace_node
                    | primitive_destroy_node
                    | primitive_write_field
                    | primitive_create_packet
                    | primitive_inject_packet
                    | primitive_clone_packet
                    | primitive_expression
    """


# -----------------------------------------------------------------------------
# Grammar rules for the periodic attack scope.
# -----------------------------------------------------------------------------

# Grammar rule for periodics
def p_periodics(p):
    """
    periodics : periodic
              | periodics periodics
    """
    # TODO TBI


# Grammar rule for the periodic scope
def p_periodic_identifier(p):
    """
    periodic : EVERY IDENTIFIER unit LCURVY RCURVY
    """
    # TODO TBI


# Grammar rule for the periodic scope
def p_periodic_value(p):
    """
    periodic : EVERY INTEGER unit LCURVY RCURVY
             | EVERY REAL unit LCURVY RCURVY
    """
    # TODO TBI


# TODO TBI


# -----------------------------------------------------------------------------
# Grammar rules for the conditional attack scope.
# -----------------------------------------------------------------------------

# Grammar rule for conditionals
def p_conditionals(p):
    """
    conditionals : conditional
                 | conditionals conditionals
    """
    # TODO TBI


# Grammar rule for the periodic scope
def p_conditional(p):
    """
    conditional : FOR NODES IN IDENTIFIER LCURVY FOR PACKETS MATCHING IDENTIFIER LCURVY RCURVY RCURVY
    """
    # TODO TBI


# TODO TBI


# -----------------------------------------------------------------------------
# Grammar rules for the primitive statements.
# -----------------------------------------------------------------------------

# Grammar rule for the primitive disableComponent
def p_primitive_disable_component(p):
    """
    primitive_disable_component : DISABLECOMPONENT LROUND node COMMA component RROUND
    """
    primitive = adlstatements.DisableComponent(p[3], p[5])
    codeblockhandler.append(2, primitive)


# Grammar rule for the primitive deceiveComponent
def p_primitive_deceive_component(p):
    """
    primitive_deceive_component : DECEIVECOMPONENT LROUND node COMMA component COMMA value RROUND
    """
    primitive = adlstatements.DeceiveComponent(p[3], p[5], p[7])
    codeblockhandler.append(2, primitive)


# Grammar rule for the primitive destroyComponent
def p_primitive_destroy_component(p):
    """
    primitive_destroy_component : DESTROYCOMPONENT LROUND node COMMA component RROUND
    """
    primitive = adlstatements.DestroyComponent(p[3], p[5])
    codeblockhandler.append(2, primitive)


# Grammar rule for the primitive misplaceNode
def p_primitive_misplace_node(p):
    """
    primitive_misplace_node : MISPLACENODE LROUND node COMMA position RROUND
    """
    primitive = adlstatements.MisplaceNode(p[3], p[5])
    codeblockhandler.append(2, primitive)


# Grammar rule for the primitive destroyNode
def p_primitive_destroy_node(p):
    """
    primitive_destroy_node : DESTROYNODE LROUND node RROUND
    """
    primitive = adlstatements.DestroyNode(p[3])
    codeblockhandler.append(2, primitive)


# Grammar rule for the primitive writeField
def p_primitive_write_field(p):
    """
    primitive_write_field : WRITEFIELD LROUND packet COMMA path COMMA source RROUND
    """
    primitive = adlstatements.WriteField(p[3], p[5], p[7])
    codeblockhandler.append(2, primitive)


# Grammar rule for the primitive readField
def p_primitive_read_field(p):
    """
    primitive_read_field : READFIELD LROUND destination COMMA packet COMMA path RROUND
    """
    primitive = adlstatements.ReadField(p[3], p[5], p[7])
    codeblockhandler.append(2, primitive)

# Grammar rule for the primitive forwardPacket
def p_primitive_forward_packet(p):
    """
    primitive_forward_packet : FORWARDPACKET LROUND packet COMMA delay COMMA unit RROUND
    """
    obj = adltypes.Reserved(p[7])
    unit_identifier = obj.identifier
    if not symbolhandler.exist(scopes - 1, unit_identifier):
        symbolhandler.define(2, obj)   
    primitive = adlstatements.ForwardPacket(p[3], p[5], unit_identifier)
    codeblockhandler.append(2, primitive)

    
# Grammar rule for the primitive createPacket
def p_primitive_create_packet(p):
    """
    primitive_create_packet : CREATEPACKET LROUND packet COMMA protocol RROUND
    """
    primitive = adlstatements.CreatePacket(p[3], p[5])
    codeblockhandler.append(2, primitive)


# Grammar rule for the primitive injectPacket
def p_primitive_inject_packet(p):
    """
    primitive_inject_packet : INJECTPACKET LROUND packet COMMA node COMMA direction COMMA delay COMMA unit RROUND
    """
    obj = adltypes.Reserved(p[11])
    unit_identifier = obj.identifier
    if not symbolhandler.exist(scopes - 1, unit_identifier):
        symbolhandler.define(2, obj)
    primitive = adlstatements.InjectPacket(p[3], p[5], p[7], p[9], unit_identifier)
    codeblockhandler.append(2, primitive)


# Grammar rule for the primitive clonePacket
def p_primitive_clone_packet(p):
    """
    primitive_clone_packet : CLONEPACKET LROUND packet COMMA packet RROUND
                           | CLONEPACKET LROUND packet COMMA captured RROUND
    """
    if p[3] == p[5]:
        raise RuntimeError("destination and source packets cannot match")
    primitive = adlstatements.ClonePacket(p[3], p[5])
    codeblockhandler.append(2, primitive)

# Grammar rule for the primitive dropPacket
def p_primitive_drop_packet(p):
    """
    primitive_drop_packet : CLONEPACKET LROUND packet RROUND
                          | CLONEPACKET LROUND CAPTURED RROUND
    """
    primitive = adlstatements.DropPacket(p[3])
    codeblockhandler.append(2, primitive)

# Grammar rule for the primitive Expression
def p_primitive_expression(p):
    """
    primitive_expression : expression_assign
    """

# -----------------------------------------------------------------------------
# Grammar rule for the definition of variables.
# -----------------------------------------------------------------------------

# Grammar rule for assignments in the expressions
def p_expression_assign(p):
    """
    expression_assign : IDENTIFIER ASSIGN expression
    """
    # Checks if the identifier exists
    identifier = p[1]
    if not symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("undefined identifier - line " + str(p.lineno(1)))
    # Checks if the identifier refers a variable
    obj = symbolhandler.object(identifier)
    if obj.symboltype != adltypes.Symbol.Type.VARIABLE:
        raise RuntimeError("the identifier does not refer a variable - line "+ str(p.lineno(1)))
    # Retrieves the expression (make it a list in case of single element)
    expression = [p[3]]
    # Evaluates the type of the expression
    expression = list(flatten(expression))
    if obj.variabletype == adltypes.Variable.Type.NONE:
        variabletype = get_expression_type(expression)
        symbolhandler.scope_symboltable_dict[2].identifier_object_dict[p[1]].variabletype = variabletype 
    else:
        if not check_expression_against_variabletype(expression, obj.variabletype):
            raise RuntimeError("cannot handle different types inside expressions - line "+ str(p.lineno(1)))
    # Builds the expression and appends it to the action list
    primitive = adlstatements.Expression(identifier, expression)
    codeblockhandler.append(2, primitive)


# Grammar rule for assignments in the expressions
def p_expression_operation_assign(p):
    """
    expression_assign : IDENTIFIER ADDASSIGN expression
                      | IDENTIFIER SUBASSIGN expression
                      | IDENTIFIER MULASSIGN expression
                      | IDENTIFIER DIVASSIGN expression
                      | IDENTIFIER MODASSIGN expression
    """
    # Checks if the identifier exists
    identifier = p[1]
    if not symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("undefined identifier - line " + str(p.lineno(1)))
    # Checks if the identifier refers a well defined variable
    obj = symbolhandler.object(identifier)
    if obj.symboltype != adltypes.Symbol.Type.VARIABLE:
        raise RuntimeError("the identifier does not refer a variable - line "+ str(p.lineno(1)))
    if obj.variabletype == adltypes.Variable.Type.NONE:
        raise RuntimeError("the identifier refers an uninitialized variable - line "+ str(p.lineno(1)))
    # Retrieves the expression (make it a list in case of single element)
    expression = [p[3]]
    # Checks the type against the operator
    expression = list(flatten(expression))
    variabletype = get_expression_type(expression)
    if variabletype == adltypes.Variable.Type.STRING:
        if p[2] != adllexer.BasicOperatorType.ADDASSIGN.value:
            raise RuntimeError("the operator does not support strings - line " + str(p.lineno(1)))
    # Defines the operator
    operator = None
    if p[2] == adllexer.BasicOperatorType.ADDASSIGN.value:
        operator = adltypes.Reserved(adllexer.BasicOperatorType.ADD.value)
    elif p[2] == adllexer.BasicOperatorType.SUBASSIGN.value:
        operator = adltypes.Reserved(adllexer.BasicOperatorType.SUB.value)
    elif p[2] == adllexer.BasicOperatorType.MULASSIGN.value:
        operator = adltypes.Reserved(adllexer.BasicOperatorType.MUL.value)
    elif p[2] == adllexer.BasicOperatorType.DIVASSIGN.value:
        operator = adltypes.Reserved(adllexer.BasicOperatorType.DIV.value)
    elif p[2] == adllexer.BasicOperatorType.MODASSIGN.value:
        operator = adltypes.Reserved(adllexer.BasicOperatorType.MOD.value)
    else:
        raise RuntimeError("operator not recognized (bug, should never happen) - line " + str(p.lineno(1)))
    if not symbolhandler.exist(scopes - 1, operator.identifier):
        symbolhandler.define(2, operator)
    expression = [expression, identifier, operator.identifier]
    expression = list(flatten(expression))
    # Builds the expression and appends it to the action list
    primitive = adlstatements.Expression(identifier, expression)
    codeblockhandler.append(2, primitive)


# Grammar rule for arithmetic operations in the expressions
def p_expression_binop(p):
    """
    expression : expression ADD expression
               | expression SUB expression
               | expression MUL expression
               | expression DIV expression
               | expression MOD expression
               | expression EXP expression
    """
    operator = adltypes.Reserved(p[2])
    if not symbolhandler.exist(scopes - 1, operator.identifier):
        symbolhandler.define(2, operator)
    rpn = [p[1], p[3], operator.identifier]
    expression = list(flatten(rpn))
    # Checks the type against the operator
    variabletype = get_expression_type(expression)
    if variabletype == adltypes.Variable.Type.STRING:
        if p[2] != adllexer.BasicOperatorType.ADD.value:
            raise RuntimeError("the operator does not support strings - line " + str(p.lineno(1)))
    p[0] = expression


# Grammar rule for the uminus in the expressions
def p_expression_uminus(p):
    """
    expression : SUB expression %prec UMINUS
    """
    expression = list(flatten(p[2]))
    variabletype = get_expression_type(expression)
    if variabletype == adltypes.Variable.Type.STRING:
        raise RuntimeError("the uminus cannot be applied to strings - line " + str(p.lineno(1)))
    value = -1
    variable = adltypes.AutoVariable(adltypes.Variable.Type.INTEGER, value)
    if not symbolhandler.exist(scopes - 1, variable.identifier):
        symbolhandler.define(2, variable)
    operator = adltypes.Reserved(adllexer.BasicOperatorType.MUL.value)
    if not symbolhandler.exist(scopes - 1, operator.identifier):
        symbolhandler.define(2, operator)
    expression = [expression, variable.identifier, operator.identifier]
    p[0] = expression


# Grammar rule for groups inside expressions
def p_expression_group(p):
    """
    expression : LROUND expression RROUND
    """
    p[0] = p[2]


# Grammar rule for integers inside expressions
def p_expression_integer(p):
    """
    expression : INTEGER
    """
    value = p[1]
    variable = adltypes.AutoVariable(adltypes.Variable.Type.INTEGER, value)
    if not symbolhandler.exist(scopes - 1, variable.identifier):
        symbolhandler.define(2, variable)
    p[0] = variable.identifier


# Grammar rule for strings inside expressions
def p_expression_string(p):
    """
    expression : STRING
    """
    value = p[1]
    variable = adltypes.AutoVariable(adltypes.Variable.Type.STRING, value)
    if not symbolhandler.exist(scopes - 1, variable.identifier):
        symbolhandler.define(2, variable)
    p[0] = variable.identifier
    

# Grammar rule for reals inside expressions
def p_expression_real(p):
    """
    expression : REAL
    """
    value = p[1]
    variable = adltypes.AutoVariable(adltypes.Variable.Type.REAL, value)
    if not symbolhandler.exist(scopes - 1, variable.identifier):
        symbolhandler.define(2, variable)
    p[0] = variable.identifier


# Grammar rule for the identifiers in the expressions
def p_expression_identifier(p):
    """
    expression : IDENTIFIER
    """
    identifier = p[1]
    # Checks if the identifier exists
    if not symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("undefined identifier - line " + str(p.lineno(1)))
    # Checks if the identifier refers a well defined variable
    variable = symbolhandler.object(identifier)
    if variable.symboltype != adltypes.Symbol.Type.VARIABLE:
        raise RuntimeError("the identifier does not refer a variable - line "+ str(p.lineno(1)))
    if variable.variabletype == adltypes.Variable.Type.NONE:
        raise RuntimeError("the variable is undefined - line "+ str(p.lineno(1)))
    p[0] = identifier


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


# Grammar rule for the node
def p_argument_node(p):
    """
    node : identifier_variable_defined
         | value_integer
         | value_string
         | value_real
    """
    p[0] = p[1]


# Grammar rule for the component
def p_argument_component(p):
    """
    component : identifier_variable_defined
              | value_integer
              | value_string
              | value_real
    """
    p[0] = p[1]


# Grammar rule for the component
def p_argument_value(p):
    """
    value : identifier_variable_defined
          | value_integer
          | value_string
          | value_real
    """
    p[0] = p[1]
    

# Grammar rule for the position
def p_argument_position(p):
    """
    position : identifier_list_defined
             | list_value
    """
    p[0] = p[1]


# Grammar rule for the packets
def p_argument_packet(p):
    """
    packet : IDENTIFIER
    """
    identifier = p[1]
    if not symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("identifier not defined - line " + str(p.lineno(1)))
    obj = symbolhandler.object(identifier)
    if obj.symboltype != adltypes.Symbol.Type.PACKET:
        raise RuntimeError("identifier does not refer a packet - line " + str(p.lineno(1)))
    p[0] = identifier


# Grammar rule for the path
def p_argument_path(p):
    """
    path : identifier_variable_defined
         | value_integer
         | value_string
         | value_real
    """
    p[0] = p[1]


# Grammar rule for the source
def p_argument_source(p):
    """
    source : identifier_variable_defined
           | value_integer
           | value_string
           | value_real
    """
    p[0] = p[1]


# Grammar rule for the destination
def p_argument_destination(p):
    """
    destination : IDENTIFIER
    """
    identifier = p[1]
    if not symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("identifier not defined - line " + str(p.lineno(1)))
    obj = symbolhandler.object(identifier)
    if obj.symboltype != adltypes.Symbol.Type.VARIABLE:
        raise RuntimeError("identifier does not refer a variable - line " + str(p.lineno(1)))
    p[0] = identifier


# Grammar rule for the destination
def p_argument_delay_reference(p):
    """
    delay : IDENTIFIER
    """
    identifier = p[1]
    if not symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("identifier not defined - line " + str(p.lineno(1)))
    obj = symbolhandler.object(identifier)
    if obj.symboltype != adltypes.Symbol.Type.VARIABLE:
        raise RuntimeError("identifier does not refer a variable - line " + str(p.lineno(1)))
    if obj.variabletype not in (adltypes.Variable.Type.INTEGER, adltypes.Variable.Type.REAL):
        raise RuntimeError("identifier does not refer a number - line " + str(p.lineno(1)))
    p[0] = identifier

    
def p_argument_delay_value(p):
    """
    delay : value_integer
          | value_real
    """
    p[0] = p[1]


# Grammar rule for the protocol
def p_argument_protocol_reference(p):
    """
    protocol : IDENTIFIER
    """
    identifier = p[1]
    if not symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("identifier not defined - line " + str(p.lineno(1)))
    obj = symbolhandler.object(identifier)
    if obj.symboltype != adltypes.Symbol.Type.VARIABLE:
        raise RuntimeError("identifier does not refer a variable - line " + str(p.lineno(1)))
    if obj.variabletype != adltypes.Variable.Type.STRING:
        raise RuntimeError("identifier does not refer a string - line " + str(p.lineno(1)))
    p[0] = identifier

    
# Grammar rule for the protocol
def p_argument_protocol_value(p):
    """
    protocol : value_string
    """
    p[0] = p[1]


# Grammar rule for the direction
def p_argument_direction(p):
    """
    direction : TX
              | RX
    """
    value = p[1]
    obj = adltypes.Reserved(value)
    identifier = obj.identifier
    if not symbolhandler.exist(scopes - 1, identifier):
        symbolhandler.define(2, obj)
    p[0] = identifier


# Grammar rule for the captured
def p_argument_captured(p):
    """
    captured : CAPTURED
    """
    value = p[1]
    obj = adltypes.Reserved(value)
    identifier = obj.identifier
    if not symbolhandler.exist(scopes - 1, identifier):
        symbolhandler.define(2, obj)
    p[0] = identifier


# Grammar rule for values passed as a reference
def p_argument_identifier_variable_defined(p):
    """
    identifier_variable_defined : IDENTIFIER
    """
    identifier = p[1]
    if not symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("identifier not declared - line " + str(p.lineno(1)))
    obj = symbolhandler.object(identifier)
    if obj.symboltype != adltypes.Symbol.Type.VARIABLE:
        raise RuntimeError("identifier does not refer a variable - line " + str(p.lineno(1)))
    if obj.variabletype == adltypes.Variable.Type.NONE:
        # TODO search for an expression inside this scope
        raise RuntimeError("identifier refers an uni variable - line " + str(p.lineno(1)))
    p[0] = identifier
   

# Grammar rule for a integer passed as a value
def p_argument_value_integer(p):
    """
    value_integer : INTEGER
    """
    value = p[1]
    obj = adltypes.AutoVariable(adltypes.Variable.Type.INTEGER, value)
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        symbolhandler.define(2, obj)
    p[0] = obj.identifier

# Grammar rule for a string passed as a value
def p_argument_value_string(p):
    """
    value_string : STRING
    """
    value = p[1]
    obj = adltypes.AutoVariable(adltypes.Variable.Type.STRING, value)
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        symbolhandler.define(2, obj)
    p[0] = obj.identifier


# Grammar rule for a real passed as a value
def p_argument_value_real(p):
    """
    value_real : REAL
    """
    value = p[1]
    obj = adltypes.AutoVariable(adltypes.Variable.Type.REAL, value)
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        symbolhandler.define(2, obj)
    p[0] = obj.identifier


# Grammar rule for lists passed as a reference
def p_argument_identifier_list_defined(p):
    """
    identifier_list_defined : IDENTIFIER
    """
    identifier = p[1]
    if not symbolhandler.exist(scopes - 1, identifier):
        raise RuntimeError("identifier not declared - line " + str(p.lineno(1)))
    obj = symbolhandler.object(identifier)
    if obj.symboltype != adltypes.Symbol.Type.LIST:
        raise RuntimeError("identifier does not refer a list - line " + str(p.lineno(1)))
    p[0] = identifier


# Grammar rule for lists passed as a reference
def p_argument_list_value(p):
    """
    list_value : LBRACK list_sequence RBRACK
    """
    items = list(flatten(p[2]))
    obj = adltypes.AutoList(items)
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        symbolhandler.define(2, obj)
    p[0] = obj.identifier


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
    temp_symbols.append(obj)
    

# Grammar rule for the definition of a variable (string)
def p_variable_definition_string(p):
    """
    variable_definition_string : VARIABLE IDENTIFIER ASSIGN STRING
    """
    identifier = p[2]
    value = p[4]
    obj = adltypes.Variable(identifier, adltypes.Variable.Type.STRING, value)
    temp_symbols.append(obj)


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
    temp_symbols.append(obj)


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
    temp_symbols.append(obj)    


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
        temp_symbols.append(obj)
    p[0] = obj.identifier

# Grammar rule for the filter operands
def p_filter_operand_value_string(p):
    """
    filter_operand : STRING
    """
    value = p[1]
    obj = adltypes.AutoVariable(adltypes.Variable.Type.STRING, value)
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        temp_symbols.append(obj)
    p[0] = obj.identifier


# Grammar rule for the filter operands
def p_filter_operand_value_real(p):
    """
    filter_operand : REAL
    """
    value = p[1]
    obj = adltypes.AutoVariable(adltypes.Variable.Type.REAL, value)
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        temp_symbols.append(obj)
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
        temp_symbols.append(obj)
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
        temp_symbols.append(obj)
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
    temp_symbols.append(obj)    


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
        temp_symbols.append(obj)
    p[0] = obj.identifier

# Grammar rule for the list item
def p_list_item_string(p):
    """
    list_item : STRING
    """
    value = p[1]
    obj = adltypes.AutoVariable(adltypes.Variable.Type.STRING, value)
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        temp_symbols.append(obj)
    p[0] = obj.identifier


# Grammar rule for the list item
def p_list_item_real(p):
    """
    list_item : REAL
    """
    value = p[1]
    obj = adltypes.AutoVariable(adltypes.Variable.Type.REAL, value)
    if not symbolhandler.exist(scopes - 1, obj.identifier):
        temp_symbols.append(obj)
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

# Generic error handler
def p_error(p):
    raise RuntimeError("wrong syntax for the token '" + p.value + "' - line " + str(p.lineno))


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


def store_temp_statements(scope):
    """
    Stores the temporaries statement inside the codeblock handler
    in the given scope.
    """
    for obj in temp_statements:
        codeblockhandler.define(scope, obj)
    del temp_statements[:]


def store_temp_symbols(scope):
    """
    Stores the temporaries symbols inside the symbol handler
    in the given scope.
    """
    for obj in temp_symbols:
        symbolhandler.define(scope, obj)
    del temp_symbols[:]


def get_expression_type(identifiers):
    """
    Gets the type of the objects referred by the given identifiers.
    
    :param identifiers: the list of the identifiers
    :type identifiers: list
    """
    # Checks if the expression is well formed
    items = list(identifiers)
    identifier = items[0]
    obj = symbolhandler.object(identifier)
    if obj.symboltype != adltypes.Symbol.Type.VARIABLE:
        raise RuntimeError("expression badly formed")
    # Evaluates the expression against the type of the first item
    type = obj.variabletype
    for identifier in identifiers:
        obj = symbolhandler.object(identifier)
        if obj.symboltype == adltypes.Symbol.Type.VARIABLE:
            if obj.variabletype != type:
                raise RuntimeError("expressions cannot support operations between different types")
    return type


def check_expression_against_variabletype(identifiers, variabletype):
    """
    Checks the type of the given variables against the given variabletype.

    :param identifiers: the list of the identifiers
    :type identifiers: list
    
    :param type: the type of the variable
    :type type: adltypes.Variable.Type
    
    """
    for identifier in identifiers:
        obj = symbolhandler.object(identifier)
        if obj.symboltype == adltypes.Symbol.Type.VARIABLE:
            if obj.variabletype != variabletype:
                return False
    return True

