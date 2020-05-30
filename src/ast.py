"""
Abstract syntax tree
"""

class AST:
    pass



class UnaryOp(AST):
    """
    Represents unary operators
    """
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class BinOp(AST):
    """
    Represent binary operators
    """
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    """
    Represents numbers
    """
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Compound(AST):
    """
    Represents BEGIN...END. block
    Contains a list of statements
    """
    def __init__(self):
        self.children = []

class Assign(AST):
    """
    Assignment statement
    """
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    """
    Represents variables
    """
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    """
    Represents empty statement. BEGIN..END.
    """
    pass

class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block


class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class VariableDeclaration(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

