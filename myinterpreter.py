import os
from mysemantic import errorFlag 
from mysemantic import AST
from mysemantic import procedures 
from mysemantic import proceduresList
from mysemantic import errorList
from mysemantic import printsList


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

def caseExe(CASE):
    route=[]
    
    if len(CASE) ==2:
        for i in execute(CASE[1]):
            route.append(i)
    elif len(CASE) ==3:
        if checkCondition(CASE[1]):
            for i in execute(CASE[2]):
                route.append(i)
    return route
    
def isTrueExe(ISTRUE):
    if ISTRUE[1]==True:
        result=True
    elif ISTRUE[1]==False:
        result=False
    
    return result    

def changeExe(CHANGE):
    
    if CHANGE[1] in localVars:
        localVars.update({CHANGE[1]:CHANGE[2]})
        
        
    if CHANGE[1] in globalVars:
        globalVars.update({CHANGE[1]:CHANGE[2]})
    
    else:
        errorList.append("Variable cannot be changed.")
        
def printExe(PRINT):
    if isinstance(PRINT[1],str):
        printsList.append(PRINT[1])
    return printsList
        
    



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
            
            #Verifies When
            elif i[0]== "When":
                route.append(whenExe(i))
            
            #Verifies Else
            elif i[0]=="Else":
                result=elseExe(i)
                route.append(result)
            
            #Verifies IsTrue
            elif i[0]=="IsTrue":
                result= isTrueExe(i)
                route.append(result)
            
            #Verifies Case
            elif i[0]=="Case":
                result= caseExe(i)
                route.append(result)
            
            #Verifies Change (ID modification)
            elif i[0]== "Change":
                result= changeExe(i)
                route.append(result)
            
            #Verifies Print
            elif i[0] == "=>":
                result=printExe(i)
                route.append(result)
            
                
                
            
            
            
                        
                        
                    
                

            
            
                    
            
            
            
            
    
    

def checkCondition(CONDITION):
    
    #GT
    if CONDITION[0]=="GT":
        result= CONDITION[1] > CONDITION[2]
    #LT
    elif CONDITION[0]=="LT":
        result= CONDITION[1] < CONDITION[2]
    
    #DIF
    elif CONDITION[0]=="DIF":
        result= CONDITION[1] != CONDITION[2]
    #EQUAL
    elif CONDITION[0]=="EQUAL":
        result= CONDITION[1] == CONDITION[2]
    
    #GTE
    elif CONDITION[0]=="GTE":
        result= CONDITION[1] >= CONDITION[2]
        
    #GTE
    elif CONDITION[0]=="LTE":
        result= CONDITION[1] <= CONDITION[2]
    
    #ISTRUE
    elif CONDITION[0]=="ISTRUE":
        result= isTrueExe(CONDITION)
        
    return result
    
    
        

def semanticAnalysis():
    pass