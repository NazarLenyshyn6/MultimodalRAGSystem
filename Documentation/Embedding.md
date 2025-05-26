# Embedding

# image_embedding.py
This module defines an interface and a concrete implementation for image embedding. It provides a class CLIPImageEmbedding that leverages the HuggingFace CLIP model to convert images into numerical embeddings, facilitating tasks like image similarity, retrieval. The module handles model initialization, input validation, and embedding extraction with proper error handling and logging.

# text_embedding.py
This module provides an interface and an implementation for embedding text data. It defines SentenceTransformerTextEmbedding, a class that loads a SentenceTransformer model (either from local path or pretrained models) to convert sentences into vector embeddings. The module includes input validation, error handling, and logging, enabling robust and reusable text embedding functionality.

# vector_projection.py
This module defines an interface and an implementation for projecting high-dimensional vectors into lower-dimensional space. The GaussianRandomVectorProjection class validates inputs, applies sklearn's random projection, and handles exceptions with logging. It provides a robust method for efficient dimensionality reduction in vector processing workflows.