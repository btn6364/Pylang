import sys
from src.tokenizer import Tokenizer
from src.parser import Parser
from src.symbol import SymbolTableBuilder

def process(filename):
    with open(filename) as file:
        text = file.read()
        if not text:
            raise Exception("Cannot read text from file")
        tokenizer = Tokenizer(text)
        parser = Parser(tokenizer.create_tokens())
        tree = parser.parse()
        symbol_table_builder = SymbolTableBuilder()
        symbol_table_builder.visit(tree)
        print(symbol_table_builder.symbol_table)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        raise Exception("Missing source file")
    if len(sys.argv) > 2:
        raise Exception("Too many arguments")
    filename = sys.argv[1]
    process(filename)
