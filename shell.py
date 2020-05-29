import sys
from src.interpreter import Interpreter
from src.tokenizer import Tokenizer

def shell():
    """
        Interactive shell
        """
    while True:
        try:
            text = input('Pylang> ')
        except EOFError:  # Ctrl + D
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.interpret()
        print(result)

def read_file(filename):
    with open(filename) as file:
        text = file.read()
        interpreter = Interpreter(text)
        result = interpreter.interpret()
        print(interpreter.GLOBAL_VARS)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        read_file(filename)
    else:
        shell()