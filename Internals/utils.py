"""Utility functions."""  

from typing import Dict
import hashlib
import uuid
import traceback
import base64
import io
import json
from PIL import Image

from Schema.schema import ImageDocument

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


def ImageDocument_to_serializable_dict(image_document: ImageDocument) -> Dict:
    """ Converts an ImageDocument instance into a serializable dictionary.

    This function transforms the given ImageDocument object into a dictionary 
    that can be easily serialized (e.g., to JSON). Specifically:
    - Metadata fields are preserved as key-value pairs.
    - If the `image` field contains a PIL.Image.Image object, it is encoded into a 
      base64-encoded PNG format string (`image_base64`) to ensure compatibility 
      with text-based serialization formats.

    Args:
        image_document (ImageDocument): The ImageDocument instance to convert.

    Returns:
        Dict: A dictionary containing:
            - All metadata fields from the ImageDocument (id, type, content, 
              source_url, image_url).
            - An additional key 'image_base64' with the base64-encoded image string 
              if the image field is present; otherwise, None.
    """
    image_base64 = None
    if image_document.image:
        buffered = io.BytesIO()
        image_document.image.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return {
        **image_document.metadata,
        'image_base64': image_base64
        }

def from_serializable_dict_to_ImageDocument(data: Dict) -> ImageDocument:
    """
    Reconstructs an ImageDocument instance from a serializable dictionary.

    This function reverses the transformation done by `ImageDocument_to_serializable_dict`.
    It reconstructs an ImageDocument object by:
    - Extracting metadata fields from the provided dictionary.
    - Decoding the optional 'image_base64' field (if present) from a base64-encoded
      PNG string into a PIL.Image.Image object and assigning it to the `image` field.

    Args:
        data (Dict): A dictionary containing serialized ImageDocument data, 
                     including:
                     - Metadata fields ('id', 'type', 'content', 'source_url', 'image_url').
                     - Optionally, 'image_base64' (a base64-encoded PNG image).

    Returns:
        ImageDocument: The reconstructed ImageDocument object with metadata fields 
                       and the decoded image (if present).
    """
    image_data = data.pop('image_base64', None)
    image_obj = None
    if image_data:
        image_bytes = base64.b64decode(image_data)
        image_obj = Image.open(io.BytesIO(image_bytes))  
    return ImageDocument(**data, image=image_obj)

def save_image_documents_to_json(image_documents_mapping: Dict[str, ImageDocument], image_documents_store_path: str, indent: int = 4) -> None:
    """ Serializes and saves a collection of ImageDocument objects to a JSON file.

    This function transforms a dictionary mapping of unique image document IDs to
    ImageDocument instances into a serializable dictionary format. Each ImageDocument
    is converted using the `ImageDocument_to_serializable_dict` function to ensure
    that complex types such as PIL.Image.Image are converted to base64-encoded strings.
    The resulting data is then written to a JSON file at the specified path.

    Args:
        image_documents_mapping (Dict[str, ImageDocument]):
            A dictionary mapping unique string IDs to ImageDocument instances.
        image_documents_store_path (str):
            The file path where the serialized JSON data will be saved.

    Raises:
        IOError: If the file cannot be opened or written to.
    """
    serializable_data = {image_document_id: ImageDocument_to_serializable_dict(image_document) for image_document_id, image_document 
                         in image_documents_mapping.items()
                         }
    with open(image_documents_store_path, 'w') as f:
        json.dump(serializable_data, f, indent=indent)

def load_image_documents_from_json(image_documents_store_path: str) -> Dict[str, ImageDocument]:
    """ Loads and deserializes ImageDocument objects from a JSON file.

    This function reads JSON data from the specified file path, where the data
    represents a dictionary mapping unique image document IDs to their serialized
    dictionary forms. Each serialized dictionary is converted back into an
    ImageDocument instance using the `from_serializable_dict_to_ImageDocument` function,
    which handles decoding of any embedded base64-encoded images.

    Args:
        image_documents_store_path (str):
            The file path from which to load the serialized JSON data.

    Returns:
        Dict[str, ImageDocument]:
            A dictionary mapping image document IDs to their deserialized
            ImageDocument instances.

    Raises:
        IOError: If the file cannot be opened or read.
        json.JSONDecodeError: If the file content is not valid JSON.
    """
    with open(image_documents_store_path, 'r') as f:
        loaded_data = json.load(f)
    return {image_document_id: from_serializable_dict_to_ImageDocument(serialized_image_document_data) 
            for image_document_id, serialized_image_document_data in 
            loaded_data.items()
            }
