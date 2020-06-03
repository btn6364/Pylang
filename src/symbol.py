from collections import OrderedDict
from src.token_type import INTEGER, REAL

"""
Represents a symbol
"""

class Symbol:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

"""
Represents built in type symbol
"""
class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        class_name = self.__class__.__name__
        return f"<{class_name}(name='{self.name}')>"

    def __repr__(self):
        return self.__str__()

"""
Represents variable symbol
"""
class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        class_name = self.__class__.__name__
        return f"<{class_name}(name='{self.name}', type='{self.type}')>"

    def __repr__(self):
        return self.__str__()

"""
Represents a symbol table
"""
class SymbolTable:
    def __init__(self):
        self.symbols = OrderedDict()
        self.init_builtins()

    def init_builtins(self):
        self.store(BuiltinTypeSymbol(INTEGER))
        self.store(BuiltinTypeSymbol(REAL))

    def __str__(self):
        header = "Symbol table contents:"
        out = ["\n", header, "_" * len(header)]
        extension = []
        for key, value in self.symbols.items():
            extension.append(("%7s: %r") % (key, value))
        out.extend(extension)
        out.append("\n")
        return "\n".join(out)

    def __repr__(self):
        return self.__str__()

    #store a symbol
    def store(self, symbol):
        print(f"Defining: {symbol}")
        self.symbols[symbol.name] = symbol

    #look up a symbol
    def lookup(self, name):
        print(f"Looking up: {name}")
        return self.symbols.get(name) #either a Symbol or None


