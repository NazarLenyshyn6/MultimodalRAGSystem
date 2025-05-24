"""."""

from typing import ClassVar, Optional, List,  Callable, Union, Literal
from typing_extensions import override

import pydantic
import numpy as np
from langchain.vectorstores import Chroma
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain.schema import Document
from langchain.embeddings.base import Embeddings

import schema
from VectorStore import base_vector_store
from Internals import adapters
from Internals import utils
from CustomExceptions import vectore_store_exceptions

ToBaseDocument =  Callable[[Document], schema.BaseDocument]

class ChromaVectorStore(base_vector_store.VectorStoreI, pydantic.BaseModel):
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
    retriver: Optional[VectorStoreRetriever] =  pydantic.Field(default=None)
    search_type: Literal['similarity', 'mmr'] = pydantic.Field(default='similarity')

    def model_post_init(self, context):
        self.vectorstore = Chroma(embedding_function=self.embedding_function,
                                  collection_name=self.collection_name)
        self.retriver = self.vectorstore.as_retriever(search_type=self.search_type)
    
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
            cls._supported_documents.add(document)
            cls._to_base_document[document.type] = to_base_document
        except Exception as e:
            raise vectore_store_exceptions.DocumentAdditionError(f"ChoromaVectorStore failed to add new supported document type: {e}")

    @override
    def clean(self) -> None:
        """Clears the vector store, removing all stored documents and embeddings.

        Raises:
            VectoreStoreCleaningError: .
        """
        try:
            self.vectorstore._collection.delete()
        except Exception as e:
            raise vectore_store_exceptions.VectoreStoreCleaningError(message=f"Failed to clear ChormaVectoreStore: {e}")

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
        for document  in  documents:
            if not type(document) in self._supported_documents:
                raise  TypeError(f'Only {self._supported_documents} are currently supported  with  ChoromaVectorStore. Got instead: {type(document)}')
        
        try:
            self.vectorstore._collection.add(
                    ids=[document.id  for document  in documents],
                    embeddings=embeddings,
                    documents=[f'{document.content}' for document in documents],
                    metadatas=[document.metadata for document in documents]
                )
        except Exception as e:
            raise vectore_store_exceptions.DocumentAdditionError(message=f"ChoromaVectorStore failed document addition: {e}")
    
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
            self.retriver.search_kwargs['k'] = k
            docs = self.retriver.invoke(query)
            return [self._to_base_document[doc.metadata['type']](doc) for doc in docs]
        except Exception as e:
            raise vectore_store_exceptions.FailedSimilaritySerachError(message=f"ChoromaVectorStore failed similarity search: {e}")
    