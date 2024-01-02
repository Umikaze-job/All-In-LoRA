
class MyException(Exception):
    def __init__(self, arg=""):
        self.arg = arg

class DuplicateException(MyException):
    def __str__(self):
        return "Duplicate names"