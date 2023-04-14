import os
from mysemantic import errorFlag 
from mysemantic import AST
from mysemantic import procedures 
from mysemantic import proceduresList
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
validFlag= True

##################### Evaluation of code #####################
def assignVariable(LIST, scope):
    #Stores defined variables as local or global depending on the scope
    if scope=="global":
        globalVars[LIST[1]]= value(LIST[2])
        #test comment later
        print(LIST[1], value(LIST[2]))
    
    if scope=="local":
        localVars[LIST[1]] = value(LIST[2])
        
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
def untilExe(UNTIL):
    #Receives a list of instructions and conditions to loop
    #Checks the condition and executes a while with the condition values
    #Calls execute function with the instructions
    #Creates and appends a list with the results from execute function
    
    route= [] #route that follows the program
    
    while checkCondition(UNTIL[2]) == True:
        for i in execute(UNTIL[1]):
            route.append(i)
    
    return route
        

def whileExe(WHILE):
    #Receives a list with the instructions and condition to loop
    #Checks the condition and executes a while with the condition values
    #Calls execute function with instructions
    #Creates and alppends a list with the results from execute func
    
    route=[] #route that follows the program
    routeAux=[]
    
    while checkCondition(WHILE[2]) == True:
        for i in execute(WHILE[1]):
            route.append(i)
            
    if route != []:
        for i in route:
            if i != None:
                for j in i:
                    routeAux.append(j)
        return routeAux

def repeatExe(REPEAT):
    #Receives the instructions and the amount of times to loop
    #Calls exe func with the instructions
    #Creates and appends the list with the results of the route
    
    route=[]
    track=0
    
    while track < value(REPEAT[2]):
        for i in execute(REPEAT[1]):
            route.append(i)
        track+=1
    return track


def whenExe(WHEN):
    #Checks the condition of if statement
    #Calls exe function with the
    #Creates a list with the results of the route
    
    route= []
    
    if checkCondition(WHEN[1]) == True:
        for i in execute(WHEN[2]):
            route.append(i)
    
    if route != []:
        #for testing purposes, comment later
        print ("When Route: ", route)
        return route
    
def elseExe(ELSE):
    #Checks the condition of else statement
    #Calls exe function with the
    #Creates a list with the results of the route
    
    route= []
    
    if checkCondition(ELSE[1]) == True:
        for i in execute(ELSE[2]):
            route.append(i)
    
    else:
        for i in execute(ELSE[3]):
            route.append(i)
            
    return route


def executeFunc(procCall):
    #Receives a list with the procName and the instructions
    global procStack, localVars, variableStack
    route =[]
    
    #Tracks the proc # in the stack
    procStack = procStack + 1
    
    #If localVars exist, appends it to the stack before jumping to the next proc
    if localVars != {}:
        variableStack.append(localVars.copy())
    
    #Checks the existance of the proc
    if procCall[1] in procedures:
        for i in procedures[procCall[1]]:
            #Saves in the list the results of the instructions of the procs
            instructions= execute(proceduresList[i][1])
            
            #Formats the nested lists
            for i in instructions:
                route.append(i)
    
    #At the end of proc execution reduces the number of procs in the stack            
    procStack = procStack - 1
    
    #Clears the localVars after proc execution
    localVars.clear()
    
    if variableStack != []:
        #If vcariable exists in stack, fills the list with the last proc's variables
        localVars = variableStack[-1]    
        variableStack.pop(-1)
    
    return route


def execute(instructionList):
    #receives a list of instructions
    #Checks the order and executes it accordingly
    #generates a list with the instructions results
    
    global scope, procStack, variableStack, validFlag
    
    route= []
    
    #For each line in the input file
    for i in instructionList:
        if isinstance(i,list):
            
            #Executes a Def
            if i[0] == "Def":
                #Checks if variable exists, if it does generates error
                if i[1] in localVars or i[1] in globalVars:
                    errorList.append("Error: Cannot define {1} to variable {0} as it was already defined".format(i[1],i[2]))
                    validFlag= False
                else: #if it doesn't, assigns it
                    assignVariable(i, scope)
            
            #Executes an Until
            elif i[0] == "Until":
                for j in untilExe(i):
                    route.append(j)
            
            #Executes a While
            elif i[0] == "While":
                executedWhile= whileExe(i)
                if executedWhile is not None:
                    for j in executedWhile:
                        route.append(j)
            
            #Executes a Repeat
            elif i[0] == "Repeat":
                #checks proper semantic
                if semanticAnalysis([i[0],i[1]]) == False:
                    validFlag=False
                    
                else:
                    repeatedOrder= repeatExe(i)
                    for j in repeatedOrder:
                        route.append(j)
            
                        
                        
                    
                

            
            
                    
            
            
            
            
    
    

def checkCondition():
    pass

def semanticAnalysis():
    pass