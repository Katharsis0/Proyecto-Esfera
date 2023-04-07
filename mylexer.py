import ply.lex as lex


reserved={'Def':'DEF',
          'Proc': 'PROC',
          '@Principal': 'MAIN'}

# List of token names.   This is always required
tokens = [
   'INTEGER',
   'PLUS',
   'MINUS',
   'STAR',
   'SLASH',
   'LP',
   'RP',
   'ID'] +list(reserved.values())


# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_STAR   = r'\*'
t_SLASH  = r'/'
t_LP  = r'\('
t_RP  = r'\)'

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
    r'^[@\w#]{2,9}\w?$'
    if t.value in reserved:
        # token.type devuelve los valores de arriba (p.e: token.type devuelve de t_CORCHETEDER : CORCHETEDER)
        t.type = reserved[t.value]
    #Regresa la variable o ID
    return t


# Error handling rule
def t_error(t):
    print ("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
# Build the lexer
lexer = lex.lex()


#Testeo
lexer.input('''@Principal''')
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)