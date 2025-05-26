"""Defines structured document models for multimodal data with medata support."""

from typing import Literal, Optional, Protocol, runtime_checkable, Union, Dict, Any, Union, ClassVar

import pydantic
from PIL import Image


@runtime_checkable
class BaseDocument(Protocol):
    """Base structured document."""

    id: str
    type: ClassVar
    content: str 

    @property
    def metadata(self) -> Dict[str, Any]:
        ...

class TextDocument(pydantic.BaseModel):
    """ Structured text document.

    Attributes:
        id: A unique identifier for the document, typically a hash of the content.
        type: The type of the document, fixed to the string 'text'.
        content: Text content of the document.
        source_url: The original source URL from which the text was extracted.
    """

    id: str
    type: ClassVar = 'text'
    content: str
    source_url: str = None

    @property
    def metadata(self) -> Dict[str, str]:
        return {'id': self.id,
                'type': self.type,
                'content': self.content,
                'source_url': self.source_url
                }

class ImageDocument(pydantic.BaseModel):
    """ Structured image document.

    Attributes:
        id: A unique identifier for the image, typically a hash of the image_url.
        type: The type of the document, fixed to the string 'image'.
        content: The loaded image object.
        source_url: The original source URL from which the image was extracted.
        image_url: The direct URL to the image content (can differ from source_url).
    """
    
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    id: str
    type: ClassVar = 'image'
    content: str
    image: Optional[Union[Image.Image]] =  pydantic.Field(default=None)
    source_url: str
    image_url: str

    @property
    def metadata(self) -> Dict[str, Union[Image.Image, str]]:
        return {'id': self.id,
                'type': self.type,
                'content': self.content,
                'source_url': self.source_url,
                'image_url': self.image_url}