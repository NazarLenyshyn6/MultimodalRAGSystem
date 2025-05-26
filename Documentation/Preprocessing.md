# Preprocessing

# image_describer.py
This module defines an abstract interface for image describers and provides a concrete implementation leveraging the BLIP model to generate textual descriptions of images. It handles model loading, input validation, and error management with detailed logging.

# image_loaders.py
This module provides an abstraction for image loading and a concrete implementation using HTTP requests to fetch images, handling errors gracefully and validating inputs while integrating with custom logging and exception frameworks.

# text_extraction.py
This module defines a text extraction interface and a simple extractor that processes lists of HTML elements, validates input types, concatenates their text content with customizable separators, and integrates logging and custom exception handling for robust usage.

# text_splitting.py
This module defines an interface and an implementation for splitting large texts into smaller, manageable chunks. It uses LangChain's RecursiveCharacterTextSplitter to break text based on chunk size and overlap, then wraps each chunk in a TextDocument with unique IDs and metadata. The module handles input validation, logging, and errors to ensure reliable text processing.
