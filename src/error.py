"""
Handle some types of errors here
"""

class Error:
    def __init__(self, error_name, detail):
        self.error_name = error_name
        self.detail = detail

    def __str__(self):
        return f"{self.error_name}: {self.detail}"

    def __repr__(self):
        return self.__str__()

class IllegalCharError(Error):
    def __init__(self, detail):
        super().__init__("Illegal Character", detail)
    