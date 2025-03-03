class LoginException(Exception):
    def __init__(self, message="Incorrect username or password."):
        super().__init__(message)