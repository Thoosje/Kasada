class OpCode_Does_Not_Exist(Exception):
    def __init__(self, message):
        super().__init__(message)