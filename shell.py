import sys
from src.interpreter import Interpreter
from src.tokenizer import Tokenizer

def read_file(filename):
    with open(filename, "r") as file:
        text = file.read()
        interpreter = Interpreter(text)
        result = interpreter.interpret()
        print(interpreter.GLOBAL_VARS)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        raise Exception("Missing source code!")
    else:
        filename = sys.argv[1]
        read_file(filename)