# -----------------------------------------------------------------------------
# parser.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module contains the grammar rules for the ADL parser.
# -----------------------------------------------------------------------------

import lexer.lexer as adllexer
import model.types as adltypes
import model.blocks as adlblocks
import model.actions as adlactions


# -----------------------------------------------------------------------------
# Support structures used to store objects during the parsing.
# -----------------------------------------------------------------------------

# List of compound attacks composing the scenario
compound_attacks = []
# List of attacks composing a compound attack
attacks = []
# List of actions composing an attack
actions = []

# Prefix for storing reserved keyword or values into variables 
prefix = '__'

# Symbol table of the scenario scope (level 0)
symbols_scenario = adltypes.SymbolTable(0)
# Symbol table inside the compound attack scope
symbols_compound = adltypes.SymbolTable(1)
# Symbol table inside the attack scope
symbols_attack = adltypes.SymbolTable(2)

# Boolean supporting expression build
contains_string = False

# Supports the rpn representation
rpn = []

# List of objects
objects = []


# -----------------------------------------------------------------------------
# General parsing rule precedence and parsing entry point.
# -----------------------------------------------------------------------------

# Parsing rules precedence
precedence = (
    ('left','ADD','SUB'),
    ('left','MUL','DIV'),
    ('left', 'EXP'),
    ('right','UMINUS', 'ASSIGN'),
)


# Grammar rule for the entry point
def p_entry(p):
    """
    entry : scenario
    """
    p[0] = p[1]


# -----------------------------------------------------------------------------
# Attack section containing the grammar rules for the ADL blocks.
# -----------------------------------------------------------------------------

# Grammar rule for the scenario
def p_scenario(p):
    """
    scenario : SCENARIO LCURVY compound_attacks RCURVY
    """
    # Builds the scenario
    p[0] = adlblocks.Scenario(compound_attacks)


# Grammar rules for the compound attacks
def p_compound_attacks(p):
    """
    compound_attacks : compound_attack
                     | compound_attacks compound_attacks
    """


# Grammar rule for the compound attack
def p_compound_attack(p):
    """
    compound_attack : FROM REAL unit LCURVY compound_attack_codeblock RCURVY
                    | FROM INTEGER unit LCURVY compound_attack_codeblock RCURVY
    """
    # Checks the value of the time
    time = p[2]
    if time < 0:
        print('[Error] time value cannot be negative - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Builds the compound attack and stores it in the related support structure
    codeblock = adlblocks.CodeblockAttackCompound(symbols_compound, attacks)
    compound_attack = adlblocks.AttackCompound(time, p[3], codeblock)
    compound_attacks.append(compound_attack)
    # Clears the support structures for the next compound attack
    symbols_compound.clear()
    del attacks[:]


# Grammar rule for the compound attack codeblock
def p_compound_attack_codeblock(p):
    """
    compound_attack_codeblock : once
                              | periodic
                              | conditional
                              | compound_attack_type
                              | compound_attack_codeblock compound_attack_codeblock
    """


# Grammar rule for the compound attack type
def p_compound_attack_type(p):
    """
    compound_attack_type : compound_attack_codeblock_variable_declaration
                         | compound_attack_codeblock_variable_definition
                         | compound_attack_codeblock_packet_declaration
                         | compound_attack_codeblock_filter_definition
                         | compound_attack_codeblock_list_definition
    """

# Grammar rule for the once attack
def p_once(p):
    """
    once : ONCE LCURVY once_codeblock RCURVY
    """
    # Builds the attack and stores it in the related support structure
    codeblock = adlblocks.CodeblockAttackOnce(symbols_attack, actions)
    attack = adlblocks.AttackOnce(codeblock)
    attacks.append(attack)
    # Clears the support structures for the next attack
    symbols_attack.clear()
    del actions[:]
    
    
# Grammar rule for the once codeblock
def p_once_codeblock(p):
    """
    once_codeblock : physical_action
                   | once_type
                   | expression_assign
                   | once_codeblock once_codeblock
    """


# Grammar rule for the physical action
def p_physical_action(p):
    """
    physical_action : destroy_component
                    | disable_component
                    | deceive_component
                    | misplace_node
                    | destroy_node
    """


# Grammar rule for the types allowed in the once codeblock
def p_once_type(p):
    """
    once_type : attack_codeblock_variable_declaration
              | attack_codeblock_variable_definition
              | attack_codeblock_list_definition
    """


# Grammar rule for the periodic attack
def p_periodic(p):
    """
    periodic : EVERY REAL unit LCURVY periodic_codeblock RCURVY
             | EVERY INTEGER unit LCURVY periodic_codeblock RCURVY
    """
    # Builds the attack and stores it in the related support structure
    codeblock = adlblocks.CodeblockAttackPeriodic(symbols_attack, actions)
    attack = adlblocks.AttackPeriodic(p[2], p[3], codeblock)
    attacks.append(attack)
    # Clears the support structures for the next attack
    symbols_attack.clear()
    del actions[:] 
    

# Grammar rule for the periodic codeblock
def p_periodic_codeblock(p):
    """
    periodic_codeblock : physical_action
                       | unconditional_action
                       | periodic_type
                       | expression_assign
                       | periodic_codeblock periodic_codeblock  
    """


# Grammar rule for the unconditional action
def p_unconditional_action(p):
    """
    unconditional_action : write_field
                         | create_packet
                         | inject_packet
    """


# Grammar rule for the types allowed in the periodic codeblock
def p_periodic_type(p):
    """
    periodic_type : attack_codeblock_variable_declaration
                  | attack_codeblock_variable_definition
                  | attack_codeblock_packet_declaration
                  | attack_codeblock_list_definition
    """


# Grammar rule for the conditional attack
def p_conditional(p):
    """
    conditional : FOR NODES IN list LCURVY conditional_codeblock RCURVY
    """
    attack = adlblocks.AttackConditional(p[4], p[6])
    attacks.append(attack)


# Grammar rule for the conditional codeblock attack
def p_conditional_codeblock(p):
    """
    conditional_codeblock : FOR PACKETS MATCHING filter LCURVY filter_codeblock RCURVY
    """
    codeblock = adlblocks.CodeblockAttackConditional(symbols_attack, p[4], actions)
    # Clears the support structures for the next attack
    symbols_attack.clear()
    del actions[:] 
    p[0] = codeblock
    
    
# Grammar rule for the filter codeblock
def p_filter_codeblock(p):
    """
    filter_codeblock : conditional_action
                     | conditional_type
                     | filter_codeblock filter_codeblock
    """


# Grammar rule for the conditional action
def p_conditional_action(p):
    """
    conditional_action : forward_packet
                       | inject_packet
                       | create_packet
                       | clone_packet
                       | drop_packet
                       | write_field
                       | read_field
    """

# Grammar rule for the conditional type
def p_conditional_type(p):
    """
    conditional_type : attack_codeblock_variable_declaration
                     | attack_codeblock_variable_definition
                     | attack_codeblock_packet_declaration
                     | attack_codeblock_list_definition
    """


# -----------------------------------------------------------------------------
# Types section containing the grammar rules for ADL types.
# -----------------------------------------------------------------------------
def p_variable_declaration(p):
    """
    variable_declaration : VARIABLE IDENTIFIER
    """
    identifier = p[2]
    if identifier in list(adllexer.reserved.keys()):
        print("[Error] " + identifier + " is a reserved keyword - line " + str(p.lineno(1)))
        raise SyntaxError
    # TODO develop here
    
    
    




# Grammar rule for the variable declaration inside a compound attack codeblock
def p_compound_attack_codeblock_variable_declaration(p):
    """
    compound_attack_codeblock_variable_declaration : VARIABLE IDENTIFIER
    """
    identifier = p[2]
    # Checks if the identifier is a reserved keyword
    if identifier in list(adllexer.reserved.keys()):
        print('[Error] ' + identifier + ' is a reserved keyword - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the compound attack scope
    if symbols_compound.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the compound attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Add the identifier into the compound attack scope
    symbols_compound.declare(identifier, adltypes.SymbolTable.TYPE['VARIABLE'])


# Grammar rule for the variable definition (real) inside a compound attack codeblock
def p_compound_attack_codeblock_variable_definition_number_real(p):
    """
    compound_attack_codeblock_variable_definition : VARIABLE IDENTIFIER ASSIGN REAL
    """
    identifier = str(p[2])
    # Checks if the identifier is a reserved keyword
    if identifier in list(adllexer.reserved.keys()):
        print('[Error] ' + identifier + ' is a reserved keyword - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the compound attack scope
    if symbols_compound.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the compound attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Add the identifier into the attack scope
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['REAL'], p[4])
    symbols_compound.define(variable)
        

# Grammar rule for the variable definition (integer) inside a compound attack codeblock
def p_compound_attack_codeblock_variable_definition_number_integer(p):
    """
    compound_attack_codeblock_variable_definition : VARIABLE IDENTIFIER ASSIGN INTEGER
    """
    identifier = str(p[2])
    # Checks if the identifier is a reserved keyword
    if identifier in list(adllexer.reserved.keys()):
        print('[Error] ' + identifier + ' is a reserved keyword - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the compound attack scope
    if symbols_compound.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the compound attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Add the identifier into the attack scope
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['INTEGER'], p[4])
    symbols_compound.define(variable)



# Grammar rule for the variable definition (string) inside a compound attack codeblock
def p_compound_attack_codeblock_variable_definition_number_string(p):
    """
    compound_attack_codeblock_variable_definition : VARIABLE IDENTIFIER ASSIGN STRING
    """
    identifier = str(p[2])
    # Checks if the identifier is a reserved keyword
    if identifier in list(adllexer.reserved.keys()):
        print('[Error] ' + identifier + ' is a reserved keyword - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the compound attack scope
    if symbols_compound.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the compound attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Add the identifier into the attack scope
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['STRING'], p[4])
    symbols_compound.define(variable)


# Grammar rule for packet declaration inside a compound attack codeblock
def p_compound_attack_codeblock_packet_declaration(p):
    """
    compound_attack_codeblock_packet_declaration : PACKET IDENTIFIER
    """
    identifier = str(p[2])
    # Checks if the identifier is a reserved keyword
    if identifier in list(adllexer.reserved.keys()):
        print('[Error] ' + identifier + ' is a reserved keyword - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the compound attack scope
    if symbols_compound.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the compound attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Add the identifier into the local namespace
    symbols_compound.declare(identifier, adltypes.SymbolTable.TYPE['PACKET'])


# Grammar rule for list definition inside the compound attack scope
def p_compound_attack_codeblock_list_definition(p):
    """
    compound_attack_codeblock_list_definition : LIST IDENTIFIER ASSIGN LBRACK list_variables_members RBRACK
    """
    identifier = str(p[2])
    # Checks if the identifier is a reserved keyword
    if identifier in list(adllexer.reserved.keys()):
        print('[Error] ' + identifier + ' is a reserved keyword - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the compound attack scope
    if symbols_compound.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the compound attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    variables = []
    for variable in objects:
        # Builds the list
        variables.append(variable.identifier)
        # Defines the variable into the symbol table inside the compound attack scope
        symbols_compound.define(variable)
    symbols_compound.define(adltypes.List(identifier, variables))
    # Clears the support structure
    del objects[:]


# Grammar rule for the variable declaration inside an attack codeblock
def p_attack_codeblock_variable_declaration(p):
    """
    attack_codeblock_variable_declaration : VARIABLE IDENTIFIER
    """
    identifier = str(p[2])
    # Checks if the identifier is a reserved keyword
    if identifier in list(adllexer.reserved.keys()):
        print('[Error] ' + identifier + ' is a reserved keyword - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the compound attack scope
    if symbols_compound.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the compound attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the attack scope
    if symbols_attack.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Add the identifier into the local namespace
    symbols_attack.declare(identifier, adltypes.SymbolTable.TYPE['VARIABLE'])    


# Grammar rule for the variable definition (real) inside an attack codeblock
def p_attack_codeblock_variable_definition_number_real(p):
    """
    attack_codeblock_variable_definition : VARIABLE IDENTIFIER ASSIGN REAL
    """
    identifier = str(p[2])
    # Checks if the identifier is a reserved keyword
    if identifier in list(adllexer.reserved.keys()):
        print('[Error] ' + identifier + ' is a reserved keyword - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the compound attack scope
    if symbols_compound.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the compound attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the attack scope
    if symbols_attack.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Add the identifier into the attack scope
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['REAL'], p[4])
    symbols_attack.define(variable)


# Grammar rule for the variable definition (integer) inside an attack codeblock
def p_attack_codeblock_variable_definition_number_integer(p):
    """
    attack_codeblock_variable_definition : VARIABLE IDENTIFIER ASSIGN INTEGER
    """
    identifier = str(p[2])
    # Checks if the identifier is a reserved keyword
    if identifier in list(adllexer.reserved.keys()):
        print('[Error] ' + identifier + ' is a reserved keyword - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the compound attack scope
    if symbols_compound.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the compound attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the attack scope
    if symbols_attack.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Add the identifier into the attack scope
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['INTEGER'], p[4])
    symbols_attack.define(variable)
    

# Grammar rule for the variable definition (string) inside an attack codeblock
def p_attack_codeblock_variable_definition_number_string(p):
    """
    attack_codeblock_variable_definition : VARIABLE IDENTIFIER ASSIGN STRING
    """
    identifier = str(p[2])
    # Checks if the identifier is a reserved keyword
    if identifier in list(adllexer.reserved.keys()):
        print('[Error] ' + identifier + ' is a reserved keyword - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the compound attack scope
    if symbols_compound.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the compound attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the attack scope
    if symbols_attack.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Add the identifier into the attack scope
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['STRING'], p[4])
    symbols_attack.define(variable)


# Grammar rule for packet declaration inside an attack codeblock
def p_attack_codeblock_packet_declaration(p):
    """
    attack_codeblock_packet_declaration : PACKET IDENTIFIER
    """
    identifier = str(p[2])
    # Checks if the identifier is a reserved keyword
    if identifier in list(adllexer.reserved.keys()):
        print('[Error] ' + identifier + ' is a reserved keyword - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the compound attack scope
    if symbols_compound.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the compound attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the attack scope
    if symbols_attack.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Add the identifier into the local namespace
    symbols_attack.declare(identifier, adltypes.SymbolTable.TYPE['PACKET'])


# Grammar rule for list definition inside the compound attack scope
def p_attack_codeblock_list_definition(p):
    """
    attack_codeblock_list_definition : LIST IDENTIFIER ASSIGN LBRACK list_variables_members RBRACK
    """
    identifier = str(p[2])
    # Checks if the identifier is a reserved keyword
    if identifier in list(adllexer.reserved.keys()):
        print('[Error] ' + identifier + ' is a reserved keyword - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the compound attack scope
    if symbols_compound.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the compound attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier was already declared in the attack scope
    if symbols_attack.type(identifier) is not None:
        print('[Error] ' + identifier + ' already declared in the attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    variables = []
    for variable in objects:
        # Builds the list
        variables.append(variable.identifier)
        # Defines the variable into the symbol table inside the attack scope
        symbols_attack.define(variable)
    # Defines the list into the symbol table inside the attack scope
    symbols_attack.define(List(identifier, variables))
    # Clears the support structure
    del objects[:]


# -----------------------------------------------------------------------------
# Filter section containing grammar rules for the ADL filter.
# -----------------------------------------------------------------------------

# Grammar rule for the filter definition
def p_compound_attack_codeblock_filter_definition(p):
    """
    compound_attack_codeblock_filter_definition : FILTER IDENTIFIER ASSIGN LROUND filter_content RROUND
    """
    # Checks if the identifier was already declared
    identifier = p[2]
    if symbols_compound.type(identifier) is not None:
        print('[Error] identifier \'' + identifier + '\' already declared - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Stores the packet filter into the support structure
    packet_filter = adltypes.PacketFilter(identifier, rpn)
    symbols_compound.define(packet_filter)
    # Clears the support structure
    del rpn[:]


# Grammar rule for the compound filter content paren
def p_filter_content_compound_paren(p):
    """
    filter_content : LROUND filter_content RROUND
    """

# Grammar rule for the compound filter content
def p_filter_content_compound_both(p):
    """
    filter_content : filter_content logical_operator filter_content
    """
    rpn.append(p[2])


# Grammar rule for the compound filter content
def p_filter_content_compound_reverse(p):
    """
    filter_content : filter_content logical_operator filter_element
    """
    rpn.append(p[3])
    rpn.append(p[2])


# Grammar rule for the compound filter content
def p_filter_content_compound_direct(p):
    """
    filter_content : filter_element logical_operator filter_content
    """
    rpn.append(p[1])
    rpn.append(p[2])
        
    
def p_filter_content_couple(p):
    """
    filter_content : filter_element logical_operator filter_element
    """
    rpn.append(p[1])
    rpn.append(p[3])
    rpn.append(p[2])


# Grammar rule for the filter content mono
def p_filter_content_mono(p):
    """
    filter_content : filter_element
    """
    rpn.append(p[1])


# Grammar rule for the basic element of the packet filter
def p_filter_element(p):
    """
    filter_element : operand comparison_operator operand
    """
    packet_filter_element = adltypes.PacketFilterElement(p[1], p[2], p[3])
    p[0] = packet_filter_element


# Grammar rule for the operand in the packet filter
def p_filter_operand(p):
    """
    operand : variable_value
            | variable_reference
    """
    p[0] = p[1]


# Grammar rule for the comparison operator in the packet filter
def p_comparison_operator(p):
    """
    comparison_operator : NOTEQUALTO
                        | EQUALTO
                        | LSEQTHN
                        | GREQTHN
                        | LSTHN
                        | GRTHN
    """
    value = str(p[1])
    # Prepend the prefix for the reserved keyword
    identifier = prefix + str(p[1])
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['RESERVED'], value)
    symbols_compound.define(variable)
    p[0] = identifier


# Grammar rule for the logical operator in the packet filter
def p_logical_operator(p):
    """
    logical_operator : LAND
                     | LOR
    """
    value = str(p[1])
    # Prepend the prefix for the reserved keyword
    identifier = prefix + str(p[1])
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['RESERVED'], value)
    symbols_compound.define(variable)
    p[0] = identifier


# -----------------------------------------------------------------------------
# Actions section containing the grammar rules for ADL actions.
# -----------------------------------------------------------------------------

# Grammar rule for the action disableComponent(node, component)
def p_disable_component(p):
    """
    disable_component : DISABLECOMPONENT LROUND node COMMA component RROUND
    """
    # Builds and appends the action to the local actions list
    action = adlactions.DisableComponent(p[3], p[5])
    actions.append(action)


# Grammar rule for the action disableComponent(node, component, value)
def p_deceive_component(p):
    """
    deceive_component : DECEIVECOMPONENT LROUND node COMMA component COMMA value RROUND
    """
    # Builds and appends the action to the local actions list
    action = adlactions.DeceiveComponent(p[3], p[5], p[7])
    actions.append(action)


# Grammar rule for the action destroyComponent(node, component)
def p_destroy_component(p):
    """
    destroy_component : DESTROYCOMPONENT LROUND node COMMA component RROUND
    """
    # Builds and appends the action to the local actions list
    action = adlactions.DestroyComponent(p[3], p[5])
    actions.append(action)

# Grammar rule for the action misplaceNode(node, position)
def p_misplace_node(p):
    """
    misplace_node : MISPLACENODE LROUND node COMMA position RROUND
    """
     # Builds and appends the action to the local actions list
    action = adlactions.MisplaceNode(p[3], p[5])
    actions.append(action)


# Grammar rule for the action destroyNode(node)
def p_destroy_node(p):
    """
    destroy_node : DESTROYNODE LROUND node RROUND
    """
    # Builds and appends the action to the local actions list
    action = adlactions.DestroyNode(p[3])
    actions.append(action)


# Grammar rule for the action 'writeField(packet, path, source)'
def p_write_field(p):
    """
    write_field : WRITEFIELD LROUND packet COMMA path COMMA source RROUND
    """
    action = adlactions.WriteField(p[3], p[5], p[7])
    actions.append(action)


# Grammar rule for the action 'readField(destination, packet, path)'
def p_read_field(p):
    """
    read_field : READFIELD LROUND destination COMMA packet COMMA path RROUND
    """
    action = adlactions.ReadField(p[3], p[5], p[7])
    actions.append(action)


# Grammar rule for the action 'forwardPacket(packet, delay, unit)'
def p_forward_packet(p):
    """
    forward_packet : FORWARDPACKET LROUND packet COMMA delay COMMA unit RROUND
    """
    action = adlactions.ForwardPacket(p[3], p[5], p[7])
    actions.append(action)


# Grammar rule for the action 'createPacket(packet, structure)'
def p_create_packet(p):
    """
    create_packet : CREATEPACKET LROUND packet COMMA structure RROUND
    """
    action = adlactions.CreatePacket(p[3], p[5])
    actions.append(action)


# Grammar rule for the action 'injectPacket(packet, node, flow, delay, unit)'
def p_inject_packet(p):
    """
    inject_packet : INJECTPACKET LROUND packet COMMA node COMMA flow COMMA delay COMMA unit RROUND
                  | INJECTPACKET LROUND captured COMMA node COMMA flow COMMA delay COMMA unit RROUND
    """
    action = adlactions.InjectPacket(p[3], p[5], p[7], p[9], p[11])
    actions.append(action)


# Grammar rule for the action 'clonePacket(destination, source)'
def p_clone_packet(p):
    """
    clone_packet : CLONEPACKET LROUND packet COMMA packet RROUND
                 | CLONEPACKET LROUND packet COMMA captured RROUND
    """
    if p[3] == p[5]:
        print("[Error] The source and the destination packet cannot match - line " + str(p.lineno(1)))
        raise SyntaxError
    action = adlactions.ClonePacket(p[3], p[5])
    actions.append(action)

    
# Grammar rule for the action 'dropPacket(packet)'
def p_drop_packet(p):
    """
    drop_packet : DROPPACKET LROUND identifier RROUND
                | DROPPACKET LROUND captured RROUND
    """
    action = adlactions.DropPacket(p[3])
    actions.append(action)


# -----------------------------------------------------------------------------
# Base argument section containing the base grammar rules for the blocks' 
# and the actions' arguments.
# -----------------------------------------------------------------------------

# Grammar rule for strings
def p_argument_string(p):
    """
    string : STRING
    """
    value = str(p[1])
    # Prepend the prefix for authomatically defined variable
    identifier = prefix + value
    # Stores the variable into the symbol table inside the attack scope
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['STRING'], value)
    
    p[0] = identifier


# Grammar rule for unsigned integers
def p_argument_uinteger(p):
    """
    uinteger : INTEGER
    """
    # Stores the number into the symbol table inside the attack scope
    value = p[1]
    if value < 0:
        print("[Error] Positive value expected, a negative value passed - line " + str(p.lineno(1)))
        raise SyntaxError
    # Prepend the prefix for authomatically defined variable
    identifier = prefix + str(value)
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['INTEGER'], value)
    symbols_attack.define(variable)
    p[0] = identifier


# Grammar rule for signed integers
def p_argument_sinteger(p):
    """
    sinteger : INTEGER
    """
    # Stores the number into the symbol table inside the attack scope
    value = p[1]
    # Prepend the prefix for authomatically defined variable
    identifier = prefix + str(value)
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['INTEGER'], value)
    symbols_attack.define(variable)
    p[0] = identifier
    

# Grammar rule for unsigned reals
def p_argument_ureal(p):
    """
    ureal : REAL
          | INTEGER
    """
    # Stores the number into the symbol table inside the attack scope
    value = p[1]
    if p[1] < 0:
        print("[Error] Positive value expected, a negative value passed - line " + str(p.lineno(1)))
        raise SyntaxError
    # Prepend the prefix for authomatically defined variable
    identifier = prefix + str(value)
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['REAL'], value)
    symbols_attack.define(variable)
    p[0] = identifier


# Grammar rule for signed reals
def p_argument_sreal(p):
    """
    sreal : REAL
          | INTEGER
    """
    # Stores the number into the symbol table inside the attack scope
    value = p[1]
    # Prepend the prefix for authomatically defined variable
    identifier = prefix + str(value)
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['REAL'], value)
    symbols_attack.define(variable)
    p[0] = identifier


# Grammar rule for the reserved keyword CAPTURED used as an argument
def p_argument_captured(p):
    """
    captured : CAPTURED
    """
    value = str(p[1])
    # Prepend the prefix for the reserved keyword
    identifier = prefix + str(p[1])
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['RESERVED'], value)
    symbols_attack.define(variable)
    p[0] = identifier


# Grammar rule for the reserved keyword SELF used as an argument
def p_argument_self(p):
    """
    self : SELF
    """
    value = str(p[1])
    # Prepend the prefix for the reserved keyword
    identifier = prefix + str(p[1])
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['RESERVED'], value)
    symbols_attack.define(variable)
    p[0] = identifier


# Grammar rule for the reserved keyword TX used as an argument
def p_argument_flow(p):
    """
    flow : TX
         | RX
    """
    value = str(p[1])
    # Prepend the prefix for the reserved keyword
    identifier = prefix + str(p[1])
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['RESERVED'], value)
    symbols_attack.define(variable)
    p[0] = identifier
    
    
# Grammar rule for the reserved keywords US, MS, S used as an argument
def p_argument_unit(p):
    """
    unit : US
         | MS
         | S
    """
    value = str(p[1])
    # Prepend the prefix for the reserved keyword
    identifier = prefix + str(p[1])
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['RESERVED'], value)
    symbols_attack.define(variable)
    p[0] = identifier
    

# Grammar rule for identifier arguments
def p_argument_identifier(p):
    """
    identifier : IDENTIFIER
    """
    # Checks if the identifier was already declared in any scope
    identifier = str(p[1])
    if not symbols_compound.exist(identifier):
        if not symbols_attack.type(identifier):
            print("[Error] " + identifier + " not declared in any scope - line " + str(p.lineno(1)))
            raise SyntaxError
    p[0] = identifier


# Grammar rule for list of variables argument
def p_argument_list_variables(p):
    """
    list_variables : LBRACK list_variables_members RBRACK
    """
    identifier = prefix
    variables = []
    # Builds the list
    for variable in objects:
        identifier += variable.identifier
        variables.append(variable.identifier)
        # Defines the variable into the symbol table inside the attack scope
        symbols_attack.define(variable)
    symbols_attack(List(identifier, variables))
    # Clears the support structure
    del objects[:]
    p[0] = identifier

    
# Grammar rule for list members
def p_argument_list_variables_members(p):
    """
    list_variables_members : list_variables_members COMMA list_variables_members
    """


# Grammar rule for list member
def p_argument_list_variables_members_string(p):
    """
    list_variables_members : STRING
    """
    value = p[1]
    identifier = prefix + value
    variable = adltypes.Variable(identifier, adltypes.Variables.TYPE['STRING'], value)
    objects.append(variable)


# Grammar rule for list member
def p_argument_list_variables_members_real(p):
    """
    list_variables_members : REAL
    """
    value = p[1]
    identifier = prefix + str(value)
    variable = adltypes.Variable(identifier, adltypes.Variables.TYPE['REAL'], value)
    objects.append(variable)


# Grammar rule for list member
def p_argument_list_variables_members_integer(p):
    """
    list_variables_members : INTEGER
    """
    value = p[1]
    identifier = prefix + str(value)
    variable = adltypes.Variable(identifier, adltypes.Variable.TYPE['INTEGER'], value)
    objects.append(variable)


# Grammar rule for variables passed by value
def p_variable_value(p):
    """
    variable_value : string
                   | sreal
    """
    p[0] = p[1]


# Grammar rule for the variables passed by reference
def p_variable_reference(p):
    """
    variable_reference : identifier
    """
    identifier = p[1]
    # Gets the variable, if exists
    variable = symbols_compound.variable(identifier)
    if variable is None:
        variable = symbols_attack.variable(identifier)
    if variable is None:
        print('[Error] ' + identifier + ' is not a variable - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the variable is well defined
    if variable.type == adltypes.Variable.TYPE['NONE']:
        # Checks if the variable is defined through an expression
        for action in actions:
            if isinstance(action, adlactions.Expression):
                if identifier == action.destination:
                    is_defined == True                
                    break
        if not is_defined:
            print('[Error] ' + identifier + ' is not defined - line ' + str(p.lineno(1)))
            raise SyntaxError 
    p[0] = identifier


# Grammar rule for lists passed by value
def p_list_variables_value(p):
    """
    list_variables_value : list_variables
    """
    p[0] = p[1]


# Grammar rule for lists passed by reference
def p_list_variables_reference(p):
    """
    list_variables_reference : identifier
    """
    identifier = p[1]
    # Check if the identifier refers a list
    list = symbols_compound.list(identifier)
    if list is None:
        list = symbols_attack.list(identifier)
    if list is None:
        print('[Error] ' + identifier + ' is not a list - line ' + str(p.lineno(1)))
        raise SyntaxError
    p[0] = indentifier

    
# -----------------------------------------------------------------------------
# Custom argument section containing the custom grammar rules for the blocks' 
# and the actions' arguments.
# -----------------------------------------------------------------------------

# Grammar rule for the node argument
def p_node(p):
    """
    node : variable_value
         | variable_reference
    """
    p[0] = p[1]


# Grammar rule for the component argument
def p_component(p):
    """
    component : variable_value
              | variable_reference
    """
    p[0] = p[1]


# Grammar rule for the value argument
def p_value(p):
    """
    value : variable_value
          | variable_reference
    """
    p[0] = p[1]


def p_position(p):
    """
    position : list_variables_value
             | list_variables_reference
    """
    p[0] = p[1]


# Grammar rule for packet identifiers
def p_packet(p):
    """
    packet : identifier
    """
    identifier = p[1]
    type = symbols_compound.type(identifier)
    if type is None:
        type = symbols_attack.types[identifier]
    # Checks if the identifier is defined
    if type != adltypes.SymbolTable.TYPE['PACKET']:
       print('[Error] ' + identifier + ' is not a packet - line ' + str(p.lineno(1)))
       raise SyntaxError
    p[0] = identifier


# Grammar rule for the path (value)
def p_path(p):
    """
    path : variable_value
         | variable_reference
    """
    p[0] = p[1]


# Grammar rule for the source
def p_source(p):
    """
    source : variable_value
           | variable_reference
    """
    p[0] = p[1]


# Grammar rule for the destination
def p_destination(p):
    """
    destination : identifier
    """
    identifier = p[1]
    variable = ymbol_table_compound_attack.variable(identifier)
    if variable is None:
        variable = symbols_attack.variable(identifier)
    if variable is None:
       print('[Error] ' + identifier + ' is not a variable - line ' + str(p.lineno(1)))
       raise SyntaxError
    p[0] = indentifier


# Grammar rule for the structure
def p_structure(p):
    """
    structure : variable_value
              | variable_reference
    """
    p[0] = p[1]


# Grammar rule for the delay
def p_delay(p):
    """
    delay : variable_value
          | variable_reference
    """
    p[0] = p[1]
    

# Grammar rule for list of variables as argument of attack
def p_attack_list_value(p):
    """
    attack_list_value : LBRACK list_variables_members RBRACK
    """
    identifier = prefix
    variables = []
    # Builds the list
    for variable in objects:
        identifier += variable.identifier
        variables.append(variable.identifier)
        # Defines the variable into the symbol table inside the attack scope
        symbols_compound.define(variable)
    symbols_compound(List(identifier, variables))
    # Clears the support structure
    del objects[:]
    p[0] = identifier
            
    
def p_attack_list_reference(p):
    """
    attack_list_reference : identifier
    """
    identifier = p[1]
    # Check if the identifier refers a list inside the compound attack scope
    type = symbols_compound.type(identifier)
    if type is None:
        print('[Error] ' + identifier + ' not defined inside the compound attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier refers a list
    if type != adltypes.SymbolTable.TYPE['LIST']:
        print('[Error] ' + identifier + ' is not a list - line ' + str(p.lineno(1)))
        raise SyntaxError
    p[0] = identifier


# Grammar rule for list argument
def p_list(p):
    """
    list : attack_list_value
         | attack_list_reference
    """
    p[0] = p[1]    


# Grammar rule for filter argument
def p_filter(p):
    """
    filter : identifier
    """
    # Checks if the identifier is a filter
    identifier = p[1]
    type = symbols_compound.type(identifier)
    if type is None:
        print('[Error] ' + identifier + ' is not defined inside the compound attack scope - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the identifier refers a Filter
    if type != adltypes.SymbolTable.TYPE['FILTER']:
        print('[Error] ' + identifier + ' is not a filter - line ' + str(p.lineno(1)))
        raise SyntaxError
    p[0] = identifier


# -----------------------------------------------------------------------------
# Expression section containing the grammar rules to support expressions.
# -----------------------------------------------------------------------------

# Grammar rule for assignments in the expressions
def p_expression_assign(p):
    """
    expression_assign : identifier ASSIGN expression
    """
    identifier = p[1]
    # Checks if the identifier refers a variable
    variable = symbols_compound.variable(identifier)
    if variable is None:
        variable = symbols_attack.variable(identifier)
    if variable is None:
        print('[Error] ' + identifier + ' is not a variable - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Builds the expression and appends it to the action list
    action = adlactions.Expression(identifier, rpn)
    actions.append(action)
    # Clears the support structures
    del rpn[:]
    contains_string = False


# Grammar rule for assignments in the expressions (generic)
def p_expression_assign_generic(p):
    """
    expression_assign : identifier ADDASSIGN expression
    """
    identifier = p[1]
    # Checks if the identifier refers a variable
    variable = symbols_compound.variable(identifier)
    if variable is None:
        variable = symbols_attack.variable(identifier)
    if variable is None:
        print('[Error] ' + identifier + ' is not a variable - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the variable is well defined
    if variable.type == adltypes.Variable.TYPE['NONE']:
        # Checks if the variable is defined through another expression
        for action in list(actions):
            if isinstance(action, adlaction.Expression):
                if identifier == action.destination:
                    is_defined = True
                    break
        if not is_defined:
            print('[Error] ' + identifier + ' is not defined - line ' + str(p.lineno(1)))
            raise SyntaxError
    # Pushes into the expression list the operands and the operator following the RPN order
    rpn.append(p[1])
    rpn.append('+')
    # Builds the expression and append to the action list
    action = adlactions.Expression(identifier, rpn)
    actions.append(action)
    # Clears the support structures
    del rpn[:]
    contains_string = False


# Grammar rule for assignments in the expressions (numbers)
def p_expression_assign_numbers(p):
    """
    expression_assign : identifier SUBASSIGN expression
                      | identifier MULASSIGN expression
                      | identifier DIVASSIGN expression
                      | identifier MODASSIGN expression
    """
    global contains_string
    if contains_string:
        print('[Error] The operator \'' + str(p[2]) + '\' is not allowed on strings - line ' + str(p.lineno(1)))
        raise SyntaxError
    identifier = p[1]
    # Checks if the identifier refers a variable
    variable = symbols_compound.variable(identifier)
    if variable is None:
        variable = symbols_attack.variable(identifier)
    if variable is None:
        print('[Error] ' + identifier + ' is not a variable - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the variable is well defined
    if variable.type == adltypes.Variable.TYPE['NONE']:
        # Checks if the variable is defined through another expression
        for action in list(actions):
            if isinstance(action, adlaction.Expression):
                if identifier == action.destination:
                    is_defined = True
                    break
        if not is_defined:
            print('[Error] ' + identifier + ' is not defined - line ' + str(p.lineno(1)))
            raise SyntaxError
    # Pushes into the expression list the operands and the operator following the RPN order
    rpn.append(p[1])
    if p[2] == '-=':
        rpn.append('-')
    elif p[2] == '*=':
        rpn.append('*')
    elif p[2] == '/=':
        rpn.append('/')
    else:
        rpn.append('|')
    # Builds the expression and append to the action list
    action = adlactions.Expression(identifier, rpn)
    actions.append(action)
    # Clears the support structures
    del rpn[:]
    contains_string = False


# Grammar rule for the arithmetic add operation in the expressions (generic)
def p_expression_binop_generic(p):
    """
    expression : expression ADD expression
    """
    # Pushes the operands and the operator into the attack stack following the RPN order
    rpn.append(p[1])
    rpn.append(p[3])
    rpn.append(p[2])


# Grammar rule for arithmetic operations in the expressions (numbers)
def p_expression_binop_numbers(p):
    """
    expression : expression SUB expression
               | expression MUL expression
               | expression DIV expression
               | expression MOD expression
               | expression EXP expression
    """
    global contains_string
    if contains_string:
        print('[Error] The operator \'' + str(p[2]) + '\' is not allowed on strings - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Pushes the operands and the operator into the expression list following the RPN order
    rpn.append(p[1])
    rpn.append(p[3])
    rpn.append(p[2])


# Grammar rule for the uminus in the expressions
def p_expression_uminus(p):
    """
    expression : SUB expression %prec UMINUS
    """
    global contains_string
    if contains_string:
        print('[Error] uminus cannot be applied to strings - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Authomatic integer -1
    value = -1
    identifier = prefix + str(value)
    symbols_attack.define(Variable(identifier, adltypes.Variables.TYPE['INTEGER'], value))
    # Pushes the operands and the operator into the expression list following the RPN order
    rpn.append(identifier)
    rpn.append(p[2])
    rpn.append('*')


# Grammar rule for a group of expressions in the expressions
def p_expression_group(p):
    """
    expression : LROUND expression RROUND
    """
    p[0] = p[2]


# Grammar rule for the strings in the expressions
def p_expression_string(p):
    """
    expression : string
    """
    global contains_string
    contains_string = True
    p[0] = p[1]


# Grammar rule for the numbers in the expressions
def p_expression_number(p):
    """
    expression : sreal
               | sinteger
    """
    p[0] = p[1]


# Grammar rule for the identifiers in the expressions
def p_expression_identifier(p):
    """
    expression : identifier
    """
    identifier = p[1]
    # Checks if the identifier is a variable
    variable = symbols_compound.variable(identifier)
    if type is None:
        variable = symbols_attack.variable(identifier)
    if type is None:
        print('[Error] ' + identifier + ' is not a variable - line ' + str(p.lineno(1)))
        raise SyntaxError
    # Checks if the variable is well defined
    if variable.type == adltypes.Variable.TYPE['NONE']:
        # Checks if the variable is defined through another expression
        for action in list(actions):
            if isinstance(action, adlaction.Expression):
                if identifier == action.destination:
                    is_defined = True
                    break
        if not is_defined:
            print('[Error] ' + identifier + ' is not defined - line ' + str(p.lineno(1)))
            raise SyntaxError
    p[0] = identifier


# -----------------------------------------------------------------------------
# Error section containing the grammar rules to support errors handling.
# -----------------------------------------------------------------------------

# FIXME it does not work
# Generic error handler
def p_error(p):
    tok = adllexer.tokens()
    print("[Error] wrong syntax - line " + str(tok.lineno) + " " + str(tok))
