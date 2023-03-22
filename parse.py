import PLY.yacc as yacc

from lexer import tokens

#list of variables
variables = {}#dictionary as id:value

boolVariables={}

#list of functions
functions = {}

#precedence for operators

precedence = (('left','PLUS','MINUS'),
            ('left','STAR','SLASH'),
            ('right','UMINUS'))


#***PRODUCTION RULES***#

#sentence: valid combo of tokens

#Manages multiple sentences in a program
def p_sentence_rule(p):
    ''' sentence : sentence sentence
                 | sentence
    '''
    if len(p)==2:
        p[0]=[p[1]]
    else:
        p[0]=p[1]+[p[2]]

#Definition of Def(id,type,val);
def p_def_rule(p):
    ''' sentence : DEF LP ID COMMA TYPE RP SEMICOLON
                 | DEF LP ID COMMA TYPE COMMA BOOl RP SEMICOLON
                 | DEF LP ID COMMA TYPE COMMA INT RP SEMICOLON
    '''
    if len(p)==7:
        p[0]=('assign',p[3],None)
    elif len(p)==9:
        p[0]=('assign',p[3],p[7])

#Definition of ID(val)
def p_id_rule(p):
    ''' sentence : ID LP VALUE RP SEMICOLON
                 | ID LP ID RP SEMICOLON
                 | ID LP INT PLUS ID RP SEMICOLON
    '''
    if isinstance(p[3],int) and isinstance(p[5],int):
        res =p[3]+p[5]
        p[0]=('assign',p[1],res)
    else:
        p[0]=('assign',p[1],p[3])

#definition of Alter(id,val) 
def p_alter_rule(p):
    ''' sentence : ALTER LP ID COMMA INT RP SEMICOLON
    '''
    p[0]=('assign',p[3],p[5])


#definition of expression
def p_expression_rule(p):
    '''expression: term
                  | expression PLUS term
                  | expression MINUS term
                  | expression STAR term
                  | expression SLASH term
                
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '+':
        p[0] = ('add', p[1], p[3])
    elif p[2] == '-':
        p[0] = ('sub', p[1], p[3])
    elif p[2] == '*':
        p[0] = ('mul', p[1], p[3])
    elif p[2] == '/':
        p[0] = ('div', p[1], p[3])

def p_print_rule(p):
    ''' sentence : PRINT LP ID RP SEMICOLON
                 | PRINT LP INT RP SEMICOLON
                 | PRINT LP BOOL RP SEMICOLON
    '''
    p[0]=('print',p[3])

#Definition for bool expressions
#Definition for bool expressions - condition
def p_boolean_expression(p):
    ''' boolean_expression : INT GT INT
                           | INT LT INT
                           | INT GTE INT
                           | INT LTE INT
                           | BOOL EQUAL BOOL
                           | BOOL DIFF BOOL
    '''

    if p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    else:
        p[0] = p[1] != p[3]



#Definition of Not(val)
# It is called when NOT is found
def p_not_rule(p):
    ''' sentence : NOT LP ID RP SEMICOLON
    '''
    if p[3]==True or False:
        p[0]=not p[3]
    
    else:#TODO: Error message: not bool
        pass

#Definition of isTrue(val)
def p_isTrue(p):
    ''' sentence : ISTRUE LP ID RP SEMICOLON
    '''
    if p[3]==True or False:
        p[0]=p[3]
    #TODO: Error message: not bool
    else:    
        pass

#Definition of Mover(A) rule
def p_mover_rule(p):
    ''' sentence : MOVER LP DIR RP SEMICOLON
    '''
    p[0]=('mover',p[3])


#Definition of Proc rule 
def p_proc_rule(p):
    ''' process : PROC PROCNAME LP instructions RP SEMICOLON
    '''
    p[0]=('proc',p[2])

#Definition of instructions to handle one or more inst
def p_instructions_rule(p):
    ''' instructions : instructions instruction
                     | instruction
    '''
    if len(p)==2:
        p[0]=[p[1]]
    else:
        p[1].append(p[2])
        p[0]=p[1]

#Definition of production rule for instruction
def p_instruction_rule(p):
    '''instruction: sentence
                  | expression
                  | boolean_expression
    '''
    p[0]=p[1]

#Definition of Call rule
def p_call_rule(p):
    ''' sentence : CALL LP PROCNAME RP SEMICOLON
    '''
    p[0]=('call',p[3])