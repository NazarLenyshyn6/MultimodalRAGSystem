"""Contains different utility functions."""  

import hashlib
import uuid
import logging
import traceback

def validate_dtypes(inputs, input_names, required_dtypes):
    """Validate if inputs corresponds to required data types.

    Args:
        inputs: List of object for type validations.
        input_names: List of object names to use in the error message.
        required_dtypes: List of expected data types.

    Raises:
        TypeError: If input does not match extcted type
    """
    for input, input_name, required_dtype in zip(inputs, input_names, required_dtypes):
        if not isinstance(input, required_dtype):
            raise TypeError(f"{input_name} must be of type {required_dtype}. Got instead: {type(input)}")
        

def generate_unique_doc_id(content: str, metadata: dict = None) -> str:
    """Generate a unique document identifier based on content, metadata, and a random salt.

    Args:
        content: The main textual content of the document.. 
        metadata: Additional metadata to incorporate into the hash.. 

    Returns:
        str:  A unique document identifier in the format: "<hash>-<uuid>".
    """
    combined = content + str(sorted(metadata.items()) if metadata else '')
    base_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
    salt = str(uuid.uuid4())
    return f"{base_hash}-{salt}"
