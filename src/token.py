"""
The token component in the lexer.
"""
class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """
        String representation of the token
        :return: Ex: Token(PLUS, "+")
        """
        return f"Token({self.type}:{self.value})"

    def __repr__(self):
        return self.__str__()