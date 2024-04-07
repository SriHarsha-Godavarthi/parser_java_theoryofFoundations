# # import yacc to do the parsing which generates ast tree
# import ply.yacc as yacc

# # abstract syntax treeNode
# class ASTNode:
#     def __init__(self, type, children=None, value=None):
#         self.type = type
#         self.children = children if children is not None else []
#         self.value = value

# class Parser:

#     def __init__(self,tokens,source_code,lexer):
#         #store tokens,code to execute,build lexer
#         self.tokens=tokens
#         #get lexer output
#         self.lexer=lexer.input(source_code)
#         self.input=source_code
#         self.parser=yacc
#         self.AstLevels={}
#         # give precedence for operators
#         self.precedence = (
#             ('left', 'LOGICAL_EET', 'LOGICAL_NE', 'LOGICAL_LE', 'LESSER_THEN', 'LOGICAL_GE', 'GREATER_THEN'),
#             ('left', 'PLUS', 'MINUS'),
#             ('left', 'MULTIPLE', 'DIVIDE'),
#             ('right', 'NOT'),
#         )
        
#         # define context free grammar using p_{rulename} i.e.(ruleName - non terminal, tokens - terminals)
#     # Program Structure
#     def p_program( self,p):
#         'program : classDeclaration'
#         p[0] = p[1]

#     def p_class_declaration( self,p):
#         'classDeclaration : PUBLIC CLASS IDENTIFIER LBRA classBody RBRA'
#         p[0] = ('class_declaration', p[3], p[5])

#     def p_class_body( self,p):
#         '''classBody : classBodyDeclaration
#                     | empty'''
#         p[0] = p[1]

#     def p_class_body_declaration( self,p):
#         '''classBodyDeclaration : methodDeclaration
#                                 | classBodyDeclaration classBodyDeclaration'''
#         if len(p) == 3:
#             p[0] = (p[1], p[2])
#         else:
#             p[0] = p[1]

#     # Method and Field Declarations
#     def p_method_declaration( self,p):
#         'methodDeclaration : type IDENTIFIER LPAR parameters RPAR LBRA statement RBRA'
#         p[0] = ('methodDeclaration', p[1], p[2], p[4], p[7])
#     # Statements
#     # def p_statement(self,p):
#     #     '''statement : if_statement
#     #                  | while_statement
#     #                  | assignment
#     #                  | print_statement'''
#     def p_statement_if(self,p):
#         '''ifStatement : IF LPAR expression RPAR statement ELSE statement'''
#         p[0] = ('ifStatement', p[3], p[6], p[8])

#     def p_statement_while(self,p):
#         '''whileStatement : WHILE LPAR expression RPAR statement'''
#         p[0] = ('whileStatement', p[3], p[6])
        
#     def p_statement_for(self,p):
#         '''forStatement : FOR LPAR type expression SEMI_COLON expression SEMI_COLON  expression operator operator RPAR'''

#     def p_statement_assignment(self,p):
#         '''assignment : IDENTIFIER ASSIGNMENT expression'''
#         p[0] = ('assignment', p[1], p[3])

#     def p_statement_print(self,p):
#         '''printStatement : PRINTFUNC LPAR expression RPAR SEMI_COLON'''
#         p[0] = ('printStatement', p[3])
    
#     def p_parameters( self,p):
#         '''parameters : type IDENTIFIER COMMA parameters
#                     | type IDENTIFIER
#                     | empty'''
#         if len(p) == 3:
#             p[0] = ('parameters', p[1], p[2])
#         elif len(p) == 5:
#             p[0] = ('parameters', p[1], p[2], p[4])
#         else:
#             p[0] = ('empty')

#     def p_type( self,p):
#         '''type : INT
#                 | CHAR
#                 | BOOLEAN
#                 | VOID
#                 | FLOAT
#                 | DOUBLE
#                 | IDENTIFIER'''
#         p[0] = p[1]

#     # Statements
#     def p_statement( self,p):
#         '''statement : ifStatement
#                     | whileStatement
#                     | assignment
#                     | printStatement
#                     | statement statement'''
#         if len(p) == 3:
#             p[0] = ('statements', p[1], p[2])
#         else:
#             p[0] = p[1]

#     # Expressions (This is a simplified version; extend as needed)
#     def p_expression( self,p):
#         '''expression : expression operator expression
#                     | LPAR expression RPAR
#                     | IDENTIFIER
#                     | NUMBER
#                     | STRING_LITRAL'''
#         if len(p) == 4:
#             if p[1] == '(':
#                 p[0] = p[2]
#             else:
#                 p[0] = ('expression', p[1], p[2], p[3])
#         else:
#             p[0] = p[1]

#     def p_operator( self,p):
#         '''operator : PLUS
#                     | MINUS
#                     | MULTIPLE
#                     | DIVIDE
#                     | LOGICAL_LE
#                     | LOGICAL_GE
#                     | LOGICAL_EET
#                     | LOGICAL_NE
#                     | LESSER_THEN
#                     | GREATER_THEN
#                     | LOGICAL_AND
#                     | LOGICAL_OR'''
#         p[0] = p[1]

#     # Empty production
#     def p_empty( self,p):
#         'empty :'
#         pass

#     # Error rule for syntax errors
#     def p_error( self,p):
#         print(f"Syntax error in input at {p}")
        
#     def build_parser(self):
#             tokens=self.tokens
#             try:
#                 # for debugging add debug=True,
#                 self.parser.yacc(module=self, start='program',debug=True)
#                 #get parser tree from parser
#                 parse_tree=self.parser.parse(self.input,lexer=self.lexer,debug=True)
#                 # return parse_tree
#                 #dictonary
#                 print("AST PARSE TREE:",parse_tree)
#             except Exception as e:
#                 print(f"An unexpected error occurred: {e}")