from src.token_type import *
from src.token import Token

RESERVED_KEYWORDS = {
    'PROGRAM': Token(PROGRAM, 'PROGRAM'),
    'VAR': Token(VAR, 'VAR'),
    'DIV': Token(INTEGER_DIV, 'DIV'),
    'INTEGER': Token(INTEGER, 'INTEGER'),
    'REAL': Token(REAL, 'REAL'),
    'BEGIN': Token(BEGIN, 'BEGIN'),
    'END': Token(END, 'END'),
    'PROCEDURE': Token(PROCEDURE, 'PROCEDURE')
}

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

    def advance(self):
        """
        Move to one more position to check for assignment or equal operators
        """
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        else:
            return self.text[peek_pos]

    def skip_comments(self):
        """
        Skip comments in the input
        Comment has the form of # comment #
        """
        while self.current_char != "@":
            self.next()
        self.next() # skip the last @

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
            return Token(REAL_CONST, float(result))
        else:
            return Token(INTEGER_CONST, int(result))

    def id_keywords(self):
        """
        Handle ids and reserved keywords
        """
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.next()
        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def create_tokens(self):
        """
        Initialize a steam of tokens from the user input
        :return: the set of tokens
        """
        while self.current_char:
            #handle comments
            if self.current_char == "@":
                self.next()
                self.skip_comments()
            #handle spaces
            elif self.current_char.isspace():
                self.skip_whitespaces()
            #handle keywords and ids
            elif self.current_char.isalpha():
                self.tokens.append(self.id_keywords())
            #handle numbers
            elif self.current_char.isdigit():
                self.tokens.append(self.multi_digit_number())
            # handle := assignment
            elif self.current_char == ":" and self.advance() == "=":
                self.next()
                self.next()
                self.tokens.append(Token(ASSIGN, ":="))
            #handle colon
            elif self.current_char == ":":
                self.next()
                self.tokens.append(Token(COLON, ":"))
            #handle comma
            elif self.current_char == ",":
                self.next()
                self.tokens.append(Token(COMMA, ","))
            #handle semi
            elif self.current_char == ";":
                self.next()
                self.tokens.append(Token(SEMI, ";"))
            #handle dot
            elif self.current_char == ".":
                self.next()
                self.tokens.append(Token(DOT, "."))
            #handle +, - , * , / and ()
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
                self.tokens.append(Token(FLOAT_DIV, "/"))
            elif self.current_char == "(":
                self.next()
                self.tokens.append(Token(LPAREN, "("))
            elif self.current_char == ")":
                self.next()
                self.tokens.append(Token(RPAREN, ")"))
            else:
                print(self.current_char)
                self.tokenizer_error(self.current_char)
        self.tokens.append(Token(EOF, None))
        return self.tokens