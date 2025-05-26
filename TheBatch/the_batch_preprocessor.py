from typing import List, Any, Union

import pydantic

from Preprocessing.text_extraction import TextExtractorI
from Preprocessing.text_extraction import SimpleBS4TextExtractor
from Preprocessing.text_spitting import TextSplitterI
from Preprocessing.text_spitting import RecursiveTextSplitter
from Preprocessing.image_describer import ImageDescriberI
from Preprocessing.image_describer import BLIPImageDescriber
from Preprocessing.image_loaders import ImageLoaderI
from Preprocessing.image_loaders import RequestsImageLoader
from DataIngestion.parsing_configs import ParsedData
from Schema.schema import BaseDocument, TextDocument, ImageDocument
from Internals.logger import logger


class TheBatchPreprocessor(pydantic.BaseModel):
    """ Preprocessor for extracting, splitting, loading, and describing multimodal data from The Batch site.

    This class integrates text and image preprocessing steps to prepare multimodal data for downstream use
    (e.g., RAG, embedding models, etc.). It relies on custom framework components for each step.

    Attributes:
        text_extractor (TextExtractorI): 
            Component responsible for extracting text from parsed HTML elements.
            Defaults to SimpleBS4TextExtractor.

        text_splitter (TextSplitterI): 
            Component responsible for splitting extracted text into manageable chunks for downstream tasks.
            Defaults to RecursiveTextSplitter.

        image_loader (ImageLoaderI): 
            Component responsible for downloading and loading images from URLs.
            Defaults to RequestsImageLoader.

        image_describer (ImageDescriberI): 
            Component responsible for generating natural language descriptions of images.
            Defaults to BLIPImageDescriber.

    Raises:
        ValidationError: If attributes does not match extecped data type.

    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    text_extractor: TextExtractorI = pydantic.Field(default=SimpleBS4TextExtractor())
    text_splitter: TextSplitterI = pydantic.Field(default=RecursiveTextSplitter())
    image_loader: ImageLoaderI = pydantic.Field(default=RequestsImageLoader())
    image_describer: ImageDescriberI = pydantic.Field(default=BLIPImageDescriber())

    def preprocess(self, 
                   source_url: str, 
                   elements: List[Any], 
                   images_urls: List[str]
                   ) -> List[Union[TextDocument, ImageDocument]]:
        """ Executes the preprocessing steps for multimodal data.

        Args:
            source_url: The source URL of the fetched content (for context during text splitting).
            elements: Parsed HTML elements containing text to be extracted.
            images_urls: List of image URLs to download and describe.

        Returns:
            List[Unition[TextDocument, ImageDocument]]: A list containing TextDocuments and ImageDocuments.
        """
        logger.info(
            "TheBatchDataPreprocessor preprocessing, extracting text from elements using %s", self.text_extractor
            )
        extracted_text = self.text_extractor.extract_text_from_elements(elements=elements)
        logger.info(
            "TheBatchDataPreprocessor successfully extracted text using %s, splitting extracted text using %s", 
            self.text_extractor, 
            self.text_splitter
            )
        splitted_text = self.text_splitter.split(text=extracted_text, source_url=source_url)
        logger.info(
            "TheBatchDataPreprocessor successfully splitted text using %s, loading images using %s", 
            self.text_splitter, 
            self.image_loader
            )
        loaded_images = [self.image_loader.load(img_url=image_url) for image_url in images_urls]
        loaded_images = [image for image in loaded_images if image is not None]
        logger.info(
            "TheBatchDataPreprocessor successfully loaded images using %s, generating image descritions for loaded images using %s", 
            self.image_loader, 
            self.image_describer
            )
        image_descriptions = [self.image_describer.describe(image) for image in loaded_images]
        logger.info(
            "TheBatchDataPreprocessor seccussfully generated image descriptinos using %s, preprocessing done successfully.", 
            self.image_describer
            )
        preprocessed_docs = splitted_text + image_descriptions
        return preprocessed_docs