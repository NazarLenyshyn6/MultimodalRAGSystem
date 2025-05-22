
from typing_extensions import override
from abc import ABC, abstractmethod

import pydantic

from DataIngestion import fetch
from DataIngestion import parsers
from DataIngestion import parsing_configs


class DataLoaderI(ABC):
    "Interface for all data loaders that transform a URL into parsed data."

    @abstractmethod
    def load(self, url: str, *args, **kwargs):
        ...

class ScrapedDataLoader(pydantic.BaseModel, DataLoaderI):
    """Concrete implementation of `DataLoaderI` that uses a fetcher and parser
       to load and parse structured data from a URL.

    This loader:
        - Uses a `FetcherI` implementation to retrieve raw website data.
        - Uses a `ParserI` implementation to extract structured data from the raw content.
        - Uses a `ParserConfig` to configure what data should be extracted.

    Attributes:
        fetcher : An object responsible for fetching content from the URL.
        parser: An object responsible for extracting structured data.
        parser_config: Configuration for the parser describing which elements to extract.

    Raises:
        ValidationError: If attribute does not match expected data type.
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    fetcher: fetch.FetcherI
    parser: parsers.ParserI
    parser_config: parsing_configs.ParserConfig

    def __repr__(self) -> str:
        return (f"DataLoader(\n"
                f"Fetcher: {self.fetcher}\n"
                f"Parser: {self.parser}\n"
                f"Parser Config: {str(self.parser_config)}\n"
                f")"
                )
    
    @override
    def load(self, url: str, *fetching_args, **fetching_kwargs) -> parsing_configs.ParsedData:
        """ Loads and parses data from a URL using the configured fetcher and parser.

        Steps:
            1. Fetches content using the `fetcher`.
            2. Parses the fetched content using the `parser` and `parser_config`.

        Args:
            url: The target URL to fetch and parse.
            *fetching_args: Additional positional arguments passed to the fetcher.
            **fetching_kwargs: Additional keyword arguments passed to the fetcher.

        Returns:
            ParsedData: A structured object representing the parsed data.

        Raises:
            Any exception raised by the fetcher or parser, for more details read documentations of used fetcher and parser.
        """
        website_response = self.fetcher.fetch(url, *fetching_args, **fetching_kwargs)
        return self.parser.extract(website_response, self.parser_config)