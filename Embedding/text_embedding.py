
from typing import List
from typing_extensions import override
from abc import ABC, abstractmethod

import numpy as np
import pydantic
from sentence_transformers import SentenceTransformer

from Internals.utils import validate_dtypes
from Internals.logger import logger
from CustomExceptions import embedding_exceptions


class TextEmbeddingI(ABC):
    """Interface class for text embedding."""
    @abstractmethod
    def encode(self, sentences: List[str]) -> np.ndarray:
        ...

class SentenceTransformerTextEmbedding(pydantic.BaseModel, TextEmbeddingI):
    """Text Embedding with SentenceTransformer.

    Attributes:
        model_name_or_path: If it is a filepath on disc, it loads the model from that path. 
                            If it is not a path, it first tries to download a pre-trained SentenceTransformer model. 
                            If that fails, tries to construct a model from the Hugging Face Hub with that name. 
        model: SentenceTransformer model that can be used to map sentences / text to embeddings.
    """
    model_config  =  pydantic.ConfigDict(arbitrary_types_allowed=True)
    model_name_or_path: str = pydantic.Field(default="sentence-transformers/all-MiniLM-L6-v2")
    model: SentenceTransformer =  pydantic.Field(default=None)

    def model_post_init(self, context):
        logger.info("SentenceTransformerTextEmbedding initialization.")
        if self.model is None:
            try:
                self.model = SentenceTransformer(self.model_name_or_path)
            except Exception as e:
                msg = f"SentenceTransformerTextEmbedding initialization failed due to error in SentenceTransformer initialization with {self.model_name_or_path} model_name_or_path."
                logger.exception(msg)
                raise embedding_exceptions.TextEmbeddingError(msg) from e
        logger.info("SentenceTransformerTextEmbedding done successfully.")

    @override
    def encode(self, sentences: List[str])  ->  np.ndarray:
        """ Computes sentence embeddings.
        Args:
            sentences: The sentences to embed.

        Raises:
            TypeError: If sentences is not a list or not all elements in sentences is a string.
            TextEmbeddingError: If sentences embedding fails.

        Returns: 2d numpy array with shape [num_inputs, output_dimension] is returned. 
                 If only one string input is provided, then the output is a 1d array with shape [output_dimension].

        """
        
        validate_dtypes(
            inputs=[sentences], 
            input_names=['sentences'], 
            required_dtypes=[list]
            )
        for sentence in sentences: 
            validate_dtypes(
                inputs=[sentence], 
                input_names=['sentences_element'], 
                required_dtypes=[str]
                )
        try:
            logger.info("SentenceTransformerTextEmbedding encoding sentences.")
            embeddings = np.asarray(self.model.encode(sentences), dtype=np.float32)
            logger.info("SentenceTransformerTextEmbedding successfuly encoded sentences.")
            return embeddings
        except Exception as e:
            msg = "SentenceTransformerTextEmbedding failed sentences embedding."
            logger.exception(msg)
            raise embedding_exceptions.TextEmbeddingError(msg) from e
        