from DataIngestion import fetch
from DataIngestion import parsers
from DataIngestion import parsing_tags
from DataIngestion import parsing_configs

fetcher = fetch.RequestsFetcher()
parser = parsers.BS4Parser()

the_batch_parser_config = parsing_configs.ParserConfig(
    parsed_tags=[
        "article_title",
        "publication_date",
        "author_name",
        "main_content",
        "images",
        "captions",
        "tags",
        "parahraph"
        ], 
    tags=[
        parsing_tags.BS4Tag(tag="h1"),
        parsing_tags.BS4Tag(tag="time"),
        parsing_tags.BS4Tag(tag="span", 
                            attrs={'class': "author"}),
        parsing_tags.BS4Tag(tag="div", 
                            # attrs={'class': "article-content"}, 
                            recursive=True),
        parsing_tags.BS4Tag(tag="img"),
        parsing_tags.BS4Tag(tag="figcaption"),
        parsing_tags.BS4Tag(tag="a", attrs={'class': 'tag'}),
        parsing_tags.BS4Tag(tag="p", recursive=True)
        ]
    )