"""Contains different utility functions."""  

import hashlib

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
        

def compute_hash_from_text(text: str) -> str:
    validate_dtypes([text], ['text'], [str])
    return hashlib.sha256(text.encode('utf-8')).hexdigest()         