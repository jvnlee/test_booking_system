class DuplicateUsernameException(Exception):
    def __init__(self, message="Username already exists."):
        super().__init__(message)