
from typing import List, Optional
from typing_extensions import override
from abc import ABC, abstractmethod

from PIL import Image
import numpy as np
import torch
import pydantic
from transformers import CLIPProcessor, CLIPModel

from Internals import utils
from Internals.logger import logger
from CustomExceptions import embedding_exceptions

class ImageEmbeddingI(ABC):
    """Interface class for image embedding."""

    @abstractmethod
    def encode(self, images: List[Image.Image]) -> np.ndarray:
        ...

class CLIPImageEmbedding(pydantic.BaseModel, ImageEmbeddingI):
    """Image embedding using CLIP from HuggingFace.

    Attributes:
        model_name_or_path: HuggingFace hub model ID or path to local model.
        model: The CLIP model instance.
        processor: CLIP processor for preparing image inputs.

    Raises:
        ImageEmbeddingError: If any exception happens during model or processor loading.
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    model_name_or_path: str = pydantic.Field(default="openai/clip-vit-base-patch32")
    model: Optional[CLIPModel] = pydantic.Field(default=None)
    processor: Optional[CLIPProcessor] = pydantic.Field(default=None)

    def model_post_init(self, context):
        """CLIPImageEmbedding initialization."""
        if self.model is None:
            try:
                self.model = CLIPModel.from_pretrained(self.model_name_or_path)
            except Exception as e:
                msg = f'CLIPImageEmbedding initialization failed due to error in CLIPModel.from_pretrained with {self.model_name_path} model_name_or_path.'
                logger.exception(msg)
                raise embedding_exceptions.ImageEmbeddingError(msg) from e
        if self.processor is None:
            try:
                self.processor = CLIPProcessor.from_pretrained(self.model_name_or_path)
            except Exception as e:
                msg = f'CLIPImageEmbedding initialization failed due to error in CLIPProcessor.from_pretraied with {self.model_name_or_path} model_namae_or_path.'
                logger.exception(msg)
                raise embedding_exceptions.ImageEmbeddingError(msg) from e
        logger.info("CLIPImageEmbedding initialization done successfully.")

    @override
    def encode(self, images: list[Image.Image]) -> np.ndarray:
        """Computes image embeddings.

        Args:
            images: List of Images to embed.

        Raises:
            TypeError: If images is not a list or contains not Image.Image objects.
            ImageEmbeddingError: If the embedding process fails.

        Returns:
            The image embeddings obtained by applying the projection layer to the pooled output of [CLIPVisionModel].
        """
        utils.validate_dtypes(
            inputs=[images], 
            input_names=['images'], 
            required_dtypes=[list]
            )
        for image in images: 
            utils.validate_dtypes(
                inputs=[image], 
                input_names=['image'], 
                required_dtypes=[Image.Image]
                )
        try:
            logger.info("ClipImageEmbedding encoding images.")
            inputs = self.processor(images=images, return_tensors="pt")
            embeddings = self.model.get_image_features(**inputs)
            np_embeddings = embeddings.detach().cpu().numpy().astype(np.float32)
            logger.info("ClipImageEmbedding successfully encoded images.")
            return np_embeddings
        except Exception as e:
            msg = "CLIPImageEmbedding failed image embedding."
            logger.exception(msg)
            raise embedding_exceptions.ImageEmbeddingError(msg) from e