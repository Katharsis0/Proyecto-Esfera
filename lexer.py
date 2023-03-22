import PLY.lex as lex
from PLY.lex import TOKEN
import re

#list of reserved words
reserved = {
    'Proc' : 'PROC',
    'Def' : 'DEF',
    'Call' : 'CALL',
    'Not' : 'NOT',
    'Alter' : 'ALTER',
    'Mover' : 'MOVER',
    'Aleatorio' : 'ALEATORIO',
    'isTrue' : 'ISTRUE',
    'Repeat' : 'REPEAT',
    'Until' : 'UNTIL',
    'While' : 'WHILE',
    'Case' : 'CASE',
    'When' : 'WHEN',
    'Else' : 'ELSE',
    'True' : 'TRUE',
    'False' : 'FALSE',
    '@Principal' : 'MAIN'}

#list of tokens
tokens = ['LP',
          'RP',
          'INT',
          'ID',
          'COMMA',
          'SEMICOLON',
          'EQUAL',#==
          'LTE',#<= - less or equal
          'GTE',#>= - greater or equal
          'DIF', #>< - different
          'PLUS',
          'MINUS',
          'TYPE',
          'BOOL',
          'STAR',#multiplication
          'SLASH',#division
          'GT',#greater than
          'LT',#less than
            ] + list(reserved.values())


#regular expression rules for matching simple tokens
t_ignore= ' \t'
t_PLUS=r'\+'
t_MINUS=r'\-'
t_STAR=r'\*'
t_SLASH=r'/'
t_LP=r'\('
t_RP=r'\)'
t_EQUAL=r'=='
t_DIFF=r'><'
t_GT=r'>'
t_LT=r'<'
t_GTE=r'>='
t_LTE=r'<='
t_COMMA=r','
t_SEMICOLON=r';'
#t_PRINT=r'=>\s*(.*)'
t_PRINT=r'=>'

#regular expression rules for matching tokens with actions


def t_ID(token):
    #verifies if the ID starts with @, that may 
    #contain alphanumeric characters, # or _
    #cannot be less than 3 chars nor exceed the 10 chars
    r'^@[a-zA-Z0-9_#]{1,8}[a-zA-Z0-9_#]?$'

    #check for reserved words
    if token.value in reserved:
        token.type = reserved[token.value]
    return token

def t_INT(token):
    r'[0-9]+'
    token.value = int(token.value)
    return token

#Defines comment rule
def t_COMMENT(token):
    r'--.*'
    pass#No return value. Token discarded

#Defines print rule
#def t_PRINT(token):
    #pass

#Defines rule to validate value 
def t_BOOL(token):
    r'(True|False)'
    if token.value.isdigit():
        error = "Invalid value '{0}' on line {1} not bool".format(token.value, token.lineno)
    elif token.value == 'True':
        token.value = True
    elif token.value == 'False':
        token.value = False
    return token

def t_TYPE(token):
    r'(int|bool)'
    return token

def t_MAIN(token):
    r'@Principal'
    return token

def t_nl(token):
    r'\n+'
    token.lexer.lineno += token.value.count("\n")
    return token

def t_error(token):
    print("Invalid character '{0} on line {1}'".format(token.value[0], token.lineno))    
    token.lexer.skip(1)

def t_eof(token):
    return None



#Construye el lexer 
lexer=lex.lex()


#Input extraido del IDE
lexer.input("""true""")

#Testing, this should be sent to the IDEs terminal
while True:
    token=lexer.token()

    if not token:
        break

    print("En la linea " + str(token.lineno) + " se encontró el token: "
            + '(' + str(token.type) + ', ' + str(token.value) + ')')
