import PLY.yacc as yacc

from lexer import *

"""Dictionary of stored procedures(functions) from the program"""

#list of Procs
procedures = {}
procedureList=[]

#list of errors
errorList=[]

#comments
comments=[]

"""Validations"""
#Main
main=0
commentNumber=0
variableNumber=0



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

#Definition of sentence error
def p_sentence_error(p):
    '''sentence : error
    '''
    
    errorList.append("Syntax error before {0} from line {1}".format(p[1].type,p.lineno(1)))

"""Sentencias"""

#Definition of Def(id,type,val);
#Out: ['Def',id,type,val]
def p_def_rule(p):
    ''' reservedkey : DEF LP ID COMMA TYPE RP SEMICOLON
                 | DEF LP ID COMMA TYPE COMMA BOOl RP SEMICOLON
                 | DEF LP ID COMMA TYPE COMMA INT RP SEMICOLON
    '''

    #if a reserved word is attempted as an ID
    if p[3] in reserved.values():
        #creates a string that includes the name of the variable that caused the error and the line number where the error occurred
        errorList.append("Error: Variable {0} cannot be a reserved word".format(p[3],p.lineno(3))) 
    if len(p)==7:
        p[0]=(p[1],p[3],None)
    elif len(p)==9:
        p[0]=(p[1],p[3],p[7])

#Error of def rule
def p_def_error(p):
    '''sentence : DEF error SEMICOLON
    '''
    errorList.append("Syntax error in procedure {0}, line {1}".format(p[1].type,p.lineno(2)))


#Definition of ID(val)
def p_id_rule(p):
    '''       id : ID LP VALUE RP SEMICOLON
                 | ID LP ID RP SEMICOLON
                 | ID LP expression RP SEMICOLON
                 
    '''
    global variableNumber
    variableNumber+=1
    p[0]=(p[1],p[3]) #Out: (ID,VALUE)

#definition of Alter(id,val) 
def p_alter_rule(p):
    ''' reservedkey : ALTER LP ID COMMA VALUE RP SEMICOLON
                 | ALTER LP ID COMMA ID RP SEMICOLON
    '''
    if(p[5]== True or False):
        errorList.append("Syntax error in procedure {0}, line {1}: Value cannot be bool. ".format(p[1].type,p.lineno(5)))
    else:
        p[0]=(p[1],p[3],p[5])

#definition of error in Alter
def p_alter_error(p):
    '''alter: ALTER error SEMICOLON
    | ALTER LP error RP SEMICOLON
    | ALTER LP ID error RP SEMICOLON
       
    '''
    errorList.append("Syntax error in procedure {0}, line {1}".format(p[1].type,p.lineno(2)))

#definition of value (not sure if needed)
def p_value_rule(p):
    ''' value : INT
            | ID
    '''
    if isinstance(p[1],int):
        p[0]=p[1]


def p_print_rule(p):
    ''' reservedkey : PRINT LP ID RP SEMICOLON
                 | PRINT LP INT RP SEMICOLON
                 | PRINT LP BOOL RP SEMICOLON
                 | PRINT LP STRING RP SEMICOLON
    '''
    p[0]=('print',p[3])




#Definition of Not(val)
# It is called when NOT is found
def p_not_rule(p):
    ''' reservedkey : NOT LP ID RP SEMICOLON
    '''
    if p[3]==True or False:
        p[0]=not p[3]
    
    else:#TODO: Error message: not bool
        pass

#Definition of isTrue(val)
def p_isTrue(p):
    ''' reservedkey : ISTRUE LP ID RP SEMICOLON
    '''
    if p[3]==True or False:
        p[0]=p[3]
    #TODO: Error message: not bool
    else:    
        pass

#Definition of Mover(A) rule
def p_mover_rule(p):
    ''' reservedkey : MOVER LP DIR RP SEMICOLON
    '''
    p[0]=('mover',p[3])
    #TODO: Error message: not DIR
    #TODO: Generate code for NodeMCU



"""Math operations"""
#definition of math operation
def p_expression_rule(p):
    '''expression: expression PLUS expression
                  | expression MINUS expression
                  | expression STAR expression
                  | expression SLASH expression
                
    '''
    #Sum 
    if p[2] == '+':
        p[0] =  p[1]+ p[3]
    #Substr
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    #Multiplication
    elif p[2] == '*':
        p[0] =  p[1], p[3]
    #Division
    elif p[2] == '/':
        p[0] = p[1] / p[3]

#Definition of term as a number
def p_expression_number(p):
    '''expression : INT
    '''
    p[0] = p[1]

#Definition of an expression wrapped in parenthesis
def p_expression_group(p):
    '''expression : LP expression RP
    '''
    p[0] = p[2]


#Definition of negative number
def p_expression_negative(p):
    '''expression : MINUS expression %prec UMINUS
    '''
    p[0] = -p[2]

#Definition of negative number error
def p_expression_negative_error(p):
    '''expression : MINUS error
    '''
    errorList.append("Syntax error in procedure {0}, line {1}".format(p[2].type,p.lineno(1)))

"""Conditional expression"""
#Definition for bool expressions
#Definition for bool expressions - condition
def p_condition_expression(p):
    ''' condition_expression : oper GT oper
                           | oper LT oper
                           | oper GTE oper
                           | oper LTE oper
                           | oper EQUAL oper
                           | oper DIFF oper
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

#Def operator of condition
def p_condition_op(p):
    '''oper: value
            | expression
            
    '''
    if isinstance(p[1],int):
        p[0] = p[1]
    elif isinstance(p[1], list):
        p[0] = p[1]
    else:
        errorList.append("Syntax error in procedure {0}, line {1}: Value cannot be bool. ".format(p[1].type,p.lineno(1)))

"""Comments"""
#Definition of comment
def p_comment(p):
    '''comment : COMMENT
    '''
    global commentNumber
    commentNumber+=1
    #add the comment in order to later validate that there is one comment in the first line of the src
    comments.append(p[1])

    p[0]=p[1]


"""Functions for instructions"""
#Definition of Call rule
def p_call_rule(p):
    ''' reservedkey : CALL LP PROCNAME RP SEMICOLON
    '''
    p[0]= p[3]

#definition of Repeat rule
def p_repeat_rule(p): #TODO: define break
    '''
    reservedkey : REPEAT LP instructions BREAK RP SEMICOLON
    '''
    p[0]=(p[1],p[3])



"""Cycles"""
#Definition of until rule
def p_until_rule(p):
    ''' reservedkey : UNTIL LP instructions RP condition_expression SEMICOLON
    '''
    p[0]=(p[1],p[3],p[5])#Output: (UNTIL,inst, condi)

#Definition of while rule
def p_while_rule(p):
    ''' reservedkey : WHILE condition_expression LP instructions RP SEMICOLON
    '''
    p[0]=(p[1],p[2],p[4])#Output: (WHILE,cond,inst)

def p_whileuntil_error(p):
    ''' reservedkey : WHILE error SEMICOLON
                    | UNTIL error SEMICOLON
    '''
    errorList.append("Syntax error in procedure {0}, line {1}: Value cannot be bool. ".format(p[1].type,p.lineno(2)))

"""Procedures"""
#Definition of procedure rule
def p_procedure_rule(p):
    ''' procedure : PROC ID LP parameters RP LP instructions RP SEMICOLON
    '''

    p[0] = ('FUNCTION', p[2], p[4], p[7])
    #check if ID is a reserved word
    #if p[2] in reserved.values():
     #   errorList.append("Error: The procedure {0} cannot be defined on line {1} because is a reserved word.".format(p[2],p.lineno(2)))
    
    #If not, add it to the dictionary of procedures
    #if p[2] not in procedures:
     #   procedures[p[2]]= [len(procedureList)]
      #  procedureList.append(p[4]) #append(p[4],p[7]
    #If procedure is already defined
    #elif p[2] in procedures:
     #   errorList.append("Error: The procedure {0} cannot be defined on line {1} because it was already defined.".format(p[2],p.lineno(2)))

def p_parameters(p):
    'parameters : ID'
    'parameters : parameters COMMA ID'

    if len(p)==2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + p[[3]]

def p_procedure_error(p):
    ''' procedure : PROC error SEMICOLON
    '''
    errorList.append("Syntax error in procedure {0}, line {1}".format(p[1].type,p.lineno(2)))


#Definition of main procedure
def p_main(p):
    ''' main : MAIN LP instructions RP SEMICOLON
    '''
    global main
    if main !=0:
        errorList.append("Error: The main procedure cannot be defined on line {0} because it can only be declared once.".format(p.lineno(1)))
    else:
        main+=1
        p[0]= (p[1],p[3])
    

#Definition of error in main proc

def p_main_error(p):
    ''' main : MAIN error SEMICOLON
             | MAIN LP error RP SEMICOLON
    '''
    errorList.append("Syntax error in procedure {0}, line {1}".format(p[1].type,p.lineno(2)))


#Definition of procedure calls
def p_procedure_call(p):
    ''' procecall : ID LP RP SEMICOLON
    '''
    #Check if procedure is defined
    if p[3] not in procedures:
        errorList.append("Error: The procedure {0} cannot be called on line {1} because it is not defined.".format(p[3],p.lineno(3)))
    else:
        p[0]=p[1]


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
        #p[0] = p[1] + p[[2]]



#Definition of production rule for instruction
def p_instruction_rule(p):
    '''instruction: sentence
                  | expression
                  | reservedkey
                  | procedure
    '''
    #If its only one element
    if len(p)==2:
        p[0]= [p[1]]
    else:
        #if more than one instruction, concatenate them
        p[0]= p[1] + [p[2]]

#Definition for CASE statement -SIMPLE
def p_case_rule(p):
    ''' reservedkey: CASE when_rule then_rule else_rule
                   | CASE when_rule then_rule
    '''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3], p[4])
    else:
        p[0] = (p[1], p[2], p[3])

#Rule for WHEN statement
def p_when_rule(p):
    ''' reservedkey: WHEN LP condition_expression RP

    '''

    p[0] = (p[1],p[3])

#Rule for THEN statement
def p_then_rule(p):
    '''reservedkey: THEN LP instructions RP
    '''

    p[0] = (p[1],p[3])

#Rule for ELSE statement
def p_else_rule(p):
    ''' reservedkey: LSB ELSE LP instructions RP RSB SEMICOLON
    '''

    p[0] = (p[1],p[3])

