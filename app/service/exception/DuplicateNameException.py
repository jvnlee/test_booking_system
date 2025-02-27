class DuplicateNameException(BaseException):
    def __init__(self, message="Name already exists."):
        super().__init__(message)