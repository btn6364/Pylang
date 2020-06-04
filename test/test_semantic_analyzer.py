import sys
from src.tokenizer import Tokenizer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer

def process(filename):
    with open(filename) as file:
        text = file.read()
        if not text:
            raise Exception("Cannot read text from file")
        tokenizer = Tokenizer(text)
        parser = Parser(tokenizer.create_tokens())
        tree = parser.parse()
        symbol_table_builder = SemanticAnalyzer()
        symbol_table_builder.visit(tree)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        raise Exception("Missing source file")
    if len(sys.argv) > 2:
        raise Exception("Too many arguments")
    filename = sys.argv[1]
    process(filename)

