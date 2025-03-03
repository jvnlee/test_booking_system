class NotAuthorizedException(Exception):
    def __init__(self, message="Not authorized to perform this operation."):
        super().__init__(message)