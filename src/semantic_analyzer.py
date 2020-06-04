from src.node_visitor import NodeVisitor
from src.symbol import VarSymbol
from src.symbol import ScopedSymbolTable
"""
Semantic analyzer
"""
class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.symbol_table = ScopedSymbolTable(scope_name="global", scope_level=1)

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

        #check for duplicate declarations
        if self.symbol_table.lookup(var_name) is not None:
            raise Exception(f"[ERROR]: Duplicate identifier {var_name} found.")

        self.symbol_table.store(var_symbol)

    def visit_Assign(self, node):
        var_name = node.left.value
        var_symbol = self.symbol_table.lookup(var_name)
        if var_symbol is None: #variable is not yet defined
            raise NameError(f"{repr(var_name)} is not defined")
        self.visit(node.right)
        self.visit(node.left)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.symbol_table.lookup(var_name)

        if var_symbol is None:
            raise NameError(f"{repr(var_name)} is not defined")

    def visit_ProcedureDeclaration(self, node):
        pass
