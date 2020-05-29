from src.token_type import INTEGER, FLOAT, PLUS, MINUS, MULTIPLY, DIVIDE, LPAREN, RPAREN, EOF
from src.tokenizer import Tokenizer
from src.parser import Parser


"""
A node visitor class used to visit node in the AST
"""
class NodeVisitor:
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit_exception)
        return visitor(node)

    def generic_visit_exception(self, node):
        raise Exception(f"No visit_{type(node).__name__} exists.")


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
        elif node.op.type == DIVIDE:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def error(self):
        raise Exception("Interpreter error.")

    def interpret(self):
        ast = self.parser.parse()
        if not ast:
            return ""
        return self.visit(ast)