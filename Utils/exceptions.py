# Parse opcode
class OpCode_Does_Not_Exist(Exception):
    def __init__(self, message):
        super().__init__(message)
     
# Run opcodes
class Not_Enough_Arguments(Exception):
    def __init__(self, message):
        super().__init__(message)     
   
class Incorrect_Args_Passed(Exception):
    def __init__(self, message):
        super().__init__(message)