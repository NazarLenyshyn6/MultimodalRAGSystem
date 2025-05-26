
from langchain.prompts import PromptTemplate

from DataIngestion import fetch
from DataIngestion import parsers
from DataIngestion import parsing_tags
from DataIngestion import parsing_configs

THE_BATCH_ULRS_PATH = r"C:\Users\User\Desktop\MultimodalRAGSystem\TheBatch\the_batch_urls.txt"
COLLECTION_NAME = "TheBatch"
TEH_BATCH_VECTORESTORE_PERSIST_DIR = r"C:\Users\User\Desktop\MultimodalRAGSystem\TheBatch\the_batch_vectorestore_persist_dir"
THE_BATCH_IMAGE_DOCUMENTS_STORE = r"C:\Users\User\Desktop\MultimodalRAGSystem\TheBatch\the_batch_image_documents_store.json"
CREATE_VECTORESTORE = False  

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
                            recursive=True),
        parsing_tags.BS4Tag(tag="img"),
        parsing_tags.BS4Tag(tag="figcaption"),
        parsing_tags.BS4Tag(tag="a", attrs={'class': 'tag'}),
        parsing_tags.BS4Tag(tag="p", recursive=True)
        ]
    )

the_batch_prompt_template = PromptTemplate(
    input_variables=["context", "user_query"],
    template="""
You are an advanced AI assistant. 
Your task is to provide a **detailed and explicit** response to the question **based strictly on the information provided in the context below**.
You must not incorporate any information beyond what is given in the context. You must not reference or mention the context explicitly or state that the information is from a source.
Your answer must be **as detailed, comprehensive, and explicit as possible** based solely on the provided context, covering all relevant details.

Context:
{context}

Question:
{user_query}

Instructions:
- Provide a detailed, explicit, and comprehensive answer strictly using the information from the context.
- Do not reference or mention the context or its presence.
- If the context does not contain enough information to answer the question, respond with:
"The information provided from TheBatch is insufficient to fully answer this question."
"""
)



