class CustomException(ERSException):
    pass


class ERSException(Exception):
    """
    Custom exception which can also be treated as an ERS issue.
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message
