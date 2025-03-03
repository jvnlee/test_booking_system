class InvalidTokenException(Exception):
    def __init__(self, message="Invalid JWT token."):
        super().__init__(message)