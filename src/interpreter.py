from src.token_type import *
from src.tokenizer import Tokenizer
from src.parser import Parser
from src.node_visitor import NodeVisitor

"""
The interpreter that will interpret the code
"""

class Interpreter(NodeVisitor):
    def __init__(self, text):
        """
        :param text: client input
        """
        self.text = text
        self.tokenizer = Tokenizer(self.text)
        self.parser = Parser(self.tokenizer.create_tokens())
        self.GLOBAL_VARS = dict()

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VariableDeclaration(self, node):
        pass

    def visit_Type(self, node):
        pass

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_VARS[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_VARS[var_name]
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val


    def visit_NoOp(self, node):
        pass

    def visit_UnaryOp(self, node):
        if node.op.type == PLUS:
            return + self.visit(node.expr)
        elif node.op.type == MINUS:
            return - self.visit(node.expr)

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MULTIPLY:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == FLOAT_DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_ProcedureDeclaration(self, node):
        pass

    def error(self):
        raise Exception("Interpreter error.")

    def interpret(self):
        ast = self.parser.parse()
        if not ast:
            return ""
        return self.visit(ast)