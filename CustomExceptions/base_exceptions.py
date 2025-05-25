class BaseException(Exception):
    """Base class for custom exceptions."""
    
    def __init__(self, message: str):
        super().__init__(message)
