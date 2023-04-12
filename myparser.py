import ply.yacc as yacc

import functions
import random
from mylexer import tokens
inputFile = "prueba.txt"


#list of local variables ID:Value
localVars={}

#list of global variables
globalVars={}

#dictionary of Procs to map funcName:instruction
procedures = {}

#list of errors
errorList=[]

#List of prints
printsList=[]

#comments
commentList=[]

"""Validations"""
#Main
main=0
commentNumber=0
variableNumber=0

precedence = (('left','PLUS','MINUS'),
            ('left','STAR','SLASH'))

#TODO: Break para repeat
#Estado inicial
def p_init(p):
    '''init : comment code
            | comment'''

    if p[1][1]!= '-':
        errorList.append("Error: Must contain at least one comment at the beginning of the program.")
        print(errorList)
    else:
        if len(p) == 3:
            p[0] = [p[1]] + [p[2]]
        if len(p) == 2:
            p[0] = p[1]

#Estructura del codigo esperado
def p_code(p):
    '''code : procedimientos main
            | main procedimientos
            | procedimientos main procedimientos
            | main
            | comment code
            | code comment'''
    if len(p) == 3:
        p[0] = [p[1]] + [p[2]]
    if len(p) == 4:
        p[0] = p[1] + [p[2] + p[3]] #revisar luego
    if len(p)==2:
        p[0] = [p[1]]

#Definicion de procedimientos
def p_procedimientos(p):
    '''procedimientos : procedimiento procedimientos
                      | procedimiento

    '''
    if len(p) == 3:
        p[0]= p[1] + [p[2]]

    else:
        p[0]=p[1]

#Definicion de procedimiento
def p_procedimiento(p):
    '''procedimiento : proc'''
    p[0] = p[1]

#Definicion de proc (palabra reservada)
def p_proc(p):
    '''proc : PROC ID LP instrucciones RP SEMICOLON'''
    if p[2] in procedures:
        errorList.append("Error: procedure {0} cannot be defined more than once in line {1}.".format(p[2],p.lineno(1)))
    else:
        procedures[p[2]]=p[4]
        p[0]= [p[1],p[2], p[4]]

#Definicion del procedimiento main
def p_main(p):
    ''' main : MAIN LP instrucciones RP SEMICOLON
             | MAIN LP RP SEMICOLON'''
    
    global main
    if main !=0:
        errorList.append("Error: The main procedure cannot be defined on line {0} because it can only be declared once.".format(p.lineno(1)))
    else:
        main+=1
        if len(p) == 6:
            p[0] = [p[1], p[3]]
        else:
            p[0] = p[1]


#Definición de las instrucciones recursivas
def p_instrucciones(p):
    '''instrucciones : instruccion instrucciones
                     | instruccion  
    '''  
    if len(p) == 3:
        p[0]= [p[1]] + [p[2]]

    else:
        p[0]=p[1]

#Definición de una instruccion (estructura)
def p_instruccion(p):
    '''instruccion : def
                    | call
                    | alter
                    | not
                    | print
                    | iterative
                    | case
                    | mover
                    | aleatorio
                    | istrue
                    | repeat
                    | change
                    | comment'''
    p[0]=p[1]



#Definicion de cada caso de instruccion
def p_def(p):
    '''def : DEF LP ID COMMA TYPE COMMA value RP SEMICOLON
            | DEF LP ID COMMA TYPE RP SEMICOLON'''
    if p[3] in localVars.values():
        errorList.append("Error: Variable {0} cannot be defined more than once in line {1}.".format(p[1].type, p.lineno(1)))
    if p[5]== 'int' and isinstance(p[7],bool):
        errorList.append("Error: Variable {0} type and value must match in line {1}.".format(p[1].type, p.lineno(1)))
    if p[5]== 'bool' and isinstance(p[7],int):
        errorList.append("Error: Variable {0} type and value must match in line {1}.".format(p[1].type, p.lineno(1)))
    if len(p)==8:
        #agrega la variable local al diccionario de variables
        localVars[p[3]]= None
        p[0]= [p[1],p[3],p[5]]
        functions.definition(p[1],p[3],p[5])
    else:
        #agrega la variable local al diccionario de variables
        localVars.append(str(p[3]),p[7])
        #p[0]=(p[1],p[3])
        p[0]= [p[1],p[3],p[5],p[7]]

def p_call(p):
    '''call : CALL LP ID RP SEMICOLON'''
    #p[0] = [p[1], p[3]]
    if p[3] not in procedures:
        errorList.append("Error: Procedure {0} should be defined before usage in line {1}.".format(p[3].type, p.lineno(1)))
    if p[3] in procedures:
        #p[0]=(p[1],p[3])
        p[0] = [p[1], p[3]]
        functions.llamada(p[1], p[3])

def p_alter(p):
    '''alter : ALTER LP ID COMMA INTEGER RP SEMICOLON
            | ALTER LP ID COMMA ID RP SEMICOLON'''
    #p[0] = [p[1], p[3], p[5]]

    if p[3] not in localVars:
        errorList.append("Error: Variable {0} has not been defined in line {1}.".format(p[3], p.lineno(1)))
    if p[3] in localVars:
        if isinstance(p[3],bool) or isinstance(p[5],bool):
            errorList.append("Error: Variable {0} type and alter value must be int in line {1}.".format(p[1].type, p.lineno(1)))
        else:
            localVars[p[3]]+= int(p[5])
            #p[0]=(p[1],p[3])
            p[0] = [p[1], p[3], p[5]]
            functions.alterar(p[3], p[5])

def p_not(p):
    '''not : NOT LP ID RP SEMICOLON'''
    #p[0] = [p[1], p[3]]

    if p[3] not in localVars:
        errorList.append("Error: Variable {0} has not been defined in line {1}.".format(p[3], p.lineno(1)))
    if p[3] in localVars:
        if isinstance(p[3],bool):
            localVars[p[3]]=not(localVars[p[3]])
            #p[0]=(p[1],p[3])
            p[0] = [p[1], p[3]]
            functions.cambioBool(p[3])
        else:
            errorList.append("Error: Variable must be bool in line {1}".format(p[3],p.lineno(1)))


def p_istrue(p):
    '''istrue : ISTRUE LP ID RP SEMICOLON'''
    #p[0] = [p[1], p[3]]

    if p[3] not in localVars:
        errorList.append("Error: Variable {0} has not been defined in line {1}.".format(p[3], p.lineno(1)))
    if isinstance(localVars[p[3]], bool) and localVars[p[3]] == True:
        p[0] = [p[1], p[3]]
    if isinstance(localVars[p[3]], bool) and localVars[p[3]] == False:
        p[0] = [p[1], p[3]]
    else:
        errorList.append("Error: Invalid condition. Expected boolean variable as parameter in line {0}.".format(p.lineno(1)))
    functions.validarTrue(p[3])

def p_print(p):
    '''print : PRINT LP prints RP SEMICOLON'''
    p[0] = p[1]
    printsList.append(''.join(map(str, p[3])))
    functions.printear(p[3])



def p_prints(p):
    '''prints : printexpr
             | prints printexpr'''
    p[0]= [p[1]] if len(p)==2 else p[1] + p[2]

def p_stringexpr(p):
    '''printexpr : STRING'''
    p[0]=p[1]

def p_idexpr(p):
    '''printexpr : ID'''
    p[0]=str(p[1])

def p_iterativo(p):
    '''iterative : WHILE condicion LP instrucciones RP SEMICOLON
                | UNTIL LP instrucciones RP condicion SEMICOLON
    '''
    if p[1]=='While':
        p[0]=[p[1],p[2],p[4]] #(While, condition, instructions)
        functions.funcionWhile(p[2], p[4])
    if p[1]=='Until':
        p[0]=[p[1],p[3],p[5]] #(Until, instructions, condition)
        functions.funcionUntil(p[3], p[5])

def p_case(p):
    '''case : CASE funciones SEMICOLON
            | CASE ID funciones SEMICOLON
    '''
    if len(p) == 5:
        p[0]=[p[1],p[2],p[3]]
        functions.funcionCase2(p[2], p[3])
    else:
        p[0]=[p[1],p[2]]
        functions.funcionCase1(p[2])

def p_mover(p):
    '''mover : MOVER LP DIR RP SEMICOLON'''
    p[0] = [p[1], p[3]]
    functions.mover(p[3])

def p_aleatorio(p):
    '''aleatorio : ALEATORIO LP RP SEMICOLON'''
    p[0] = p[1]
    listDir=['ATR','ADL','ADE','AIZ','IZQ','DER','DDE','DIZ']
    for i in range (0,9):
        functions.mover(random.choice(listDir))


def p_repeat(p):
    '''repeat : REPEAT LP instrucciones RP SEMICOLON'''
    p[0] = [p[1], p[3]]
    functions.repetir(p[3])

def p_value(p):
    '''value : INTEGER
            | BOOL
    '''
    p[0]=p[1]

def p_funciones(p):
    '''funciones : funcion
                | funciones funcion
    '''
    if len(p)==2:
        p[0]=[p[1]]
    else:
        p[0]=[p[1]]+[p[2]]

def p_funcion(p):#TODO: revisar la concatenacion de functions
    '''funcion : when then
                | when then else'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0]=[p[1]] + [p[2]] + [p[3]]

def p_when(p):
    '''when : WHEN LP condicion RP
            | WHEN value
    '''
    if len(p)==3:
        p[0]=[p[1],p[2]]

    if len(p)==5:
        p[0]=[p[1],p[3]]

def p_then(p):
    '''then : THEN LP instrucciones RP
    '''
    p[0]=[p[1],p[3]]

def p_else(p):
    '''else : ELSE LP instrucciones RP
    '''
    p[0]=[p[1],p[3]]

def p_condicion(p):
    '''condicion : oper GT oper
                | oper LT oper
                | oper EQUAL oper
                | oper DIF oper
                | oper GTE oper
                | oper LTE oper
                | istrue
    '''
    if p[2]=='>':
        if isinstance(p[1],int) and isinstance(p[3],int):
            p[0]= p[1] > p[3]
        else:
            errorList.append("Error: Invalid comparison. Comparison not valid for booleans in line {0}.".format(p.lineno(1)))

    if p[2]=='<':
        if isinstance(p[1],int) and isinstance(p[3],int):
            p[0]= p[1] == p[3]
        if isinstance(p[1],int) and isinstance(p[3],int):
            p[0]= p[1] == p[3]
        else:
            errorList.append("Error: Invalid condition. Comparison between different types in line {0}.".format(p.lineno(1)))

    if p[2]=='><':
        if isinstance(p[1],bool) and isinstance(p[3],bool):
            p[0]= p[1] != p[3]
        if isinstance(p[1],int) and isinstance(p[3],int):
            p[0]= p[1] != p[3]
        else:
            errorList.append("Error: Invalid condition. Comparison between different types in line {0}.".format(p.lineno(1)))

    if p[2]=='>=':
        if isinstance(p[1], int) and isinstance(p[3], int):
            p[0]= p[1] >= p[3]
        else:
            errorList.append("Error: Invalid comparison. Comparison not valid for booleans in line {0}.".format(p.lineno(1)))

    if p[2]=='<=':
        if isinstance(p[1], int) and isinstance(p[3], int):
            p[0]= p[1] <= p[3]
        else:
            errorList.append("Error: Invalid comparison. Comparison not valid for booleans in line {0}.".format(p.lineno(1)))

    if p[2]=='==':
        if isinstance(p[1], int) and isinstance(p[3], int):
            p[0]= p[1] == p[3]
        else:
            errorList.append("Error: Invalid comparison. Comparison not valid for booleans in line {0}.".format(p.lineno(1)))

    else:
        p[0] = p[1]

def p_oper(p):
    '''oper : value
            | expression
    '''
    p[0]=p[1]

#Cambiar el valor de una variable
def p_change(p):
    '''change : ID LP value RP SEMICOLON'''
    if p[1] not in localVars:
        errorList.append("Error: Variable {0} must be defined first before modifying value on line {1}.").format(p[1],p.lineno(1))
    if p[1] in localVars:
        localVars.update({p[1]:p[3]})
        p[0] = [p[1], p[3]]
        functions.cambioVariable(p[1], p[3])


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
    global commentNumber
    commentNumber+=1
    commentList.append(p[1])
    p[0]=p[1]



# Error rule for syntax errors
def p_error(p):
    if p:
        print(f"Error de sintaxis en línea {p.lineno}, columna {p.lexpos}: '{p.value}'")
        print(errorList)
    else:
        print("Error de sintaxis: EOF")
        print(errorList)

    #print("Syntax error in input!")




#create parser
parser = yacc.yacc(debug=True)

with open(inputFile, 'r') as file:
    data=file.read()
    res=parser.parse(data)
    if res != None:
        res = list(filter(None, res))
    print(res)
