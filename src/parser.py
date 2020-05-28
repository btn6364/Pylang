from src.token_type import PLUS, MINUS, MULTIPLY, DIVIDE

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
        self.eat(token.type)
        return token.value

    def term(self):
        """
        Rule: term: factor ((MUL|DIV) factor)*
        """
        result = self.factor()
        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result *= self.factor()
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                result /= self.factor()
        return result

    def expr(self):
        """
        Rule: expr: term ((PLUS|MINUS) term)*
        """
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result

    def parse(self):
        """
        Parse the lexer
        """
        return self.expr()