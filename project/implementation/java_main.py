from java_lexer import Tokenizer
from java_parser import Parser

def main():
    tokens = [
        'STRING_LITRAL',
        'IDENTIFIER', # any letter (letter | number)*
        'LOGICAL_LE', # <= 
        'LOGICAL_GE', # >=
        'LOGICAL_EET', # ==
        'LOGICAL_NE',  # !=
        'LOGICAL_AND', # &&
        'LOGICAL_OR', # ||
        'GREATER_THEN', # >
        'LESSER_THEN', # <
        'PLUS', # +
        'MINUS', # -
        'MULTIPLE', # *
        'DIVIDE', # %
        'SEMI_COLON', # ;
        'COMMA', # ,
        'LPAR', # )
        'RPAR', # (
        'LBRA', # {
        'RBRA', # }
        'COMMENT', # /* ... */,
        'NOT', # !
        'ASSIGNMENT',
        'LBK', # [
        'RBK', # ]
        'NUMBER',
        'EMPTY', # empty string,
        'DOT'
    ]
    # call tokenizer class which has lexer 
    lexical_analyzer=Tokenizer(tokens)
    #build lexer
    tokens=lexical_analyzer.get_tokens()
    lexer=lexical_analyzer.build()
    with open("./java_input.txt", "r") as file_data:
        #source_code = file_data.read()
        source_code=''
        lineNo=1
        for line in file_data:
        #   print(line)
          source_code+=line
          tokens_rec = lexical_analyzer.test(line.strip(),lineNo)
          lineNo+=1
    # initialize parser and build it to generate parse tree 
    # which uses shif reduce parser
    parser_build=Parser(tokens,source_code,lexer)
    # check wheather written program is correct or not
    parse_tree=parser_build.build_parser() 
    # print(lexical_analyzer.tokensFound)
    # print("######parser Tree########")
    # print(parse_tree)
    
main()