from typing import Dict, Union, Literal, Optional
from typing_extensions import override
from abc import ABC, abstractmethod

import pydantic

ConstructedBS4Tag = Dict[str, Union[str, dict[str, str], bool, int, None]]
HTMLTag = Literal[
    'a', 'abbr', 'address', 'area', 'article', 'aside', 'audio',
    'b', 'base', 'bdi', 'bdo', 'blockquote', 'body', 'br', 'button',
    'canvas', 'caption', 'cite', 'code', 'col', 'colgroup',
    'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'div', 'dl', 'dt',
    'em', 'embed',
    'fieldset', 'figcaption', 'figure', 'footer', 'form',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hr', 'html',
    'i', 'iframe', 'img', 'input', 'ins',
    'kbd',
    'label', 'legend', 'li', 'link',
    'main', 'map', 'mark', 'meta', 'meter',
    'nav', 'noscript',
    'object', 'ol', 'optgroup', 'option', 'output',
    'p', 'param', 'picture', 'pre', 'progress',
    'q',
    'rp', 'rt', 'ruby',
    's', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strong', 'style', 'sub', 'summary', 'sup',
    'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track',
    'u', 'ul',
    'var', 'video',
    'wbr'
]


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
        attrs: A dictionary of HTML attributes used to filter matching tags. 
        recursive: Whether to search for tags recursively within children.. 
        limit: Maximum number of results to return. If None, all matches are returned. 
    """
    tag: HTMLTag
    attrs: Optional[Dict[str, str]] = pydantic.Field(default=None)
    recursive: bool = pydantic.Field(default=True)
    limit: Optional[int] = pydantic.Field(default=None)

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
        return {
            'name': self.tag, 
            'attrs': self.attrs or {}, 
            'recursive': self.recursive, 
            'limit': self.limit
            }