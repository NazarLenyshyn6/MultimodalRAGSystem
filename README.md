# Multimodal RAG System for TheBatch

A Multimodal Retrieval-Augmented Generation (RAG) system that retrieves and summarizes relevant news articles from TheBatch, leveraging both textual and visual data. Supports query-based search, question answering, and media display.

# Description
This project implements a Multimodal RAG system designed to:

- Retrieve relevant articles from TheBatch using advanced retrieval techniques.

- Incorporate textual and visual data (e.g., images from articles).

- Answer user queries using a generative model enhanced by retrieved content.

- Display associated media alongside article summaries.

The system integrates:

- Dense retrievers (textual) and visual retrievers (image embeddings).

- Generative models for summarization and question-answering.

- User interface for interactive querying and media display.

# Installation
```
git clone https://github.com/NazarLenyshyn6/MultimodalRAGSystem.git
pip install -r requirements.txt
pip install -e .
```

# Usage
To start the interactive user interface for the Multimodal RAG System, run the Streamlit app with the following command:

```bash
streamlit run TheBatch/the_batch_app.py
```

This will lanch the web-based interface where you can enter you queries and view article
summaries along with images.

# TODO
- Implement automated tests for both backend and UI components.
- Add support for PNG, JPEG, SVG image formats in multimodal retrieval.
- Implement a modular framework for creating and managing UI components.


