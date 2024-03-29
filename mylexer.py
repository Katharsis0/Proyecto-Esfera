import ply.lex as lex

# reserved={ 'Def' : 'DEF',
#            'Proc' : 'PROC',
#            '@Principal' : 'MAIN',
#            'Call': 'CALL',
#            'Not': 'NOT',
#            'Alter': 'ALTER',
#            'Mover': 'MOVER',
#            'Aleatorio': 'ALEATORIO',
#            'isTrue': 'ISTRUE',
#            'Repeat': 'REPEAT',
#            'Until': 'UNTIL',
#            'While': 'WHILE',
#            'Case': 'CASE',
#            'When': 'WHEN',
#            'Else': 'ELSE',
#            'Then': 'THEN',
#            'True': 'TRUE',
#            'False': 'FALSE',
#            'Print' : 'PRINT'}



# List of token names.   This is always required
tokens = [
   'INTEGER',
   'PLUS',
   'MINUS',
   'STAR',
   'SLASH',
   'LP',
   'RP',
   'COMMENT',
   'ID', #+list(reserved.values())
   'COMMA',
   'SEMICOLON',
   'EQUAL',#==
   'LTE',#<= - less or equal
   'GTE',#>= - greater or equal
   'DIF', #>< - different
   #'UMINUS',
   'TYPE',
   'BOOL',
   'GT',#greater than
   'LT',#less than
   'DIR', #Direction

    #Tokens Reserved
    'DEF',
   'PROC',
   'MAIN',
   'CALL',
   'NOT',
   'ALTER',
   'MOVER',
   'ALEATORIO',
   'ISTRUE',
   'REPEAT',
   'UNTIL',
   'WHILE',
   'CASE',
   'WHEN',
   'ELSE',
   'THEN',
   'PRINT',
    'VALUE',
    'CHANGE',
    'STRING',
    'BREAK',
    'LED',
    'TROMPO',
    'CIRCULO',
]



#tokens += list(reserved.values())


# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_SLASH = r'/'
t_LP = r'\('
t_RP = r'\)'
t_COMMA = r'\,'
t_DIR = r'ATR|ADL|ADE|AIZ|IZQ|DER|DDE|DIZ'
t_SEMICOLON = r';'
t_DIF=r'><'
t_GT=r'>'
t_LT=r'<'
t_GTE=r'>='
t_LTE=r'<='
t_EQUAL = r'=='



#Reserved
t_DEF = r'Def'
t_PROC = r'Proc'
t_MAIN = r'@Principal' #Lo reconoce como ID
t_CALL = r'Call'
t_NOT = r'Not'
t_ALTER = r'Alter'
t_MOVER = r'Mover'
t_ALEATORIO = r'Aleatorio'
t_ISTRUE = r'IsTrue'
t_REPEAT = r'Repeat'
t_UNTIL = r'Until'
t_WHILE = r'While'
t_CASE = r'Case'
t_WHEN = r'When'
t_ELSE = r'Else'
t_THEN = r'Then'
t_PRINT = r'=>'
t_CHANGE = r'Change'
t_STRING = r'\"[^\"]*\"'
t_BREAK = r'Break'
#func opcionales
t_LED= r'Led'
t_TROMPO = r'Trompo'
t_CIRCULO = r'Circulo'




#Token int
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


#Token ID or reserved word. If its reserved word return its value.

def t_ID(t):
    r'@[a-zA-Z][a-zA-Z0-9_]*'
    if t.value == '@Principal':
        t.type = 'MAIN'
    else:
        t.type = 'ID'
    return t


def t_COMMENT(token):
    r'--.*'
    return token

def t_TYPE(t):
    r'(int | bool)'
    t.type = 'TYPE'
    return t

def t_BOOL(t):
    r'(True|False)'
    if t.value == 'True':
        t.value = True
    elif t.value == 'False':
        t.value = False
    t.type = 'BOOL'
    return t

# Error handling rule
def t_error(t):
    print ("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
# Build the lexer
lexer = lex.lex()

#Open the input file and read its contents
with open('./Tests/Pruebas/edad.sfra', 'r') as f:
    input_string = f.read()

#Pass the input string to the lexer
lexer.input(input_string)

#Tokenize the input and print the resulting tokens
while True:
    tok = lexer.token()
    if not tok:
        break
    #print(tok)