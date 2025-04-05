
class Language:
    def __init__(self, name:str, version:str):
        self.version = version
        self.name=name

class CodeExecutionResult:

    def __init__ (self, user_code, case,  status: int, error, data):
            self.status=status
            self.error=error
            self.data=data
            self.user_code=user_code
            self.case=case
    def __repr__(self):
        return f"{self.status}, {self.error}, {self.data}, {self.user_code}, {self.case}"
