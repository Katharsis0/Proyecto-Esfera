import lexer
import parse 


#Test

inputString= "1 + 2"
lexer_init= lexer.lex()
parser_init= parse.yacc()

parse_tree=parser_init.parse(inputString,lexer=lexer_init)

