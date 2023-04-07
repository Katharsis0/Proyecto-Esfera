import ply.yacc as yacc
from mylexer import tokens
inputFile = "prueba.txt"


precedence = (('left','PLUS','MINUS'),
            ('left','STAR','SLASH'))

#TODO: token def,
#Estado inicial
def p_init(p):
    '''init : comment code
            | comment'''
    if len(p) == 2:
        p[0]= p[1] + [p[2]]

    else:
        p[0]=p[1]

#Estructura del codigo esperado
def p_code(p):
    '''code : procedimientos main
            | main procedimientos
            | procedimientos main procedimientos'''
    if len(p) == 2:
        p[0]= p[1] + [p[2]]
    
    else: 
        p[0]= p[1] + [p[2]] + [p[3]] #revisar luego

#Definicion de procedimientos
def p_procedimientos(p):
    '''procedimientos : procedimiento procedimientos
                      | procedimiento
    '''
    if len(p) == 2:
        p[0]= p[1] + [p[2]]

    else:
        p[0]=p[1]

#Definicion de procedimiento
def p_procedimiento(p):
    '''procedimiento : proc'''
    p[0]=p[1]

#Definicion de proc (palabra reservada)
def p_proc(p):
    '''proc : PROC ID LP instrucciones RP'''
    p[0]= (p[2],p[4])

#Definicion del nombre de un procedimiento o una variable
def p_id(p):
    '''id : ID '''
    p[0]=p[1]


def p_instrucciones(p):
    '''instrucciones : instruccion instrucciones
                     | instruccion  
    '''  
    if len(p) == 2:
        p[0]= p[1] + [p[2]]

    else:
        p[0]=p[1]

def p_instruccion(p):
    '''instruccion : def'''
    p[0]=p[1]

def p_def(p):
    '''def : DEF LP ID RP'''
    p[0]= (p[1],p[3])



#Expresiones matematicas
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term STAR factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term SLASH factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LP expression RP'
    p[0] = p[2]
########################################################################

def p_proc(p):
    'proc : PROC LP RP'
    p[0]= p[1]

def p_comment(p):
    '''comment : COMMENT'''
    p[0]=p[1]


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")




#create parser
parser = yacc.yacc(debug=True)

with open(inputFile, 'r') as file:
    data=file.read()
    res=parser.parse(data)
    print(res)