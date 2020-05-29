from src.token_type import INTEGER, FLOAT, PLUS, MINUS, MULTIPLY, DIVIDE, LPAREN, RPAREN

"""
Abstract syntax tree
"""
class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

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

    def factor(self):
        """
        Rule: factor: INTEGER|FLOAT
        """
        token = self.current_token
        if token.type in (INTEGER, FLOAT):
            self.eat(token.type)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
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
        return self.expr()