from CustomExceptions.base_exceptions import BaseException


class ImageDescriptionError(BaseException):
    ...

class ImageLoadingError(BaseException):
    ...

class TextExtractionError(BaseException):
    ...

class TextSplittingError(BaseException):
    ...

class TextSplitterInitializationError(BaseException):
    ...