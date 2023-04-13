import os
from mysemantic import errorFlag 
from mysemantic import AST
from mysemantic import procedures 
from mysemantic import procedureList
from mysemantic import errorList

errorFolder= os.getcwd() + "/Errors/error.txt"

#Code to execute
code=[]

#NodeMCU instructions
instructions=[]

#Local vars ID:Valor
localVars={}

#global vars ID:Valor
globalVars={}

#Reserved keys
reservedKeys= ["Mover", "Aleatorio"]

#Variable scope
scope= "global"

#If a proc is called in another proc keeps track of amount of procs in stack 
procStack= 0

#If a proc is called in another proc keeps track of variables 
variableStack=[]

#Flag to check if code is free of errors in order to run
valid= True

##################### Evaluation of code #####################
 
def assignVariable(list, scope):
    #Stores defined variables as local or global depending on the scope
    if scope=="global":
        globalVars[list[1]]= value(list[2])
        #test comment later
        print(list[1], value(list[2]))
    
    if scope=="local":
        localVars[list[1]] = value(list[2])
        
def value(x):
    #Returns the value of a variable
    if x in localVars:
        return localVars[x]
    elif x in globalVars:
        return globalVars[x]
    elif x == False:
        return False
    elif x == True:
        return True
    elif isinstance(x, int):
        return x
        
######Execution of code#######
def until(until):
    #Receives a list of instructions and conditions to loop
    #Checks the condition and executes a while with the condition values
    #Calls execute function with the instructions
    #Creates and appends a list with the results from exe function
    
    route= []
    pass