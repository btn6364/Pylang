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
Procedure Symbol
"""
class ProcedureSymbol(Symbol):
    def __init__(self, name, params=None):
        super(ProcedureSymbol, self).__init__(name)
        self.params = params if params else []

    def __str__(self):
        return f"<{self.__class__.__name__}(name={self.name}, params={self.params})>"

    def __repr__(self):
        return self.__str__()

"""
Represents a symbol table
"""
class ScopedSymbolTable:
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self.symbols = OrderedDict()
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope # for scope chaining

    def init_builtins(self):
        self.store(BuiltinTypeSymbol(INTEGER))
        self.store(BuiltinTypeSymbol(REAL))

    def __str__(self):
        header1 = "SCOPE (SCOPE SYMBOL TABLE):"
        out = ["\n", header1, '=' * len(header1)]
        for header_name, header_value in (
            ("Scope name: ", self.scope_name),
            ("Scope level: ", self.scope_level),
            ("Enclosing scope", self.enclosing_scope.scope_name if self.enclosing_scope else None)
        ):
            out.append("%-15s: %s" % (header_name, header_value))
        header2 = "Scope (Scoped symbol table) contents:"
        out.extend([header2, "-" * len(header2)])
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
        print(f"Looking up: {name}. (Scope name: {self.scope_name})")
        symbol = self.symbols.get(name) #either a Symbol or None

        if symbol:
            return symbol

        #go up the chain and look up the variable
        if self.enclosing_scope:
            return self.enclosing_scope.lookup(name)

