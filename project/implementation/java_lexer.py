import ply.lex as lex

class Tokenizer:
    def __init__(self, tokens):
        self.tokensFound = []
        self.lineNo=0
        # Update reserved with Java-specific keywords
        self.reserved = {
            'if': 'IF', 'else': 'ELSE', 'while': 'WHILE', 'do': 'DO', 'for': 'FOR',
            'int': 'INT', 'char': 'CHAR', 'float': 'FLOAT', 'double': 'DOUBLE',
            'boolean': 'BOOLEAN', 'void': 'VOID', 'class': 'CLASS',
            'public': 'PUBLIC', 'private': 'PRIVATE', 'protected': 'PROTECTED',
            'static': 'STATIC', 'final': 'FINAL', 'this': 'THIS', 'super': 'SUPER', 'return': 'RETURN',
            'import': 'IMPORT', 'package': 'PACKAGE', 'default': 'DEFAULT', 'switch': 'SWITCH', 'main': 'MAIN',  'System.out.println': 'PRINTFUNC'
        }
        self.tokens = tokens + list(self.reserved.values())

    def get_tokens(self):
        return self.tokens

    # Update token regex patterns for Java
    t_NUMBER = r'\d+(\.\d+)?'
    t_ignore = ' \t\n'
    t_STRING_LITRAL = r'\"(\\.|[^"])*\"'
    t_COMMENT = r'//.*|/\*(.|\n)*?\*/'
    t_LOGICAL_LE = r'<='
    t_LOGICAL_GE = r'>='
    t_LOGICAL_EET = r'=='
    t_LOGICAL_NE = r'!='
    t_LOGICAL_AND = r'&&'
    t_NOT = r'!'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULTIPLE = r'\*'
    t_DIVIDE = r'\/'
    t_SEMI_COLON = r';'
    t_ASSIGNMENT = r'='
    t_COMMA = r','
    t_RPAR = r'\)'
    t_LPAR = r'\('
    t_LBRA = r'\{'
    t_RBRA = r'\}'
    t_LBK = r'\['
    t_RBK = r'\]'
    t_LOGICAL_OR = r'\|\|'
    t_GREATER_THEN = r'>'
    t_LESSER_THEN = r'<'
    t_DOT=r'\.'
    
    def t_error(self, t):
        print(f"Illegal character: {t.value[0]} in line {self.lineNo} at position {t.lexpos}")
        
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    # Test the lexer
    def test(self, data,lineNo):
        #input source code for analysis
        self.lineNo=lineNo
        self.lexer.input(data)
        #get the tokens and info(type,vale) from lexer and process it 
        while True:
            token = self.lexer.token()
            if not token:
                break
            else:
              token.lineno=lineNo
            # print(token)
            self.tokensFound.append(token.type)
        #display all lexems
        # print(self.tokensFound)
        return self.tokensFound