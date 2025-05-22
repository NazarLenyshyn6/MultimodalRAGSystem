from typing import Dict, Union, Literal, Optional
from typing_extensions import override
from abc import ABC, abstractmethod

import pydantic

ConstructedBS4Tag = Dict[str, Union[str, dict[str, str], bool, int, None]]

class TagI(ABC):
    """
    Abstract base class for tag objects used in HTML text parsing.

    Implementations of this interface must define the `construct()` method, 
    which returns a tuple of parameters required by a specific parser library 
    (e.g., BeautifulSoup, lxml) to locate and extract HTML elements.

    This abstraction allows parser-agnostic configurations and enables easy 
    extension to multiple parsing backends.
    """

    @abstractmethod
    def construct(self):
        """Construct and return the parameters needed for tag-based element extraction."""
        ...

class BS4Tag(pydantic.BaseModel, TagI):
    """Configuration object for specifying a tag used in BeautifulSoup-based HTML parsing.

    Attributes:
        tag: The HTML tag name to search for (e.g., 'h1', 'p', 'div').
            Only commonly text-based tags are allowed to enforce semantic correctness. 
        attrs: A dictionary of HTML attributes used to filter matching tags. 
        recursive: Whether to search for tags recursively within children.. 
        limit: Maximum number of results to return. If None, all matches are returned. 
    """
    tag: Literal['p', 'h1', 'h2', 
                 'h3', 'h4', 'h5', 
                 'h6','span','div', 
                 'a', 'li', 'strong', 
                 'b','em', 'i',
                 'blockquote','label', 'td', 
                 'th','caption', 'summary',
                 'code', 'pre', 'small',
                 'mark', 'cite', 'q', 
                 'abbr', 'time', 'figcaption', 
                 'article', 'section', 
                 'header', 'footer', 'aside', 
                 'main'
                 ]
    attrs: Optional[Dict[str, str]] = pydantic.Field(default=None)
    recursive: bool = pydantic.Field(default=True)
    limit: Optional[int] = pydantic.Field(default=None)
    extract: Optional[str] = pydantic.Field(default=None)

    def __str__(self):
        return repr(self)

    @override
    def construct(self) -> ConstructedBS4Tag:
        """
        Construct a dict representation of the tag configuration suitable 
        for BeautifulSoup's `find_all` method.

        Returns:
            Dict[str, Uniton[name, tag, attrs, recursive, limit]]
        """
        return {'name': self.tag, 
                'attrs': self.attrs or {}, 
                'recursive': self.recursive, 
                'limit': self.limit
                }