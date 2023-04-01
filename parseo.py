import PLY.yacc as yacc

from lexer import tokens
from lexer import reserved



#Nota: este archivo sustituye a 'parsing.py'. 
#TODO: al finalizar este modulo se debe eliminar 'parsing.py'


"""Dictionary of stored procedures(functions) from the program"""

#list of local variables
localVars={}

#list of global variables
globalVars={}

#list of Procs
procedures = {}
proceduresList=[] #Check is two procedures have the same name

#list of errorsw
errorList=[]

#comments
commentList=[]

"""Validations"""
#Main
main=0
commentNumber=0
variableNumber=0

#FOR TESTING
inputFile = "prueba.txt"


#precedence for operators

precedence = (('left','PLUS','MINUS'),
            ('left','STAR','SLASH'),
            ('right','UMINUS'))


#***PRODUCTION RULES***#

def p_sentences(p): #TODO: revisar la concatenacion de sentencias
    '''sentences : sentences sentence
                | sentence
    '''

    if len(p)==2:
        p[0]=[p[1]]
    else:
        p[0]=p[1]+[p[2]]

def p_sentence(p):
    ''' sentence : def
                | call
                | alter
                | not
                | condFunction
                | print
    '''

    p[0] = p[1]

def p_keyword(p):
    ''' keyword : procedure
            | procedure procedure
            | main
    '''

    p[0] = p[1]

def p_body(p): # iterative -> while and until
    ''' body: iterative
            | case
            | def
            | mover
            | aleatorio
            | sentence
            | repeat
    '''

    p[0]=p[1]

####****Body****####
def p_def(p):
    '''def: DEF LP ID COMMA TYPE RP SEMICOLON
        | DEF LP ID COMMA TYPE COMMA value SEMICOLON
    '''
    global localVars
    #if a reserved word is used as an ID
    if p[3] in reserved.values():
        errorList.append("Error: Variable {0} cannot be a reserved word in line {1}.".format(p[1].type, p.lineno(1)))
    if p[3] in localVars.values():
        errorList.append("Error: Variable {0} cannot be defined more than once in line {1}.".format(p[1].type, p.lineno(1)))
    if p[5]== 'int' and isinstance(p[7],bool):
        errorList.append("Error: Variable {0} type and value must match in line {1}.".format(p[1].type, p.lineno(1)))
    if p[5]== 'bool' and isinstance(p[7],int):
        errorList.append("Error: Variable {0} type and value must match in line {1}.".format(p[1].type, p.lineno(1)))
    if len(p)==7:
        #agrega la variable local al diccionario de variables
        localVars[p[3]]= None
        p[0]=(p[1],p[3])
    else:
        #agrega la variable local al diccionario de variables
        localVars.append(str(p[3]),p[7])
        p[0]=(p[1],p[3])

def p_alter(p):
    '''alter: ALTER LP ID COMMA value RP SEMICOLON
    '''
    if p[3] not in localVars:
        errorList.append("Error: Variable {0} has not been defined in line {1}.".format(p[3], p.lineno(1)))
    if p[3] in localVars:
        if isinstance(p[3],bool) or isinstance(p[5],bool):
            errorList.append("Error: Variable {0} type and alter value must be int in line {1}.".format(p[1].type, p.lineno(1)))
        else:
            localVars[p[3]]+= int(p[5])
            p[0]=(p[1],p[3])

def p_not(p):
    '''not: NOT LP ID RP SEMICOLON
    '''
    if p[3] not in localVars:
        errorList.append("Error: Variable {0} has not been defined in line {1}.".format(p[3], p.lineno(1)))
    if p[3] in localVars:
        if isinstance(p[3],bool):
            localVars[p[3]]=not(localVars[p[3]])
            p[0]=(p[1],p[3])

def p_istrue(p):
    '''istrue: ISTRUE LP ID RP SEMICOLON
    '''
    if p[3] not in localVars:
        errorList.append("Error: Variable {0} has not been defined in line {1}.".format(p[3], p.lineno(1)))
    if isinstance(localVars[p[3]], bool) and localVars[p[3]] == True:
        p[0] = (p[1], p[3])
    if isinstance(localVars[p[3]], bool) and localVars[p[3]] == False:
        p[0] = (p[1], p[3])
    else:
        errorList.append("Error: Invalid condition. Expected boolean variable as parameter in line {0}.".format(p.lineno(1)))


#Iterative functions
def p_iterative(p):
    '''iterative: WHILE condition LP instructions RP SEMICOLON
                | UNTIL LP instructions RP condition SEMICOLON
    '''
    if p[1]=='While':
        p[0]=(p[1],p[2],p[4]) #(While, condition, instructions)
    if p[1]=='Until':
        p[0]=(p[1],p[3],p[5]) #(Until, instructions, condition)

def p_case(p):
    '''case: CASE functions SEMICOLON
            | CASE ID functions SEMICOLON
    '''
    if len(p)==4:
        if p[2] not in localVars.values():
            errorList.append("Error: Variable {0} should be defined before usage in line {1}.".format(p[2].type, p.lineno(1)))
        else:
            p[0]=(p[1],p[2],p[3])
    else:
        p[0]=[p[1],p[2]]

def p_call(p):
    '''call: CALL LP ID RP SEMICOLON
    '''
    if p[3] not in proceduresList:
        errorList.append("Error: Procedure {0} should be defined before usage in line {1}.".format(p[3].type, p.lineno(1)))
    if p[3] in proceduresList:
        p[0]=(p[1],p[3])


def p_functions(p):
    '''functions: function
                | functions function
    '''
    if len(p)==2:
        p[0]=[p[1]]
    else:
        p[0]=p[1]+[p[2]]

def p_function(p):#TODO: revisar la concatenacion de functions
    '''function: when then
                | when then else'''
    if len(p)==2:
        p[0]=p[1] + [p[2]]
    else:
        p[0]=p[1] + [p[2]] + [p[3]]

def p_when(p):
    '''when: WHEN LP condition RP
            | WHEN value 
    '''
    if len(p)==2:
        p[0]=(p[1],p[2])

    if len(p)==4:
        p[0]=(p[1],p[3])

def p_then(p):
    '''then: THEN instructions
    '''
    p[0]=(p[1],p[2])

def p_else(p):
    '''else: ELSE instructions
    '''
    p[0]=(p[1],p[2])

def p_instructions(p):
    '''instructions: instruction
                   | instructions instruction
    '''
    if len(p)==2:
        p[0]=[p[1]]
    else:
        p[0]=p[1]+[p[2]]

def p_instruction(p):
    '''instruction: sentences
                  | body
                  |expression'''
    p[0]=p[1]

def p_expression(p):
    '''expression: expression PLUS term
                | expression MINUS term
                | term
    '''
    if len(p)==3:
        if p[2]=='+':
            p[0]=p[1] + p[3]
        elif p[2]=='-':
            p[0]=p[1] - p[3]
    else:
        p[0]=p[1]

def p_term(p):
    '''term: term STAR factor
            | term SLASH factor
            | factor
    '''
    if len(p)==3:
        if p[2]=='*':
            p[0]= p[1] * p[3]
        elif p[2]=='/':
            p[0]= p[1] / p[3]
    else:
        p[0]=p[1]

def p_factor(p):
    '''factor: LP expression RP
            | UMINUS factor
            | INT
    '''
    if len(p)==2:
        p[0]=-p[2]
    
    if len(p)==3:
        p[0]= p[2]
    else:
        p[0]=p[1]
  
def p_condFunction(p):
    '''
    condFunction : istrue
    '''

    p[0] = p[1]

def p_condition(p):
    '''condition: oper GT oper  
                | oper LT oper 
                | oper EQ oper  
                | oper DIF oper   
                | oper GTE oper  
                | oper LTE oper
                | condFunction
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
            p[0]= p[1] == p[3]
        if isinstance(p[1],int) and isinstance(p[3],int):
            p[0]= p[1] == p[3]
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
    else:
        p[0] = p[1]

#Definition of operand
#Used in expression
def p_oper(p):
    '''oper: value
            | expression
    '''
    p[0]=p[1]

#Definition of value 
#Used in define, when, and value
def p_value(p):
    '''value: ID
            | INT
            | BOOL
    '''
    p[0]=p[1]


#Definition of procedure
def p_procedure(p):
    '''procedure: PROC ID LP instructions RP SEMICOLON
    '''
    if p[2] in reserved.values():
        errorList.append("Error: Procedure name {0} cannot be a reserved word in line {1}.".format(p[2], p.lineno(1)))
    
    #If no procedure with the same name has been defined
    if p[2] not in procedures:
        procedures[p[2]]= [len(proceduresList)]
        proceduresList.append([p[2],p[4]])
    
    #If a procedure with the same name has been defined

    if p[2] in procedures:
        errorList.append("Error: Procedure {0} has already been defined in line {1}.".format(p[2], p.lineno(1)))



            
#######COMMENTS##############

#Definition of comments
def p_comments(p):
    '''comments: COMMENT
    '''
    global commentNumber
    commentNumber+=1
    commentList.append(p[1]) 
    p[0]=p[1]






###########Parser###########

#create parser
parser = yacc.yacc(debug=True)

with open(inputFile, 'r') as file:
    data=file.read()
    res=parser.parse(data)
    print(res)
