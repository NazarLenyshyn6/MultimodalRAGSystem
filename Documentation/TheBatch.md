# LLM
# the_batch_llms.py
This module defines TheBatchLLM, a multimodal RAG (retrieval-augmented generation) system that integrates an Ollama LLM, 
a prompt template, and a vector store to answer user queries with both text and relevant image documents. 
It manages initialization, querying, and error handling.


# the_batch_trained_llms.py
This module sets up and stores a ready-to-use TheBatchLLM instance, 
configured with the prompt template and vector store for efficient querying and retrieval in TheBatch system.


# Preprocessing
# the_batch_data_loader.py
This module integrates a customizable data ingestion system for The Batch website, 
combining fetchers and parsers (e.g., RequestsFetcher, BS4Parser) with configurable parsing rules 
to load and structure multimodal data (text, images) for downstream processing.

# the_batch_data_preprocessor.py
This module combines multimodal data preprocessing steps, including text extraction and splitting from HTML elements and image loading and description, into a unified framework for preparing data from The Batch website. It leverages custom components for each step (e.g., BS4 text extractor, BLIP image describer) to produce structured TextDocument and ImageDocument outputs for downstream applications like RAG or embedding models.


# Store
# the_batch_image_documents_store.py
Directory that serves as the persistence location for the Choroma vector store used by TheBatch system. This vector store contains both text and image documents extracted 
and preprocessed from TheBatch site.

# the_batch_vectorestore_persist_dir
Stores as mapping from unique image document IDs to thein configurations(metadata, extracted text, loaded image, image url). 
Used for loading and referencing image data.

# the_batch_configs.py
This module defines the configuration setup for TheBatch system, including:

- Paths for storage of URLs, vectorstores, and image documents.

- Fetcher and parser instances for web data retrieval and HTML parsing.

- A detailed ParserConfig specifying tag mappings for text and image extraction from The Batch website.

- A specialized PromptTemplate for LLMs to generate explicit, comprehensive answers based strictly on provided context, without external knowledge or references.

# the_batch_exceptions.py
This module defines custom exception specific to TheBatch LLM system

# the_batch_vectorestore_pipeline.py
This module handles the creation and loading of a Chroma vectorstore for TheBatch dataset, integrating:

- Data ingestion: Loads TheBatch URLs and fetches their content.

- Preprocessing: Processes HTML content and extracts structured data (both text and image).

- Image document management: Saves mappings of image documents to a JSON store.

- Embedding: Generates documents embeddings using a SentenceTransformerTextEmbedding model.

- Chroma vectorstore: Stores preprocessed documents and embeddings in a persistent vectorstore for semantic search and RAG use cases.