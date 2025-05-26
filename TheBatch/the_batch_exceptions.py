"Defines custom exception specific to TheBatch LLM system."

from CustomExceptions.base_exceptions import BaseException

class THEBatchLLMAnswerGenerationError(BaseException):
    ...

class THEBatchLLMInitializationError(BaseException):
    ...