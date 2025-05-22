""" Module containing preconfigured data loaders ready to use instantly.

This module provides predefined parser configurations and data loader
instances tailored for common use cases, such as scraping news articles.
These loaders are fully set up with fetchers, parsers, and parsing configurations,
allowing quick integration without additional setup.
"""


from DataIngestion import fetch
from DataIngestion import parsing_tags 
from DataIngestion import parsing_configs
from DataIngestion import website_data_loaders
from DataIngestion import parsers

news_article_parser_config = parsing_configs.ParserConfig(
    parsed_tags=[
        'Title',
        'Author',
        'Published_date',
        'Content',
        'Summary',
        'Tags',
        'Paragraph',
        'Image',
        ], 
    tags=[
        parsing_tags.BS4Tag(tag="h1"),
        parsing_tags.BS4Tag(tag="span"),
        parsing_tags.BS4Tag(tag="time"),
        parsing_tags.BS4Tag(tag="div", recursive=True),
        parsing_tags.BS4Tag(tag="meta"),
        parsing_tags.BS4Tag(tag="li"),
        parsing_tags.BS4Tag(tag='p', recursive=True),
        parsing_tags.BS4Tag(tag="img"),
        ]
    )

news_article_loader = website_data_loaders.ScrapedDataLoader(fetcher=fetch.RequestsFetcher(),
                                                             parser=parsers.BS4Parser(),
                                                             parser_config=news_article_parser_config)