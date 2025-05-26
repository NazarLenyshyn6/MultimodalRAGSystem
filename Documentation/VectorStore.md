# VectoreStore

# base_vector_store.py
This module provides the VectorStoreI Protocol defining the expected methods and constructor for any vector store implementation. It ensures implementations support initializing with a directory, adding documents with embeddings, performing similarity searches, and saving/loading the store.

# chroma_vectore_store.py
This module defines a ChromaVectorStore leveraging Chroma for scalable vector storage and retrieval. It supports various document types via a type conversion system and provides robust methods for adding, searching, saving, and loading data, with clear error handling and logging. The design prioritizes modularity, extensibility, and compliance with LangChain interfaces.