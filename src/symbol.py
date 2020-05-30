from collections import OrderedDict
from src.token_type import INTEGER, REAL
from src.node_visitor import NodeVisitor
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
        return self.name

    def __repr__(self):
        return self.__str__()

"""
Represents variable symbol
"""
class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return f"({self.name}: {self.type})"

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
        symbol_list = [value for value in self.symbols.values()]
        out = f"Symbols: {symbol_list}"
        return out

    def __repr__(self):
        return self.__str__()

    #store a symbol
    def store(self, symbol):
        print(f"Define: {symbol}")
        self.symbols[symbol.name] = symbol

    #look up a symbol
    def lookup(self, name):
        print(f"Lookup: {name}")
        return self.symbols.get(name) #either a Symbol or None

"""
Building symbol table
"""
class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Num(self, node):
        pass

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_VariableDeclaration(self, node):
        type_name = node.type_node.value
        type_symbol = self.symbol_table.lookup(type_name)
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)
        self.symbol_table.store(var_symbol)

    def visit_Assign(self, node):
        var_name = node.left.value
        var_symbol = self.symbol_table.lookup(var_name)
        if var_symbol is None: #variable is not yet defined
            raise NameError(f"{repr(var_name)} is not defined")
        self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.symbol_table.lookup(var_name)

        if var_symbol is None:
            raise NameError(f"{repr(var_name)} is not defined")

    def visit_ProcedureDeclaration(self, node):
        pass

