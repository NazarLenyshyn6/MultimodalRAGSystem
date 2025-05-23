
from typing import List, Optional
from abc import ABC, abstractmethod

from PIL import Image
import numpy as np
import torch
import pydantic
from transformers import CLIPProcessor, CLIPModel

from Internals import  utils

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
        preprocessor: CLIP processor for preparing image inputs.
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    model_name_or_path: str = pydantic.Field(default="openai/clip-vit-base-patch32")
    model: Optional[CLIPModel] = pydantic.Field(default=None)
    preprocessor: Optional[CLIPProcessor] = pydantic.Field(default=None)

    def model_post_init(self, context):
        if self.model is None:
            self.model = CLIPModel.from_pretrained(self.model_name_or_path)
        if self.preprocessor is None:
            self.preprocessor = CLIPProcessor.from_pretrained(self.model_name_or_path)

    def encode(self, images: list[Image.Image]) -> np.ndarray:
        """Computes image embeddings.

        Args:
            images: List of Images to embed.

        Raises:
            TypeError: If images is not a list or contains not Image.Image objects.

        Returns:
            The image embeddings obtained by applying the projection layer to the pooled output of [CLIPVisionModel].
        """
        utils.validate_dtypes([images], ['images'], [list])
        for image in images: utils.validate_dtypes([image], ['image'], [Image.Image])
        inputs = self.preprocessor(images=images, return_tensors="pt")
        embeddings = self.model.get_image_features(**inputs)
        return embeddings.detach().cpu().numpy().astype(np.float32)