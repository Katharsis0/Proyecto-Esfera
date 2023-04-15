import os
import random

from mysemantic import errorFlag
from mysemantic import AST
from mysemantic import procedures 
from mysemantic import proceduresList
from mysemantic import errorList
from mysemantic import printsList


errorFolder= os.getcwd() + "/Errors/error.txt"

#Code to execute
codeMain=[]

codeProcs=[]

codeExe=[]

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

duino=[]

##################### Evaluation of code #####################
def assignVariable(LIST, scope):
    #Stores defined variables as local or global depending on the scope
    print(f'VariableList {LIST}')
    if scope=="global":
        globalVars[LIST[1]]= value(LIST[3])
        #test comment later
        print(LIST[1], value(LIST[3]))
    
    if scope=="local":
        localVars[LIST[1]] = value(LIST[3])
        
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
    print("El while", WHILE)
    route=[] #route that follows the program
    routeAux=[]
    
    while checkCondition(WHILE[1]) == True:
        for i in execute(WHILE[2]):
            route.append(i)
        print("Ruta while: ",route)
            
    if route != []:
        for i in route:
            if i != None:
                for j in i:
                    routeAux.append(j)
        print("Ruta while aux:", routeAux)
        return routeAux

def repeatExe(REPEAT):
    print(REPEAT)
    route = []
    for i in execute(REPEAT[1]):
        route.append(i)
    return route
    
    
    

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
    return value(ISTRUE[1])
    
def changeExe(CHANGE):
    print(globalVars) 
    if CHANGE[1] in localVars:
        localVars.update({CHANGE[1]:CHANGE[2]})
    
    if CHANGE[1] in globalVars:
        globalVars.update({CHANGE[1]:CHANGE[2]})
    
    else:
        errorList.append("Variable cannot be changed.")
    print(globalVars)

        
        
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
    if procCall[0] in procedures:
        for i in procedures[procCall[1]]:
            #Saves in the list the results of the instructions of the procs
            instructions= execute(procCall[1])
            
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

def moverExe(direction):
    #En cada caso se hace la transformación debida
    dir=[]
    if direction[2] == 'ATR':
        dir.append("pwm:-100")
    elif  direction[2] == 'ADL':
        dir.append("pwm:100")
    elif  direction[2] == 'ADE':
        dir.append("diagD:-1")
    elif  direction[2] == 'AIZ':
        dir.append("diagI:-1")
    elif  direction[2] == 'IZQ':
        dir.append("dir:-1")
    elif  direction[2] == 'DER':
        dir.append("dir:1")
    elif  direction[2] == 'DDE':
        dir.append("diagD:1")
    elif  direction[2] == 'DIZ':
        dir.append("diagI:1")

    #Se retorna el dato debido
    return dir

def aleatorioExe():

    route = []
    listDir=['ATR','ADL','ADE','AIZ','IZQ','DER','DDE','DIZ']
    for x in range(11):
        route += random.choice(listDir)
    return route

def notExe(variable):
    print("el not: " , variable)
    changeExe(["Change",variable, not(value(variable))])



def execute(instructionList):
    #receives a list of instructions
    #Checks the order and executes it accordingly
    #generates a list with the instructions results
    
    global scope, procStack, variableStack, validFlag
    
    route= []
    print("Init execute")
    print("InstructionList: ", instructionList)
    #For each line in the input file
    for i in instructionList:    
        if isinstance(i,list):
            
            #Executes a Def
            if i[0] == "Def":
                print("Encontro def")
                #Checks if variable exists, if it does generates error
                if i[1] in localVars or i[1] in globalVars:
                    errorList.append("Error: Cannot define {1} to variable {0} as it was already defined".format(i[1],i[2]))
                    validFlag= False
                else: #if it doesn't, assigns it
                    assignVariable(i, scope)
            
            #Executes an Until
            elif i[0] == "Until":
                print("Encontro Until")
                
                for j in untilExe(i):
                    route.append(j)
            
            #Executes a While
            elif i[0] == "While":
                print("Encontro While")
                executedWhile= whileExe(i)
                if executedWhile is not None:
                    for j in executedWhile:
                        route.append(j)
            
            #Executes a Repeat
            elif i[0] == "Repeat":
                print("Encontro repeat")
                repeatedOrder = repeatExe(i)
                for j in repeatedOrder:
                    route.append(j)
            
            #Verifies When
            elif i[0]== "When":
                print("Encontro When")
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
                print("I del change:", i)
                if isinstance(i[2],list):
                    if i[2][1] in localVars or i[2][1] in globalVars:
                        i[2]=not(value(i[2][1]))
                    
                elif i[2] in localVars or i[2] in globalVars:
                    i[2]=value(i[2])        
            
                result= changeExe(i)
                route.append(result)
            
            #Verifies Print
            elif i[0] == "=>":
                result=printExe(i)
                route.append(result)

            #Verifies Alter
            elif i[0] == "Alter":
                print("Alter:" , i)

                i[2]=value(i[1])+value(i[2])
                result=changeExe(i)
                route.append(result)
    
            #Verifies Call
            elif i[0] == "Call": 
                if i[2] in proceduresList:
                    result = executeFunc([i[1],procedures[i[1]]])
                    route.append(result)
                else:
                    errorList.append("Error: Cannot call {2} as it does not exist".format(i[2]))              

            elif i[0] == "Proc":#Modifique la lista no es variables sino procs
                if i[1] in proceduresList:
                    errorList.append("Error: Cannot define {1} to procedure {0} as it already exists".format(i[1],i[0]))
                else:
                    result = executeFunc([i[1], i[2]]) #Se toman en cuenta paréntesis
                    route.append(result)


            elif i[0] == "Not":
                print("i del not: " ,i)
                if isinstance(i[1], int):
                    errorList.append("Error: Value is not bool {1}".format(i[1]))
                elif i[1] in globalVars or i[1] in localVars:
                    result = notExe(i[1])
                    route.append(result)
                else:
                    errorList.append("Error: Variable {1} does not exist".format(i[1]))
            
            elif i[0] == "Mover":
                print("Encontro Mover")
                route.append(i[1])
            
            elif i[0]=="Aleatorio":
                print("Encontro Aleatorio")
                listDir=['ATR','ADL','ADE','AIZ','IZQ','DER','DDE','DIZ']
        
                for x in range(11):
                    route.append(random.choice(listDir))
                print("Ruta aleatorio: ", route)
                
            elif i[0] == "Zigzag":
                print("encontro ZigZag")
                listDir=['DER', 'IZQ', 'DER', 'IZQ', 'DER', 'IZQ']
                route.append(listDir)
            
            elif i[0] == "Zagzig":
                listDir=['IZQ', 'DER', 'IZQ', 'DER', 'IZQ', 'DER']
                route.append(listDir)
                
            elif i[0] == "Led":
                print("encontro led")
                route.append(['LED'])
            
            
        elif i=="Aleatorio":
            print("Encontro Aleatorio")
            listDir=['ATR','ADL','ADE','AIZ','IZQ','DER','DDE','DIZ']
        
            for x in range(11):
                route.append(random.choice(listDir))
            print("Ruta aleatorio: ", route)
            
                        
        
    return route

def checkCondition(CONDITION):
    print("la condicion",CONDITION)
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


########### Main route ########################

if AST is not None:
    print("Este es el AST\n", AST)
    for sentence in AST:
        print("Sentencia: ", sentence)
        if isinstance(sentence,list):
            #If Main is found
            print("Sentence0:",sentence[0])
            if sentence[0]=="MAIN":
                if len(sentence)==1:
                    print("Main is declared but empty.")
                
                #Appends the main instructions
                else:
                    if isinstance(sentence[1],list):
                        codeMain+=sentence[1]
                    else:
                        codeMain.append(sentence[1])
                        
            if sentence=="PROC":
                if isinstance(sentence[2],list):
                        codeProcs+=sentence[2]
                else:
                    codeProcs.append(sentence[2])
                
    
    #Filters out invalid productions
    print("Code main antes de conc", codeMain)
    print("Code procs antes de conc", codeProcs)
    if codeProcs != []:
        if isinstance(codeProcs[0],list):
            codeMain+=codeProcs
        else:
            codeMain.append(codeProcs)
            
    
    filter(None,codeMain)
    
    print("Antes de ardino: ", codeMain)
    arduinoOrders= execute(codeMain)
    
else:
    #print("se esta yendo por aca")
    with open(errorFolder,'w+') as errorFile:
       for i in errorList:
           errorFile.write(i + "\n")
            
if validFlag and not(errorFlag):
    print("Code to execute: ", codeMain)
    #print(AST)
    
    print("Code to arduino: ", arduinoOrders)
    
    print("Created procedures: ", procedures)#Dictionary


with open(errorFolder,'w+') as errorFile:
        for i in errorList:
            errorFile.write(i + "\n")

if not validFlag or errorFlag:
    exit()