# LLM

# llm_reponse.py
This module provides a simple dataclasess to encapsulate the response from a Retrieval-Augmented Generation (RAG) language models, bundling the user query, the model’s generated text, and the documents used as context.

# rag_llm.py
This module specifies a protocol for Retrieval-Augmented Generation (RAG) language models and provides a concrete implementation using the Ollama LLM. It manages document retrieval from a vector store, constructs prompts with context, and generates responses accordingly, while handling validation and logging.