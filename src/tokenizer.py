from src.token_type import INTEGER, FLOAT, PLUS, MINUS, MULTIPLY, DIVIDE, EOF
from src.token import Token

"""
The tokenizer that will break the code down into a stream of tokens.
"""
class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.tokens = []

    def tokenizer_error(self, detail):
        raise Exception(f"[ERROR]: {detail} is not defined")

    def next(self):
        """
        Move the pos pointer by 1 position and set the current_char
        """
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespaces(self):
        """
        Skip whitespaces in the input
        """
        while self.current_char is not None and self.current_char.isspace():
            self.next()

    def multi_digit_number(self):
        """
        Construct multiple-digit numbers
        """
        result = ""
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == "."):
            result += self.current_char
            self.next()
        if "." in result:
            return Token(FLOAT, float(result))
        else:
            return Token(INTEGER, int(result))

    def create_tokens(self):
        """
        Initialize a steam of tokens from the user input
        :return: the set of tokens
        """
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespaces()
            elif self.current_char.isdigit():
                self.tokens.append(self.multi_digit_number())
            elif self.current_char == "+":
                self.next()
                self.tokens.append(Token(PLUS, "+"))
            elif self.current_char == "-":
                self.next()
                self.tokens.append(Token(MINUS, "-"))
            elif self.current_char == "*":
                self.next()
                self.tokens.append(Token(MULTIPLY, "*"))
            elif self.current_char == "/":
                self.next()
                self.tokens.append(Token(DIVIDE, "/"))
            else:
                self.tokenizer_error(self.current_char)
        self.tokens.append(Token(EOF, None))
        return self.tokens