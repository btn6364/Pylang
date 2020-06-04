from src.token_type import *
from src.ast import *


"""
Parser that will parse the tokens array
"""
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0
        self.current_token = self.tokens[self.token_idx]

    def parser_error(self):
        raise Exception("[ERROR]: Parser error")

    def get_next_token(self):
        """
        Get the next token in the token array.
        """
        self.token_idx += 1
        return self.tokens[self.token_idx]

    def eat(self, token_type):
        """
        Consume the current token if it matches the token type. Then set the current token to the next one.
        """
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.parser_error()

    def program(self):
        """
        Program: PROGRAM variable SEMI block DOT
        """
        self.eat(PROGRAM)
        var_node = self.variable()
        program_name = var_node.value
        self.eat(SEMI)
        block_node = self.block()
        program_node = Program(program_name, block_node)
        self.eat(DOT)
        return program_node

    def block(self):
        """
        block: declarations compound_statement
        """
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node

    def declarations(self):
        """
        declarations: VAR (variable_declaration SEMI)+
                     | (PROCEDURE ID (LPAREN parameter_list RPAREN)? SEMI block SEMI)*
                     | empty
        """
        declarations = []
        while True:
            if self.current_token.type == VAR:
                self.eat(VAR)
                while self.current_token.type == ID:
                    var_declarations = self.variable_declaration()
                    declarations.extend(var_declarations)
                    self.eat(SEMI)
            elif self.current_token.type == PROCEDURE:
                self.eat(PROCEDURE)
                procedure_name = self.current_token.value
                self.eat(ID)
                if self.current_token.type == LPAREN:
                    self.eat(LPAREN)
                    param_nodes = self.formal_parameter_list()
                    self.eat(RPAREN)

                self.eat(SEMI)
                block_node = self.block()
                procedure_declaration = ProcedureDeclaration(procedure_name=procedure_name, param_nodes=param_nodes, block_node=block_node)
                declarations.append(procedure_declaration)
                self.eat(SEMI)
            else:
                break
        return declarations


    def formal_parameter_list(self):
        """
        formal_parameter_list: formal_parameters
                             | formal_parameters SEMI formal_parameter_list
                             | empty
        """
        if self.current_token.type != ID:
            return []

        param_nodes = self.formal_parameters()
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            param_nodes.extend(self.formal_parameters())

        return param_nodes


    def formal_parameters(self):
        """
        formal_parameters: ID (COMMA ID))* COLON type_spec
        Ex: x, y, z: INTEGER
        """
        param_nodes = []

        param_tokens = [self.current_token]
        self.eat(ID)
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            param_tokens.append(self.current_token)
            self.eat(ID)

        self.eat(COLON)
        type_node = self.type_spec()

        for param_token in param_tokens:
            param_node = Param(Var(param_token), type_node)
            param_nodes.append(param_node)

        return param_nodes


    def variable_declaration(self):
        """
        variable_declaration: ID (COMMA ID)* COLON type_spec
        """
        var_nodes = [Var(self.current_token)]
        self.eat(ID)

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)
        self.eat(COLON)

        type_node = self.type_spec()
        var_declarations = [
            VariableDeclaration(var_node, type_node) for var_node in var_nodes
        ]
        return var_declarations

    def type_spec(self):
        """
        type_spec: INTEGER | REAL
        """
        token = self.current_token
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
        else:
            self.eat(REAL)
        node = Type(token)
        return node

    def compound_statement(self):
        """
        Compound_statement: BEGIN statement_list END
        """
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """
        statement_list: statement | statement SEMI statement_list
        """
        node = self.statement()
        results = [node]
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())
        if self.current_token.type == ID:
            self.parser_error()
        return results

    def statement(self):
        """
        statement: compound_statement | assignment_statement | empty
        """
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        """
        assignement_statement: variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable: ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        """
        Empty production
        """
        return NoOp()

    def factor(self):
        """
        Rule: factor: PLUS factor | MINUS factor | INTEGER | FLOAT | LPAREN expr RPAREN | variable
        """
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type in (INTEGER_CONST, REAL_CONST):
            self.eat(token.type)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def term(self):
        """
        Rule: term: factor ((MUL|DIV) factor)*
        """
        node = self.factor()
        while self.current_token.type in (MULTIPLY, INTEGER_DIV, FLOAT_DIV):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
            elif token.type == INTEGER_DIV:
                self.eat(INTEGER_DIV)
            elif token.type == FLOAT_DIV:
                self.eat(FLOAT_DIV)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        """
        Rule: expr: term ((PLUS|MINUS) term)*
        """
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def parse(self):
        """
        Parse the lexer into a AST
        """
        node = self.program()
        if self.current_token.type != EOF:
            raise Exception("Expect end of the program here!")

        return node