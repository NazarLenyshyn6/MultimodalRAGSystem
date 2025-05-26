""" Defines custom exceptions for handling errors related to embedding operations within the system. """

from CustomExceptions.base_exceptions import BaseException

class ImageEmbeddingError(BaseException):
    ...

class TextEmbeddingError(BaseException):
    ...

class VectorProjectionError(BaseException):
    ...