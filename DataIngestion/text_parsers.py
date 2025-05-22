from typing import Literal
from typing_extensions import override
from abc import ABC, abstractmethod


import pydantic
from bs4 import BeautifulSoup

from DataIngestion import fetching_result
from DataIngestion import text_parsing_configs
from DataIngestion import text_parsing_tags
from Internals import utils

class TextParserI(ABC):
    """Interface for text parsers that extract structured data from raw website content."""

    @abstractmethod
    def extract(self, website_responce: fetching_result.FetchResultI, parser_config: text_parsing_configs.TextParserConfig) -> text_parsing_configs.ParsedText:
        ...


class BS4TextParser(pydantic.BaseModel,TextParserI):
    """Concrete implementation of TextParserI using BeautifulSoup4 to extract HTML content.

    Attributes:
        parser : The backend parser to use with BeautifulSoup. Defaults to 'html.parser'.

    Raises:
        ValidationError: If invalid backend parser specified.

    """
    parser: Literal['html.parser', 'lxml', 'html5lib'] = pydantic.Field(default='html.parser')

    @override
    def extract(self, website_response: fetching_result.FetchResultI, parser_config: text_parsing_configs.TextParserConfig) -> text_parsing_configs.ParsedText:
        """
        Extracts tagged content from HTML using BeautifulSoup based on the parsing configuration.

        Args:
            website_response : FetchResultI object containing fetching results.
            parser_config: Configuration defining mappings of field names to BS4Tag objects.

        Raises:
            RuntimeError: If data fetch was unsuccessful.
            TypeError: If any tag in parser_config.tags is not of type BS4Tag.

        """
        utils.validate_dtypes(
            inputs=[
                website_response, 
                parser_config
                ],
            input_names=[
                'website_response', 
                'parser_config'
                ],
            required_dtypes=[
                fetching_result.FetchResultI, 
                text_parsing_configs.TextParserConfig
                ]
                        )
        if website_response.success == False:
            raise RuntimeError("Cannot parse HTML: website_response.success is False.")
        if not all(isinstance(tag, text_parsing_tags.BS4Tag) for tag in parser_config.tags):
            raise TypeError("All tags in parser_config must be instances of BS4Tag.")
        soup = BeautifulSoup(website_response.data, self.parser)
        parsed_data = {}
        for parsed_tag, tag in parser_config:
            name, attrs, recursive, limit = tag.construct().values()
            raw_data = soup.find_all(name=name, attrs=attrs, recursive=recursive, limit=limit)
            data = [d.get(tag.extract) for d in raw_data] if tag.extract else [d.text for d in raw_data]
            parsed_data[parsed_tag] = data
        return text_parsing_configs.ParsedText(url=website_response.url, parsed_data=parsed_data)
