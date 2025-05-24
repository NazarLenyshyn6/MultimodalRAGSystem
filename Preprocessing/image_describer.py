"""."""

from typing import Optional
from typing_extensions import override
from abc import ABC, abstractmethod

import pydantic 
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

from Preprocessing import image_loaders
from schema import ImageDocument
from Internals import utils
from CustomExceptions import preprocessing_exceptions


class ImageDescriberI(ABC):
    """Interface class for image describer."""

    @abstractmethod
    def describe(self, image: image_loaders.LoadedImage) -> ImageDocument:
        ...

class BLIPImageDescriber(pydantic.BaseModel, ImageDescriberI):
    """Generate image descriptions using  Hugging Face BLIP model.

    Attributes:
        pretrained_model_name_or_path: Name or path to the pretrained BLIP model to load.
        processor: Optional pre-initialized BLIP processor. If None, it is loaded from pretrained.
        model: Optional pre-initialized BLIP model. If None, it is loaded from pretrained.

    Raises:
        ValidationError: If attribute does not match exptected data type.
        ImageDescriptionError: .
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    pretrained_model_name_or_path: str = pydantic.Field(default="Salesforce/blip-image-captioning-base")
    processor: Optional[BlipProcessor] = pydantic.Field(default=None, repr=False)
    model: Optional[BlipForConditionalGeneration] = pydantic.Field(default=None, repr=False)

    def model_post_init(self, context):
        if self.processor is None:
            self.processor =  BlipProcessor.from_pretrained(self.pretrained_model_name_or_path)
        if self.model is None:
            self.model = BlipForConditionalGeneration.from_pretrained(self.pretrained_model_name_or_path)

    @override
    def describe(self, image: image_loaders.LoadedImage) -> ImageDocument:
        """Generates a description for a give image.

        Args:
            image: An image object containing the image data (PIL Image) and the source URL
                    Instance of LoadedImage class.

        Raises:
            TypeError: If image is not LoadedImage type object.

        Returns:
            ImageDocument: Structured image document with image description.
        """
        utils.validate_dtypes(
            inputs=[image], 
            input_names=['image'], 
            required_dtypes=[image_loaders.LoadedImage]
            )
        try:
            inputs = self.processor(images=image.image, return_tensors='pt')
            with torch.no_grad():
                output = self.model.generate(**inputs)
            description = self.processor.decode(output[0], skip_special_tokens=True)
            return ImageDocument(id=utils.generate_unique_doc_id(content=description, metadata={}),
                                content=description,
                                image=image.image,
                                source_url=image.url,
                                image_url=image.url)
        except Exception as e:
            raise preprocessing_exceptions.ImageDescriptionError(message=f'BlipImageDescriber failed image description: {e}')