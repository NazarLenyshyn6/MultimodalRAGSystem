"""Defines interfaces and implementations for parsing structured data from fetched website content."""


from typing import Literal
from typing_extensions import override
from abc import ABC, abstractmethod

import pydantic
from bs4 import BeautifulSoup

from DataIngestion import fetching_result
from DataIngestion import parsing_configs
from DataIngestion import parsing_tags
from Internals import utils
from Internals.logger import logger
from CustomExceptions import fetch_exceptions
from CustomExceptions import parse_exceptions


class ParserI(ABC):
    """Interface for text parsers that parse structured data from raw website content."""

    @abstractmethod
    def parse(
        self, 
        website_responce: fetching_result.FetchResultI, 
        parser_config: parsing_configs.ParserConfig
        ) -> parsing_configs.ParsedData:
        ...


class BS4Parser(pydantic.BaseModel,ParserI):
    """Concrete implementation of TextParserI using BeautifulSoup4 to parse HTML content.

    Attributes:
        parser : The backend parser to use with BeautifulSoup. Defaults to 'html.parser'.

    Raises:
        ValidationError: If invalid backend parser specified.

    """
    parser: Literal['html.parser', 'lxml', 'html5lib'] = pydantic.Field(default='html.parser')

    @override
    def parse(
        self, 
        website_response: fetching_result.FetchResultI, 
        parser_config: parsing_configs.ParserConfig
        ) -> parsing_configs.ParsedData:
        """
        parses tagged content from HTML using BeautifulSoup based on the parsing configuration.

        Args:
            website_response : FetchResultI object containing fetching results.
            parser_config: Configuration defining mappings of field names to BS4Tag objects.

        Raises:
            FailedFatchingError: If data fetch was unsuccessful.
            TypeError: If any tag in parser_config.tags is not of type BS4Tag.
            BS4ParsingError: If data parsing fails.

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
                parsing_configs.ParserConfig
                ]
                )
        logger.info("BS4Parser parsing data from %s", website_response.url)
        if website_response.success == False:
            logger.error(
                "BS4Praser failed parsing data from %s: Data fatching failed.", website_response.url
                )
            raise fetch_exceptions.FatchingError(
                f"BS4Parser cannot parse HTML from {website_response.url}: website_response.success is False."
                )
        if not all(isinstance(tag, parsing_tags.BS4Tag) for tag in parser_config.tags):
            msg = "All tags in parser config must be instances of BS4Tag."
            logger.error(
                "BS4 Parser failed parsing data from %s: %s",
                website_response.url,
                msg
                )
            raise TypeError(msg)
        try:
            soup = BeautifulSoup(website_response.data, self.parser)
            parsed_data_dict = {}
            for parsed_tag, tag in parser_config:
                name, attrs, recursive, limit = tag.construct().values()
                parsed_data_dict[parsed_tag] = soup.find_all(name=name, 
                                                        attrs=attrs, 
                                                        recursive=recursive, 
                                                        limit=limit
                                                        )
            parsed_data = parsing_configs.ParsedData(url=website_response.url, 
                                                     parsed_data=parsed_data_dict
                                                     )
            logger.info(
                "BS4Parser successfully parsed data from %s", website_response.url
                )
            return parsed_data
        except Exception as e:
            msg = f"BS4Parser failed to parse content from {website_response.url}"
            logger.exception(msg)
            raise parse_exceptions.BS4ParsingError(msg) from e

