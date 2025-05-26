# Data Ingestion

# fetch.py
This module defines FetcherI, an abstract base class for web content fetchers, and RequestsFetcher, a concrete implementation that retrieves data from websites using the requests library. It handles different fetch-related exceptions and logs fetching outcomes.

# fetching_result.py
This module defines FetchResultI, a protocol specifying the interface for fetch result objects, and FetchResult, a Pydantic-based data transfer object (DTO) capturing details of web fetch operations. The DTO encapsulates metadata such as status codes, response data, headers, error messages, and timestamps.

# parsers.py
This module provides an abstract interface ParserI for parsing text data from raw website content, alongside a concrete implementation BS4Parser that uses BeautifulSoup4 to extract HTML elements based on configurable parsing rules. It includes rigorous type validation, error handling with custom exceptions, and detailed logging to support robust parsing workflows in web data ingestion pipelines.

# parsing_config.py
This module provides ParserConfig, a Pydantic data model that pairs tag identifiers with their parsing instructions, enforcing validation rules to ensure consistency and type safety. It also defines ParsedData, a container for structured parsed results from a URL, dynamically exposing parsed tag data as attributes for convenient access.

# pasing_tags.py
This module provides abstract interfaces and concrete data models to configure and represent HTML tags for parsing tasks. It enables parser-agnostic tag definitions and includes a BeautifulSoup-specific implementation (BS4Tag) for specifying tag names, attributes, recursion behavior, and result limits used in web scraping and HTML content extraction workflows.
