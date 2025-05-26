import pydantic

from TheBatch.the_batch_configs import the_batch_parser_config
from DataIngestion.fetch import FetcherI
from DataIngestion.fetch import RequestsFetcher
from DataIngestion.parsers import ParserI
from DataIngestion.parsers import BS4Parser
from DataIngestion.parsing_configs import ParsedData
from DataIngestion.parsing_configs import ParserConfig
from Internals.logger import logger

class TheBatchDataLoader(pydantic.BaseModel):
    """ Loader for retrieving and parsing data from The Batch website.

        This class integrates fetching and parsing logic using custom framework modules,
        enabling seamless loading of multimodal data (text, images) from The Batch site.

    Attributes:
        fetcher (FetcherI): 
            An instance responsible for fetching raw data from The Batch site.
            Defaults to a Requests-based fetcher (`RequestsFetcher`).

        parser (ParserI): 
            An instance responsible for parsing fetched HTML content.
            Defaults to a BeautifulSoup-based parser (`BS4Parser`).

        parser_config (ParserConfig): 
            Configuration object defining tag mappings and parsing rules specific to The Batch.
            Defaults to a predefined `the_batch_parser_config`.

    Raises:
        ValidationError: If attributes does not match expected data type. 
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    fetcher: FetcherI = pydantic.Field(default=RequestsFetcher())
    parser: ParserI = pydantic.Field(default=BS4Parser())
    parser_config: ParserConfig = pydantic.Field(default=the_batch_parser_config)

    def load(self, url: str) -> ParsedData:
        """Fetches HTML content from the specified URL and parses it into a structured format."""
        logger.info(
            "TheBatchDataLoader fetching data from %s using %s", 
            url, 
            self.fetcher
            )
        the_batch_response = self.fetcher.fetch(url)
        logger.info(
            "TheBatchDataLoader successfully fetched data from %s, now parsing using %s",
            url, 
            self.parser
            )
        the_batch_parsed_data = self.parser.parse(website_response=the_batch_response,
                                                  parser_config=self.parser_config)
        logger.info(
            "TheBatchDataLoader successfully loaded data from %s",
            url
            )
        return the_batch_parsed_data