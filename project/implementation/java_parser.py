

import ply.yacc as yacc
from collections import deque

class ASTNode:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children if children is not None else []
        self.value = value
        
class Parser:

    def __init__(self,tokens,source_code,lexer):
        #store tokens,code to execute,build lexer
        self.tokens=tokens
        #get lexer output
        self.lexer=lexer.input(source_code)
        self.input=source_code
        self.parser=yacc
        self.AstLevels={}
        self.derivations = []
        # give precedence for operators
        self.precedence = (
            ('left', 'LOGICAL_EET', 'LOGICAL_NE', 'LOGICAL_LE', 'LESSER_THEN', 'LOGICAL_GE', 'GREATER_THEN'),
            ('left', 'PLUS', 'MINUS'),
            ('left', 'MULTIPLE', 'DIVIDE'),
            ('right', 'NOT'),
        )

    # Program Structure
    def p_program(self,p):
        '''program : class_declaration'''
        p[0] = ASTNode('program', [p[1]])

    def p_class_declaration(self,p):
        '''class_declaration : CLASS IDENTIFIER LBRA class_body RBRA'''
        p[0] = ASTNode('class_declaration', [ASTNode('CLASS',value=p[1]),ASTNode('IDENTIFIER',value=p[2]),ASTNode('LBRA',value=p[3]),p[4],ASTNode('RBRA',value=p[5])])

    def p_class_body(self,p):
        '''class_body : method_declaration
                    | field_declaration
                    | empty'''
        p[0] = ASTNode('class_body', [p[1]])
    
    def p_method_declaration(self,p):
        '''method_declaration : type IDENTIFIER LPAR parameter_list RPAR LBRA statement RBRA'''
        p[0] = ASTNode('method_declaration', [p[1], ASTNode('IDENTIFIER',value=p[2]),ASTNode('LPAR',value=p[3]), p[4],ASTNode('RPAR',value=p[5]),ASTNode('LBRA',value=p[6]), p[7],ASTNode('RBRA',value=p[8])])
        
    def p_statement(self,p):
        '''statement : while_statement
                    | if_statement
                    | assignment_statement
                    | method_call_statement
                    | block'''
        p[0] = ASTNode('statement', [p[1]])

    def p_block(self,p):
        '''block : LBRA statement RBRA'''
        p[0] = ASTNode('block', [ASTNode('LBRA',value=p[1]),p[2],ASTNode('RBRA',value=p[3])])

    def p_while_statement(self,p):
        '''while_statement : WHILE LPAR expression RPAR statement'''
        p[0] = ASTNode('while_statement', [ASTNode('WHILE',value=p[1]),ASTNode('LPAR',value=p[2]),p[3],ASTNode('RPAR',value=p[4]), p[5]])

    def p_if_statement(self,p):
        '''if_statement : IF LPAR expression RPAR statement else_statement'''
        p[0] = ASTNode('if_statement', [ASTNode('IF',value=p[1]),ASTNode('LPAR',value=p[2]),p[3],ASTNode('RPAR',value=p[4]), p[5], p[6]])

    def p_else_statement(self,p):
        '''else_statement : ELSE statement
                        | empty'''
        if len(p) == 3:
            p[0] = ASTNode('else_statement', [ASTNode('ELSE',value=p[1]),p[2]])
        else:
            p[0] = ASTNode('else_statement', [p[1]])

    def p_assignment_statement(self,p):
        '''assignment_statement : IDENTIFIER ASSIGNMENT expression SEMI_COLON'''
        p[0] = ASTNode('assignment_statement',[ ASTNode('IDENTIFIER',value=p[1]),ASTNode('ASSIGNMENT',value=p[2]) ,p[3],ASTNode('SEMI_COLON',value=p[4])])

    def p_method_call_statement(self,p):
        '''method_call_statement : IDENTIFIER LPAR argument_list RPAR SEMI_COLON'''
        p[0] = ASTNode('method_call_statement', [ASTNode('IDENTIFIER',value=p[1]),ASTNode('LPAR',value=p[2]),p[3],ASTNode('RPAR',value=p[4]),ASTNode('SEMI_COLON',value=p[5])])
    
        # Expressions (This is a simplified version; extend as needed)
    def p_expression( self,p):
        '''expression : expression operator expression
                    | LPAR expression RPAR
                    | IDENTIFIER
                    | NUMBER
                    | STRING_LITRAL'''
        if len(p)==2:
            p[0]=ASTNode('expression',[ASTNode('identifier/number/string_literal',value=p[1])])
        elif len(p)==4:
            if p[1]=='(':
                p[0]=ASTNode('expression',[ASTNode('LPAR',value=p[1]),p[2],ASTNode('RPAR',value=p[3])])
            else:
                p[0]=ASTNode('expression',[p[1],p[2],p[3]])

    def p_argument_list(self,p):
        '''argument_list : expression
                        | expression COMMA argument_list
                        | empty'''
        # This is a simplification. Normally, you'd build a list of arguments.
        if len(p) == 2:
            p[0] = ASTNode('argument_list', [p[1]])
        elif len(p) > 3:
            p[0] = ASTNode('argument_list', [p[1],ASTNode('COMMA',value=p[2]) ,p[3]])

    def p_return_statement(self,p):
        '''return_statement : RETURN expression SEMI_COLON
                            | RETURN SEMI_COLON'''
        if len(p) == 4:
            p[0] = ASTNode('return_statement', [ASTNode('RETURN',value=p[1]),p[2],ASTNode('SEMI_COLON',value=p[3])])
        else:
            p[0] = ASTNode('return_statement', [ASTNode('RETURN',value=p[1]),ASTNode('SEMI_COLON',value=p[2])])
             
    def p_field_declaration(self,p):
        '''field_declaration : type IDENTIFIER SEMI_COLON'''
        p[0] = ASTNode('field_declaration', p[1], ASTNode('IDENTIFIER',value=p[2]),ASTNode('SEMI_COLON',value=p[3]))

    def p_parameter_list(self,p):
        '''parameter_list : type IDENTIFIER
                        | type IDENTIFIER COMMA parameter_list
                        | empty'''
        # This is simplified. You might want to create a list of parameters.
        if len(p) == 3:
            p[0] = ASTNode('parameter', [p[1], ASTNode('IDENTIFIER',value=p[2])])
        elif len(p) > 3:
            p[0] = ASTNode('parameter_list',[ p[1], ASTNode('IDENTIFIER',value=p[2]),ASTNode('COMMA',value=p[3]), p[4]])
        
            
    def p_type( self,p):
        '''type : INT
                | CHAR
                | BOOLEAN
                | VOID
                | FLOAT
                | DOUBLE
                | IDENTIFIER'''
        p[0] = ASTNode('type',value=p[1])            
    def p_operator( self,p):
        '''operator : PLUS
                    | MINUS
                    | MULTIPLE
                    | DIVIDE
                    | LOGICAL_LE
                    | LOGICAL_GE
                    | LOGICAL_EET
                    | LOGICAL_NE
                    | LESSER_THEN
                    | GREATER_THEN
                    | LOGICAL_AND
                    | LOGICAL_OR'''
        p[0] = ASTNode('operator',value=p[1])
    def print_ast(self, node, level):
        try:
                # print(node)
                if node is not None:
                    # print(node.value)
                    if  node.type is not None:
                        if level not in self.AstLevels:
                            # If not, initialize it with an empty string
                            self.AstLevels[level] = node.type
                        else:
                            self.AstLevels[level] = self.AstLevels[level] + " " + node.type 
                    for child in node.children:
                        self.print_ast(child, level + 1)
        except Exception as e:
            # print('Exception node',node)
            print(f"An unexpected error occurred: {e}")
    # Empty production
    def p_empty( self,p):
        'empty :'
        pass

    # Error rule for syntax errors
    def p_error( self,p):
        
        print(f"Syntax error in input at {p}")

    def build_parser(self):
        try:
            self.parser.yacc(module=self, start='program', debug=True)
            parse_tree=self.parser.parse(self.input,lexer=self.lexer,debug=True)
            #print AST tree
            self.print_ast(parse_tree, 0)
             #dictonary
            print("AST PARSE TREE:")
            for item in sorted(list(self.AstLevels.keys())):
                print(f"level {item}: ",self.AstLevels[item])
            # print("print AST levels for each shift and reduce \n",type(parse_tree))
        except Exception as e:
            print(f"An unexpected error occurred: {e}")