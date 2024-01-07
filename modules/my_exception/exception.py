
class MyException(Exception):
    def __init__(self, arg:str=""):
        self.arg = arg

class DuplicateException(MyException):
    def __str__(self) -> str:
        return "Duplicate names"