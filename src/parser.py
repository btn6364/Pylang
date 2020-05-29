from src.token_type import INTEGER, FLOAT, PLUS, MINUS, MULTIPLY, DIVIDE, LPAREN, RPAREN, \
                           DOT, BEGIN, END, DOT, ASSIGN, ID, SEMI, EOF
from src.ast import UnaryOp, BinOp, Num, NoOp, Compound, Assign, Var


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
        Program: BEGIN compound statement
        """
        node = self.compound_statement()
        self.eat(DOT)
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
        elif token.type in (INTEGER, FLOAT):
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
        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
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