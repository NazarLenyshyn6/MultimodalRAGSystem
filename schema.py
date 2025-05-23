from typing import Literal, Optional

import pydantic
from PIL import Image


class TextDocument(pydantic.BaseModel):
    """ Structured text document.

    Attributes:
        id: A unique identifier for the document, a hash of the content.
        type: The type of the document, fixed to the string 'text'.
        text: The content of the document.
        source_url: The original source URL from which the text was extracted.
    """
    id: str
    type: Literal['text'] = pydantic.Field(default='text')
    text: str
    source_url: str


class ImageDocument(pydantic.BaseModel):
    """ Structured image document.

    Attributes:
        id: A unique identifier for the image, typically a hash of the image_url.
        type: The type of the document, fixed to the string 'image'.
        image: The loaded image object.
        source_url: The original source URL from which the image was extracted.
        image_url: The direct URL to the image content (can differ from source_url).
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    id: str
    type: Literal['image'] = pydantic.Field(default='image')
    image: Image.Image
    source_url: str
    image_url: str