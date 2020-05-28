from src.token_type import PLUS, MINUS, MULTIPLY, DIVIDE

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.current_token = None

    def parser_error(self):
        raise Exception("[ERROR]: Parser error")

    def get_next_token(self):
        self.token_idx += 1
        return self.tokens[self.token_idx]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.parser_error()

    def term(self):
        """
        Return an INTEGER or FLOAT value
        """
        token = self.current_token
        self.eat(token.type)
        return token.value

    def expr(self):
        """
        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER
        """
        self.current_token = self.get_next_token()

        result = self.term()
        while self.current_token.type in (PLUS, MINUS, MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
            elif token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result *= self.term()
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                result /= self.term()
        return result

    def parse(self):
        return self.expr()