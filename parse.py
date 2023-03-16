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


#Definition of parser rules
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
    p[0]=('assign',p[1],p[3])

#Definition of ID(val)
def p_id_rule(p):
    ''' sentence : ID LP VALUE RP SEMICOLON
                 | ID LP ID RP SEMICOLON
                 | ID LP INT PLUS ID RP SEMICOLON
    '''
    p[0]=('assign',p[1],p[3])

#definition of Alter(id,val)
def p_alter_rule(p):
    ''' sentence : ALTER LP ID COMMA INT RP SEMICOLON
    '''
    p[0]=('assign',p[1],p[3])
