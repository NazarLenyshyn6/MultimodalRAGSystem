"""Defines configuration and result data classes for text parsing of HTML content."""


from typing import Optional, Literal, List, Dict

import pydantic

from DataIngestion import parsing_tags
from Internals.logger import logger


class ParserConfig(pydantic.BaseModel):
    """
    Configuration container for text parser tag mappings.

    Attributes:
        parsed_tags: A list of string identifiers corresponding to parsed tags extracted from text.

        tags: A list of tag configuration objects implementing the TagI interface.
              Each element provides detailed parsing instructions for a specific HTML tag or element.

    Raises:
        ValidationError: 
            - If 'parsed_tags' or 'tags' is empty.
            - If both list does not have the same lenght.
            - If not all elemnts is tag list has the same data type.
        
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    parsed_tags: List[str]
    tags: List[parsing_tags.TagI]

    @pydantic.model_validator(mode='after')
    def validate_parsed_tags_tags(cls, values):
        logger.info("ParserConfig validation.")
        parsed_tags = values.parsed_tags
        tags = values.tags
        if len(parsed_tags) == 0 or len(tags) == 0:
            logger.error(
                "ParserConfig validation failed: Either parsed_tags or tags is empty."
                )
            raise ValueError(
                'Neither parsed_tags nor tags can be empty.'
                )
        if len(parsed_tags) != len(tags):
            logger.error(
                "ParserConfig validation failed: parsed_tags and tags lengths mismatch."
                )
            raise ValueError(
                'parsed_tags and tags must have the same length.'
                )
        tag_type = type(tags[0])
        if not all(isinstance(tag, tag_type) for tag in tags):
            logger.error(
                "ParserConfig validation failed: Not all tags have the same type."
                )
            raise ValueError(
                'All objects in tags list must be of the same type.'
                )
        logger.info("ParserConfig validation done successfully.")
        return values

    def __repr__(self) -> str:
        return f'ParserConfig(parsed_tags={self.parsed_tags}, tags={[tag_.tag for tag_ in self.tags]})'
    
    def __iter__(self):
        return zip(self.parsed_tags, self.tags)
    

class ParsedData:
    """Structured result of parsing text from a given URL.

    Attributes:
        url: The source URL from which the text was parsed.. 
        parsed_tags: A list of string identifiers representing the tags. 
        parsed_data:  A list of parsed string data corresponding to each tag. 

    Dynamic Attributes:
        For each tag name in `parsed_tags`, an attribute is dynamically created on the instance
        with the tag name, holding the corresponding parsed data.

    """
    def __init__(self, 
                 url: str, 
                 parsed_data: Dict[str, list]
                 ) -> None:
        self.url = url 
        self.parsed_tags = parsed_data.keys()
        for parsed_tag, data in parsed_data.items():
            setattr(self, parsed_tag.lower(), data)

    def __repr__(self):
        return f'ParsedData(url={self.url}, parsed_tags={self.parsed_tags})'
    
    def get_all(self):
        """Returns a list of all extracted data."""
        all_data = []
        for parsed_tag in self.parsed_tags:
            all_data.extend(getattr(self, parsed_tag.lower()))
        return all_data
    