from src.tokenizer import Tokenizer
from src.parser import Parser

"""
The interpreter that will interpret the code
"""

class Interpreter():
    def __init__(self, text):
        """
        :param text: client input
        """
        self.text = text
        self.tokenizer = Tokenizer(self.text)
        self.parser = Parser(self.tokenizer.create_tokens())

    def error(self):
        raise Exception("[ERROR]: Interpreter error")

    def interpret(self):
        return self.parser.parse()

