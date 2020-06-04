from src.node_visitor import NodeVisitor
from src.symbol import VarSymbol, ProcedureSymbol
from src.symbol import ScopedSymbolTable
"""
Semantic analyzer
"""
class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.global_scope = ScopedSymbolTable(scope_name="global", scope_level=1)
        self.current_scope = self.global_scope

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Program(self, node):
        print("ENTER scope: global")

        # visit subtree
        self.visit(node.block)

        print(self.global_scope)
        #restore to the previous scope
        self.current_scope = self.current_scope.enclosing_scope
        print("LEAVE scope: global")

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
        type_symbol = self.current_scope.lookup(type_name)

        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)

        #check for duplicate declarations
        if self.current_scope.lookup(var_name) is not None:
            raise Exception(f"[ERROR]: Duplicate identifier {var_name} found.")

        self.current_scope.store(var_symbol)

    def visit_Assign(self, node):
        # var_name = node.left.value
        # var_symbol = self.current_scope.lookup(var_name)
        # if var_symbol is None: #variable is not yet defined
        #     raise NameError(f"{repr(var_name)} is not defined")
        #visit right-hand side
        self.visit(node.right)
        #visit left-hand side
        self.visit(node.left)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)

        if var_symbol is None:
            raise NameError(f"Symbol({repr(var_name)}) is not defined")

    def visit_ProcedureDeclaration(self, node):
        procedure_name = node.procedure_name
        procedure_symbol = ProcedureSymbol(procedure_name)
        self.current_scope.store(procedure_symbol)

        print(f"ENTER scope: {procedure_name}")
        #local scopes
        procedure_scope = ScopedSymbolTable(
            scope_name = procedure_name,
            scope_level = self.current_scope.scope_level + 1,
            enclosing_scope = self.current_scope
        )
        self.current_scope = procedure_scope

        #insert parameters into the procedure scope
        for param_node in node.param_nodes:
            param_type = self.current_scope.lookup(param_node.type_node.value)
            param_name = param_node.var_node.value
            var_symbol = VarSymbol(param_name, param_type)
            #add to the current scope
            self.current_scope.store(var_symbol)

            #add to the current procedure symbol
            procedure_symbol.params.append(var_symbol)

        self.visit(node.block_node)

        print(procedure_scope)

        #restore to the previous scope
        self.current_scope = self.current_scope.enclosing_scope
        print(f"LEAVE scope: {procedure_name}")
