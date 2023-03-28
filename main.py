import lexer
import parsing 


#Test

inputString= "1 + 2"
lexer_init= lexer.lex()
parser_init= parsing.yacc()

parse_tree=parser_init.parse(inputString,lexer=lexer_init)

