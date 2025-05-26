""" Defines custom exceptions for handling errors related to interactions with
Large Language Models (LLMs), particularly those used in Retrieval-Augmented Generation (RAG) systems.
"""

from CustomExceptions.base_exceptions import BaseException

class RAGLLMInitializationError(BaseException):
    ...