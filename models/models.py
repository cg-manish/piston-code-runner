
class Language:
    def __init__(self, name:str, version:str):
        self.version = version
        self.name=name

class CodeExecutionResult:

    def __init__ (self, case,  status: int, error, data):
            self.status=status
            self.error=error
            self.data=data
            self.case=case
    def __repr__(self):
        return f"{self.status}, {self.error}, {self.data},{self.case}"
    def to_dict(self):
         return {
              "status": self. status,
              "error":self.error,
              "data":self.data,
              "case":self.case
         }
         
