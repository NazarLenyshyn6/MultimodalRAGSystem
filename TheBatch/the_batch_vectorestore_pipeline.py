"""Module to create and manage TheBatch Chroma vectorstore with preprocessed text and image documents."""

import numpy as np
from pathlib import Path

from TheBatch.Preprocessing.the_batch_data_loader import TheBatchDataLoader
from TheBatch.Preprocessing.the_batch_preprocessor import TheBatchPreprocessor
from Embedding.text_embedding import SentenceTransformerTextEmbedding
from VectorStore.chroma_vector_store import ChromaVectorStore
from Internals.adapters import ChromaTextEmbeddingAdapter
from Internals.logger import logger
from Schema.schema import ImageDocument
from Internals.utils import save_image_documents_to_json
from TheBatch.the_batch_configs import (THE_BATCH_IMAGE_DOCUMENTS_STORE, 
                                        THE_BATCH_URLS_PATH, 
                                        THE_BATCH_VECTORESTORE_PERSIST_DIR, 
                                        CREATE_VECTORESTORE, 
                                        COLLECTION_NAME)

def create_the_batch_vectorestore():
    # Load The Batch urls
    with open(THE_BATCH_URLS_PATH) as f:
        the_batch_urls = f.readlines()
    the_batch_urls = [url.strip() for url in the_batch_urls]

    # Load data
    loader = TheBatchDataLoader()
    loaded_data = [loader.load(url=url) for url in the_batch_urls]

    # Preprocess data
    preprocessor = TheBatchPreprocessor()
    documents = []
    for data in loaded_data:
        images_urls = [img['src'] for img in data.images]
        processed_docs = preprocessor.preprocess(
            source_url=data.url,
            elements=data.get_all(),
            images_urls=images_urls
        )
        documents.extend(processed_docs)

    # Save ImageDocuments
    image_documents = {doc.id: doc for doc in documents if isinstance(doc, ImageDocument)}
    save_image_documents_to_json(image_documents, THE_BATCH_IMAGE_DOCUMENTS_STORE)

    # Embedding
    embedding_function = SentenceTransformerTextEmbedding()
    embeddings = np.vstack([embedding_function.encode([doc.content]) for doc in documents])

    # Create vectorstore with persistence
    adapted_embedding = ChromaTextEmbeddingAdapter(embedding_function=embedding_function)
    vectorstore = ChromaVectorStore(
        embedding_function=adapted_embedding,
        collection_name=COLLECTION_NAME,
        persist_directory=THE_BATCH_VECTORESTORE_PERSIST_DIR
    )

    # Add documents and embeddings
    vectorstore.add_documents(documents=documents, embeddings=embeddings)
    vectorstore.save()
    return vectorstore


def load_the_batch_vectorestore():
    # Recreate embedding function for adapter
    embedding_function = SentenceTransformerTextEmbedding()
    adapted_embedding = ChromaTextEmbeddingAdapter(embedding_function=embedding_function)

    # Load from persisted directory
    vectorstore = ChromaVectorStore(
        embedding_function=adapted_embedding,
        collection_name=COLLECTION_NAME,
        persist_directory=THE_BATCH_VECTORESTORE_PERSIST_DIR
    )
    return vectorstore


# Main logic
if CREATE_VECTORESTORE is True:
    logger.info("Creating TheBatch vectore store.")
    the_batch_vectorestore = create_the_batch_vectorestore()
    logger.info("TheBatch vectorestore successfully created and saved.")
else:
    logger.info("Loading TheBatch vectorestore.")
    the_batch_vectorestore = load_the_batch_vectorestore()
    logger.info("TheBatch vectorestore loaded successfully.")
