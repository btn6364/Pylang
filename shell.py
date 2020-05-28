from src.interpreter import Interpreter

def main():
    """
    Interactive shell
    """
    while True:
        try:
            text = input('Pylang> ')
        except EOFError: #Ctrl + D
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.interpret()
        print(result)

if __name__ == '__main__':
    main()