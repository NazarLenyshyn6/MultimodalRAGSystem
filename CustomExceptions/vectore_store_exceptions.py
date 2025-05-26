"""Defines custom exceptions for errors encountered during vector store operations."""


from CustomExceptions.base_exceptions import BaseException

class DocumentAdditionError(BaseException):
    ...

class SimilaritySerachError(BaseException):
    ...

class VectoreStoreCleaningError(BaseException):
    ...

class VectoreStoreInitializationError(BaseException):
    ...

class VectoreStoreSavingError(BaseException):
    ...