"""."""

import pydantic
import numpy as np

from Embedding import text_embedding
from Internals import utils

class ChromaTextEmbeddingAdapter(pydantic.BaseModel):
    """Adapt TextEmbeddingI object to follow langchain_core.embeddings.Embeddings interface.

    Attributes:
        embedding_function: TextEmbeddingI object for text embedding.
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    embedding_function: text_embedding.TextEmbeddingI

    def embed_query(self, text: str) -> np.ndarray:
        """Embed input text.

        Args:
            text: Text to embed.

        Raises:
            TypeError: If text is not a string.

        Returns:
            np.ndarray: Embedding vector.
        """
        utils.validate_dtypes(
            inputs=[text], 
            input_names=['text'], 
            required_dtypes=[str]
            )
        return self.embedding_function.encode([text])[0]