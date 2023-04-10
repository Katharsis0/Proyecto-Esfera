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
   'LSB', #left square bracket '['
   'RSB', #right square bracket ']'
   'COMMA',
   'SEMICOLON',
   'EQUAL',#==
   'LTE',#<= - less or equal
   'GTE',#>= - greater or equal
   'DIF', #>< - different
   'UMINUS',
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
   'TRUE',
   'FALSE',
   'PRINT'
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

#Reserved
t_DEF = r'Def'
t_PROC = r'Proc'
t_MAIN = r'@Principal' #Lo reconoce como ID
t_CALL = r'Call'
t_NOT = r'Not'
t_ALTER = r'Alter'
t_MOVER = r'Mover'
t_ALEATORIO = r'Aleatorio'
t_ISTRUE = r'isTrue'
t_REPEAT = r'Repeat'
t_UNTIL = r'Until'
t_WHILE = r'While'
t_CASE = r'Case'
t_WHEN = r'When'
t_ELSE = r'Else'
t_THEN = r'Then'
t_TRUE = r'True'
t_FALSE = r'False'
t_PRINT = r'Print'


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
#TODO: Validar en el parser que si es un ID inicie con @.
def t_ID(t):
    #r'^@?\w[\w#@]*$'
    #r'^[@\w#]{2,9}\w?$'
    #r'^[@\w#]{2,9}\w?$'
    #if t.value in reserved:
        # token.type devuelve los valores de arriba (p.e: token.type devuelve de t_CORCHETEDER : CORCHETEDER)
     #   t.type = reserved[t.value]
    #Regresa la variable o ID
    #return t
    r'^@[A-Za-z0-9#-]{3,9}$'

    #r'^[@\w#]{2,9}\w?$'
    #if t.value in reserved:
        # token.type devuelve los valores de arriba (p.e: token.type devuelve de t_CORCHETEDER : CORCHETEDER)
       # t.type = reserved[t.value]
        #Regresa la variable o ID
    return t


def t_COMMENT(token):
    r'--.*'
    return token

# Error handling rule
def t_error(t):
    print ("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
# Build the lexer
lexer = lex.lex()



#Testeo
lexer.input(''';''')
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)