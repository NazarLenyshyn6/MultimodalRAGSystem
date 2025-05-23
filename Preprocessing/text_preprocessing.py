

from typing import List, Any
from abc import ABC, abstractmethod

import bs4
import pydantic


class TextExtractorI(ABC):
    """Interface class for text extractor."""
    @abstractmethod
    def extract_text_from_elements(self, elements: List[Any]) -> str:
        ...

class SimpleBS4TextExtractor(pydantic.BaseModel, TextExtractorI):
    """Extract text from bs4 Tags.

    Attributes:
        separator: Used to join parts of text within a tag.
        strip : Whether to strip whitespace from each text part.
        join_symbol : Symbol used to join text across multiple tags.
    """

    separator: str = pydantic.Field(default = ' ')
    strip: bool  = pydantic.Field(default = True)
    join_symbol: str = '\n'

    def extract_text_from_elements(self, elements: List[bs4.element.Tag]) -> str:
        """Extract text from a list of bs4.element.Tag objects.

        Args:
            elements: List of BeautifulSoup tags.

        Raises: 
            TypeError: If elements is not a list or contains non-tag objects.

        Returns:
            str: Extracted and concatenated text.
        """
        text = []
        if not isinstance(elements, list):
            raise TypeError('Elements must be a list of tags.')
        for tag in elements:
            if not isinstance(tag,  bs4.element.Tag):
                raise TypeError('All tags must be of type bs4.element.Tag')
            text.append(tag.get_text(separator=self.separator, strip=self.strip))
        return self.join_symbol.join(text)
