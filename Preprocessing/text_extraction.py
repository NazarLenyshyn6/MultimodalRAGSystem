

from typing_extensions import override
from typing import List, Any
from abc import ABC, abstractmethod

import bs4
import pydantic

from Internals import utils
from CustomExceptions import preprocessing_exceptions


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

    @override
    def extract_text_from_elements(self, elements: List[bs4.element.Tag]) -> str:
        """Extract text from a list of bs4.element.Tag objects.

        Args:
            elements: List of BeautifulSoup tags.

        Raises: 
            TypeError: If elements is not a list or contains non-tag objects.
            TextExtractionError: .

        Returns:
            str: Extracted and concatenated text.
        """
        text = []
        utils.validate_dtypes(
            inputs=[elements], 
            input_names=['elements'], 
            required_dtypes=[list]
            )
        try:
            for tag in elements:
                utils.validate_dtypes(
                    inputs=[tag], 
                    input_names=['tag'],
                    required_dtypes=[bs4.element.Tag]
                    )
                text.append(tag.get_text(separator=self.separator, strip=self.strip))
            return self.join_symbol.join(text)
        except Exception as e:
            raise preprocessing_exceptions.TextExtractionError(message=f"SimpleBS4TextExtractor failed text extraction: {e}")

