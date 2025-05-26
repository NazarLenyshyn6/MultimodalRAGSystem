""""Defines the RAG LLM interface and concrete implementatinos."""

from typing import Protocol, runtime_checkable, List

import numpy as np
import pydantic
from langchain.llms import Ollama
from langchain_core.prompts.prompt import PromptTemplate

from VectorStore import base_vector_store
from LLM.llm_response import RAGLLMResponse
from Schema.schema import BaseDocument
from Internals.logger import logger
from CustomExceptions import llm_exceptions


@runtime_checkable
class RAGLLMI(Protocol):
    def __init__(self, 
                 vectorstore: base_vector_store.VectorStoreI, 
                 *args, 
                 **kwargs
                 ):
        ...

    def update_vectorstore(self, 
                           documents: List[BaseDocument], 
                           embeddings: np.ndarray
                           ) -> None:
        ...

    def clean_vectorestore(self) -> None:
        ...

    def get_relevant_docs(self, k: int) -> List[BaseDocument]:
        ...

    def query(self, 
              user_query: str, 
              k: int, 
              *args, 
              **kwargs
              ) -> RAGLLMResponse:
        ...

class OllamaRAGLLM(pydantic.BaseModel):
    """OllamaRAGLLM is a Retrieval-Augmented Generation (RAG) model wrapper that integrates:
        - A vector store for document retrieval.
        - A prompt template to inject context into queries.
        - An Ollama LLM to generate responses.

    The model retrieves relevant documents from a vector store based on user queries, 
    constructs a context, and invokes the LLM with a dynamically formatted prompt.

    Attributes:
        model: language model (default is 'llama3.2').
        prompt_template: Template with input variables ('context', 'user_query').
        vectorstore: Vectorstore that follows VectorStoreI inteface.

    Raises:
        RAGLLMInitalizationError: If OllamaRagLLM initialization fails.
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    model: Ollama = pydantic.Field(default=Ollama(model='llama3.2'))
    prompt_template: PromptTemplate
    vectorstore: base_vector_store.VectorStoreI

    @pydantic.model_validator(mode='after')
    def validate_prompt_template(cls, values):
        """ Validates that the prompt template contains the required input variables.

        Raises:
            ValueError: If the prompt template's input variables are not {'context', 'user_query'}.
        """
        logger.info("OllamaRAGLLM initialization")
        prompt_template = values.prompt_template
        if set(prompt_template.input_variables) != {'context', 'user_query'}:
            msg = 'Prompt template input variables must be (context, user_qeury). Got instead: {prompt_template.input_variables}'
            logger.error(msg)
            raise llm_exceptions.RAGLLMInitializationError(msg)
        logger.info("OllamaRAGLLM initialization done successfully.")
        return values

    def _get_context(self, relevant_docs: List[BaseDocument]) -> str:
        """
        Constructs the context string by concatenating content from the retrieved documents.

        Args:
            relevant_docs: Retrieved documents.

        Returns:
            str: Concatenated text content of relevant documents.
        """
        return ''.join(doc.content for doc in relevant_docs)
    
    def update_vectorestore(self, 
                            documents: List[BaseDocument], 
                            embeddings: np.ndarray
                            ) -> None:
        """ Updates the vector store with new documents and their embeddings.

        Args:
            documents: Documents to add.
            embeddings: Corresponding vector embeddings.
        """
        self.vectorstore.add_documents(documents, embeddings)

    def clean_vectorestore(self) -> None:
        """Clears the vector store, removing all stored documents and embeddings."""
        self.vectorstore.clean()

    def get_relevant_docs(self, 
                          user_query: str, 
                          k: int = 5
                          ) -> List[BaseDocument]:
        """ Retrieves the top-k relevant documents from the vector store for a given user query.

        Args:
            user_query: The user's query.
            k: Number of top documents to retrieve. Defaults to 5.

        Returns:
            List[BaseDocument]: The top-k relevant documents.
        """
        return self.vectorstore.similarity_search(user_query, k)

    def query(self, 
              user_query: str, 
              k: int = 5
              ) -> RAGLLMResponse:
        """
        Executes a retrieval-augmented query:
        1. Retrieves top-k relevant documents.
        2. Constructs the context from the documents.
        3. Formats the prompt with context and user query.
        4. Invokes the Ollama LLM to generate a response.

        Args:
            user_query : The user's query.
            k: Number of relevant documents to retrieve. Defaults to 5.

        Returns:
            RAGLLMResponse: Response object containing the user query, LLM output, and relevant documents.
        """
        logger.info(f"OllamaRAGLLM processing user query: {user_query}")
        relevant_docs = self.get_relevant_docs(user_query=user_query, 
                                               k=k)
        context = self._get_context(relevant_docs=relevant_docs)
        prompt = self.prompt_template.invoke({'context': context, 'user_query': user_query})
        llm_response = self.model.invoke(prompt)
        model_response = RAGLLMResponse(user_query=user_query, 
                                         llm_resopnse=llm_response, 
                                         relevant_docs=relevant_docs
                                         )
        logger.info(f"OllamaRAGLLM successfully processed user query: {user_query}")
        return model_response