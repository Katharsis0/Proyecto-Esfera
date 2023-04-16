#Proceso de analisis semántico

from myparser import commentList
from myparser import commentNumber
from myparser import main
from myparser import errorList
from myparser import res as AST
from myparser import proceduresList
from myparser import procedures
from myparser import printsList



#Flag for error verification
errorFlag=False


###Semantic Analysis###

if commentNumber == 0:
    errorFlag = True
    errorList.append("Error: The program must have at least one comment.")

elif commentNumber > 0 and AST is not None:
    if commentList[0] != AST[0]:
        errorFlag = True
        errorList.append("Error: The program must start with at least one comment.")
    for comment in commentList:
        if comment in AST:
            AST.remove(comment)

elif main == 0:
    errorFlag = True
    errorList.append("Error: The program must contain at least one @Principal() procedure.")

if len(errorList) != 0:
    errorFlag = True
    errorList.append("\nError: Program cannot be executed until errors are solved.\n")


if AST is not None:
    AST = list(filter(None, AST))[0]




