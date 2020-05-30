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
