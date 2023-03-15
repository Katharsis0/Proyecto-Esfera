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

#Manages multiple sentences in a program
def p_sentence(p):
    ''' sentence : sentence sentence
                 | sentence
    '''
    if len(p)==2:
        p[0]=[p[1]]
    else:
        p[0]=p[1]+[p[2]]

#Definition of a assignment
def p_sentence_assign(p):
    ''' sentence : DEF LP ID COMMA expression SEMICOLON
    '''
    p[0]=('assign',p[1],p[3])