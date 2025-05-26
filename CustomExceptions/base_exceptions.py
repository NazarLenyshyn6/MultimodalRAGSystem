"Defines the base class for custom exceptions used throughout the application."

class BaseException(Exception):
    """Base class for custom exceptions."""
    
    def __init__(self, message: str):
        super().__init__(message)
