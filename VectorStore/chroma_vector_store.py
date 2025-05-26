"""Chroma-based VectorStore supporting multiple document types with embeddings, retrieval, and persistence."""

from typing import ClassVar, Optional, List,  Callable, Union, Literal
from typing_extensions import override

import pydantic
import numpy as np
from langchain.vectorstores import Chroma
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain.schema import Document
from langchain.embeddings.base import Embeddings

import Schema.schema as schema
from VectorStore import base_vector_store
from Internals import adapters
from Internals import utils
from Internals.logger import logger
from CustomExceptions import vectore_store_exceptions

ToBaseDocument =  Callable[[Document], schema.BaseDocument]

class ChromaVectorStore(pydantic.BaseModel):
    """Vector Store implementation using Chroma, supporting multiple document types with embeddings.

    Attributes:
        collection_name: The name of the collection used in the Chroma vector store. 
        embedding_function: A text embedding function or LangChain-compatible embedding object used to
                            convert text into vector representations. 
        vectorstore: Internal Chroma vector store instance, initialized post model init.
        retriver: Retriever for similarity search and MMR search.
        search_type: Type of retrieval search to use.

    Raises:
        ValidationError: If attribute does not match expected data type.
        VectoreStoreInitializationError: If vectorestore initialization fails.
    """
    _supported_documents: ClassVar = {schema.ImageDocument, schema.TextDocument}
    _to_base_document: ClassVar = {
        schema.ImageDocument.type: lambda langchain_document: schema.ImageDocument(
            id=langchain_document.metadata['id'],
            type=langchain_document.metadata['type'],
            content=langchain_document.page_content,
            source_url=langchain_document.metadata['source_url'],
            image_url=langchain_document.metadata['image_url']
            ),
        schema.TextDocument.type: lambda langchain_document: schema.TextDocument(
            id=langchain_document.metadata['id'],
            type=langchain_document.metadata['type'],
            content=langchain_document.page_content,
            source_url=langchain_document.metadata['source_url']
            )
            }
    
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    collection_name: str
    embedding_function: Union[adapters.ChromaTextEmbeddingAdapter, Embeddings]
    vectorstore: Optional[Chroma] = pydantic.Field(default=None, repr=False)
    persist_directory: str
    retriver: Optional[VectorStoreRetriever] =  pydantic.Field(default=None)
    search_type: Literal['similarity', 'mmr'] = pydantic.Field(default='similarity')

    def model_post_init(self, context):
        try:
            self.vectorstore = Chroma(embedding_function=self.embedding_function,
                                      collection_name=self.collection_name,
                                      persist_directory=self.persist_directory)
        except Exception as e:
            msg = (f"ChromaVectorStore initialization failed due to error in Chroma initialization."
                   f"Embedding function: {self.embedding_function}"
                   f"Collection naem: {self.collection_name}"
                   )
            logger.exception(msg)
            raise vectore_store_exceptions.VectoreStoreInitializationError(msg) from e
        try:
            self.retriver = self.vectorstore.as_retriever(search_type=self.search_type)
        except Exception as e:
            msg = f"ChromaVectoreStore initialization failed due to error in Chroma.as_retriver with {self.search_type} search type."
            logger.exception(msg)
            raise vectore_store_exceptions.VectoreStoreInitializationError(msg) from e
    
    @classmethod
    def add_supported_document(
        cls, 
        document: schema.BaseDocument, 
        to_base_document: ToBaseDocument,
        ) -> None:
        """ Registers a new supported document type for the vector store.

        Args:
            document (schema.BaseDocument): Example instance of a supported document type.
            to_base_document (Callable[[Document], schema.BaseDocument]): A conversion function to convert
                LangChain Document into the BaseDocument type.

        Raises:
            TypeError: If `document` or `to_base_document` is not of the expected type.
            DocumentAdditionError: .
        """
        utils.validate_dtypes(
            inputs=[
                document, 
                to_base_document
                ], 
                input_names=[
                    'document', 
                    'to_base_document'
                    ], 
                required_dtypes=[
                    schema.BaseDocument, 
                    ToBaseDocument]
                    )
        try:
            logger.info(f"Adding new supported document type {document} to ChrommaVectoreStore")
            cls._supported_documents.add(document)
            cls._to_base_document[document.type] = to_base_document
            logger.info(f"{document} successfully added to ChoromaVectoreStore.")
        except Exception as e:
            msg = (f"CHomaVectoreStore failed to add new supported document type"
                   f"Document: {document}"
                   f"Convertion function: {to_base_document}"
                   )
            logger.exception(msg)
            raise vectore_store_exceptions.DocumentAdditionError(msg) from e

    @override
    def clean(self) -> None:
        """Clears the vector store, removing all stored documents and embeddings.

        Raises:
            VectoreStoreCleaningError: If vectorestore cleaning fails.
        """
        try:
            logger.info("ChromaVectoreStore cleaning.")
            self.vectorstore._collection.delete()
            logger.info("ChromaVectoreStore successfully clean.")
        except Exception as e:
            msg = f"ChoraVectoreStore cleaning failed."
            logger.exception(msg)
            raise vectore_store_exceptions.VectoreStoreCleaningError(msg) from e

    @override
    def add_documents(self, 
                      documents: list[schema.BaseDocument], 
                      embeddings: np.ndarray
                      ) -> None:
        """ Adds documents and their embeddings to the Chroma vector store.

        Args:
            documents (List[schema.BaseDocument]): List of BaseDocument instances to store.
            embeddings (np.ndarray): 2D numpy array of embedding vectors corresponding to the documents.

        Raises:
            TypeError: If embeddings are not a numpy ndarray, or if a document type is not supported.
            DocumentAdditionError: .
        """
        utils.validate_dtypes(
            inputs=[embeddings], 
            input_names=['embeddings'], 
            required_dtypes=[np.ndarray]
            )
        for document in documents:
            if not type(document) in self._supported_documents:
                raise TypeError(
                    f'Only {self._supported_documents} are currently supported  with  ChoromaVectorStore. Got instead: {type(document)}'
                    )
        
        try:
            logger.info("Adding new (documents, embeddings) to ChromaVectoreStore.")
            self.vectorstore._collection.add(
                    ids=[document.id  for document  in documents],
                    embeddings=embeddings,
                    documents=[f'{document.content}' for document in documents],
                    metadatas=[document.metadata for document in documents]
                )
            logger.info("New (documents, embeddings) successfully added to ChromaVectoreStore.")
        except Exception as e:
            msg = "ChromaVectoreStore failed document addition."
            logger.exception(msg)
            raise vectore_store_exceptions.DocumentAdditionError(msg) from e
    
    @override
    def similarity_search(self,
                           query: str,  
                           k: int = 5
                           ) -> List[schema.BaseDocument]:
        """ Performs a similarity search for a given query.

        Args:
            query (str): The query string to search for.
            k (int, optional): The number of top results to return. Defaults to 5.

        Raises:
            TypeError: If `query` is not a string or `k` is not an integer.
            FailedSimilaritySearch: .

        Returns:
            List[schema.BaseDocument]: List of top-K similar documents, converted into supported BaseDocument types.
        """

        utils.validate_dtypes(
            inputs=[query, k], 
            input_names=['query', 'k'], 
            required_dtypes=[str, int]
            )
        try:
            logger.info(f"Searching {k} similar documents for query: {query} in ChromaVectoreStore")
            self.retriver.search_kwargs['k'] = k
            docs = self.retriver.invoke(query)
            retrieved_docs = [self._to_base_document[doc.metadata['type']](doc) for doc in docs]
            logger.info(f"{k} similar documents for query: {query} successfully retieved from ChromaVectoreStore")
            return retrieved_docs
        except Exception as e:
            msg = f"ChoromaVectorStore failed similarity search for query: {query}"
            logger.exception(msg)
            raise vectore_store_exceptions.SimilaritySerachError(msg) from e
        
    @override
    def save(self) -> None:
        """ Saves the current state of the Chroma vector store to disk at the specified path.

        Args:
            vectorestore_path: The file system path where the vector store state should be saved.

        Raises:
            TypeError: If `vectorestore_path` is not a string.
            VectoreStoreSavingError: If saving the vector store fails due to an internal error.
        """
        try:
            logger.info(f"Saving ChromaVectoreStore to path: {self.persist_directory}")
            self.vectorstore.persist()
            logger.info(f"ChromaVectoreStore successfully saved to {self.persist_directory}")
        except Exception as e:
            msg = f"ChromaVectoreStore failed to save to {self.persist_directory}."
            logger.exception(msg)
            raise vectore_store_exceptions.VectoreStoreSavingError(msg) from e

    @override
    def load(self, vectorestore_path: str) -> None:
        """ Loads a Chroma vector store from disk at the specified path and initializes internal structures.

        Args:
            vectorestore_path (str): The file system path from which to load the vector store state.

        Raises:
            TypeError: If `vectorestore_path` is not a string.
            VectoreStoreLoadingError: If loading the vector store fails due to an internal error.
        """
        utils.validate_dtypes(
            inputs=[vectorestore_path],
            input_names=['vectorestore_path'],
            required_dtypes=[str]
        )
        try:
            logger.info(f"Loading ChromaVectoreStore from path: {vectorestore_path}")
            self.vectorstore = Chroma(
                embedding_function=self.embedding_function,
                collection_name=self.collection_name,
                persist_directory=vectorestore_path
            )
            self.retriver = self.vectorstore.as_retriever(search_type=self.search_type)
            self.persist_directory = vectorestore_path
            logger.info("ChromaVectore persist  directory changed to %s", vectorestore_path)
            logger.info(f"ChromaVectoreStore successfully loaded from {vectorestore_path}")
        except Exception as e:
            msg = f"ChromaVectoreStore failed to load from {vectorestore_path}."
            logger.exception(msg)
            raise vectore_store_exceptions.VectoreStoreLoadingError(msg) from e