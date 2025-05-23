
from typing import List
from typing_extensions import override
from abc import ABC, abstractmethod

from langchain.text_splitter import RecursiveCharacterTextSplitter
import pydantic

from schema import TextDocument
from Internals.utils  import compute_hash_from_text
from Internals.utils import validate_dtypes


class TextSplitterI(ABC):
    @abstractmethod
    def split(self, text: str, source_url: str) -> List[TextDocument]:
        ...

class RecursiveTextSplitter(pydantic.BaseModel, TextSplitterI):
    """ A text splitter implementation using LangChain's RecursiveCharacterTextSplitter
        that splits input text into chunks and returns a list of TextDocument instances.

    Attributes:
        chunk_size: . 
        chunk_overlap: . 
        separators: . 
        splitter: . 

    Raises:
        ValidationError: If attributes does not match excpected data types.
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    chunk_size: int = pydantic.Field(default=1500)
    chunk_overlap: int = pydantic.Field(default=0)
    separators: List[str] = pydantic.Field(default=None)
    splitter: RecursiveCharacterTextSplitter =  pydantic.Field(default=None, repr=False)

    def model_post_init(self, context):
        if self.separators  is None:
            self.separators = ["\n\n", "\n", " ", ""]
        if self.splitter is None:
            self.splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size,
                                                           chunk_overlap=self.chunk_overlap,
                                                           )
        
    @override
    def split(self, text: str, source_url: str) -> List[TextDocument]:
        """
        Split the input text into chunks and wrap each chunk in a TextDocument.

        Args:
            text: The input text to split.
            source_url: URL of the text source.

        Raises:
            TypeError: If text or source_url (if not None) is not a string.

        Returns:
            List: List of text chunks wrapped as TextDocument.
        """
        validate_dtypes(
            inputs=[
                text, 
                source_url
                ],
            input_names=[
                'text',
                'source_url'
                ],
            required_dtypes=[
                str, 
                (str, type(None))
                ]
                )
        split_text = self.splitter.split_text(text)
        return [
            TextDocument(
                id=compute_hash_from_text(text),
                text=text,
                source_url=source_url
                ) 
                for text in split_text
                ]