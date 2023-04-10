import ply.yacc as yacc
from mylexer import tokens
inputFile = "prueba.txt"


#list of local variables
localVars={}

#list of global variables
globalVars={}

#list of Procs
procedures = {}
proceduresList=[] #Check is two procedures have the same name

#list of errors
errorList=[]

#comments
commentList=[]

"""Validations"""
#Main
main=0
commentNumber=0
variableNumber=0

precedence = (('left','PLUS','MINUS'),
            ('left','STAR','SLASH'))

#TODO: token def,
#Estado inicial
def p_init(p):
    '''init : func'''
    # '''init : comment code
    #         | comment'''

    # if len(p) == 2:
    #     p[0]= p[1] + [p[2]]
    #
    # else:
    p[0]=p[1]

def p_second(p):
    '''second : comment code
              | comment'''

def p_paren(p):
    '''func : DEF ID'''
    p[0] = (p[1], p[3])

#Estructura del codigo esperado
def p_code(p):
    '''code : procedimientos main
            | main procedimientos
            | procedimientos main procedimientos
            | main '''
    if len(p) == 2:
        p[0] = p[1] + p[2]
    if len(p) == 3:
        p[0]= p[1] + p[2] + p[3] #revisar luego
    else:
        p[0] = p[1]

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
    '''proc : PROC ID LP factor RP SEMICOLON'''
    p[0]= (p[1],p[2], p[4])

#Definicion del procedimiento main
def p_main(p):
    ''' main : MAIN LP instrucciones RP SEMICOLON
             | MAIN SEMICOLON'''
    if len(p) == 4:
        p[0] = ('@Principal', p[3])
    else:
        p[0] = ('@Principal')

#Definicion del nombre de un procedimiento o una variable
def p_id(p):
    '''id : ID'''
    p[0]=(p[1])

#Definición de las instrucciones recursivas
def p_instrucciones(p):
    '''instrucciones : instruccion instrucciones
                     | instruccion  
    '''  
    if len(p) == 2:
        p[0]= p[1] + [p[2]]

    else:
        p[0]=p[1]

#Definición de una instruccion (estructura)
def p_instruccion(p): #Agregar condFuntion y los demás
    '''instruccion : def
                    | call
                    | alter
                    | not
                    | print
                    | iterative
                    | case
                    | mover
                    | aleatorio
                    | repeat'''
    p[0]=p[1]



#Definicion de cada caso de instruccion
def p_def(p):
    '''def : DEF LP factor RP'''
    p[0]= (p[1],p[3])

def p_call(p):
    '''call : CALL LP id RP SEMICOLON'''
    p[0] = (p[1], p[3])

def p_alter(p):
    '''alter : ALTER LP id COMMA factor RP SEMICOLON'''
    p[0] = (p[1], p[3], p[5])

def p_not(p):
    '''not : NOT LP id RP SEMICOLON'''
    p[0] = (p[1], p[2])

def p_condFuncion(p):
    '''istrue : ISTRUE LP id RP SEMICOLON'''
    p[0] = (p[1], p[3])

def p_print(p):
    '''print : PRINT LP RP SEMICOLON'''
    p[0] = p[1]


def p_iterativo(p): #WHILE condicion LP instrucciones RP
    '''iterative : WHILE LP instrucciones SEMICOLON
                | UNTIL LP RP instrucciones SEMICOLON
    '''
    if p[1]=='While':
        p[0]=(p[1],p[2],p[4]) #(While, condition, instructions)
    if p[1]=='Until':
        p[0]=(p[1],p[3],p[5]) #(Until, instructions, condition)

def p_case(p):
    '''case : CASE instrucciones SEMICOLON
            | CASE ID instrucciones SEMICOLON
    '''
    if len(p) == 4:
        p[0]=(p[1],p[2],p[3])
    else:
        p[0]=[p[1],p[2]]

def p_mover(p):
    '''mover : MOVER LP DIR RP SEMICOLON'''
    p[0] = (p[1], p[3])

def p_aleatorio(p):
    '''aleatorio : ALEATORIO LP RP SEMICOLON'''
    p[0] = p[1]


def p_repeat(p):
    '''repeat : REPEAT LP instrucciones RP '''
    p[0] = (p[1], p[3])



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
    'factor : INTEGER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LP expression RP'
    p[0] = p[2]
########################################################################

def p_comment(p):
    '''comment : COMMENT'''
    p[0]=p[1]


# Error rule for syntax errors
def p_error(p):
    if p:
        print(f"Error de sintaxis en línea {p.lineno}, columna {p.lexpos}: '{p.value}'")
    else:
        print("Error de sintaxis: EOF")

    #print("Syntax error in input!")




#create parser
parser = yacc.yacc(debug=True)

with open(inputFile, 'r') as file:
    data=file.read()
    res=parser.parse(data)
    print(res)