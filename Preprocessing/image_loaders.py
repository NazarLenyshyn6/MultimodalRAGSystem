"""Defines interfaces and concrete implementations for loading images from URLs"""

from  typing_extensions import override
from abc import ABC, abstractmethod
from PIL import Image
from io import BytesIO

import pydantic

from DataIngestion import fetch
from Internals import utils
from Internals.logger import logger

from CustomExceptions import fetch_exceptions
from CustomExceptions import preprocessing_exceptions

class LoadedImage:
    """ Wrapper for a loaded image along with its source URL.

    Attributes:
        url: The URL from which the image was loaded.
        image: The loaded image object.
    """
    
    def __init__(self, url: str, image: Image.Image):
        self.url = url
        self.image = image

    def __repr__(self) -> str:
        return f'LoadedImage(url={self.url})'
    

class ImageLoaderI(ABC):
    """Interface class for image loaders."""
    @abstractmethod
    def load(
        self, 
        img_url: str, 
        handle_exception: bool, 
        *fetching_args, 
        **fetching_kwargs
        ) -> None | LoadedImage:
        ...


class RequestsImageLoader(pydantic.BaseModel, ImageLoaderI):
    """ Image loader implementation that uses the `RequestsFetcher` to fetch image data
        and PIL to load the image from bytes.

    Attributes:
        fetcher: The fetcher instance used to get raw image bytes.

    Raises:
        ValidationError: If fetcher is  not  of type  RequestsFetcher.
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    fetcher: fetch.RequestsFetcher = pydantic.Field(default_factory=fetch.RequestsFetcher)

    @override
    def load(
            self, 
            img_url: str, 
            handle_exception: bool = True,
            params: dict = None, 
            headers: dict = None, 
            cookies: dict = None, 
            meta_data: dict = None
            ) -> LoadedImage:
        """ Load an image from a given URL.

        Args:
            url: The HTTP/HTTPS URL of the image to fetch.
            handle_exception: Whether to suppress exceptions and return None on failure.Defaults to True.
            params: Query parameters to send with the HTTP request.
            headers: HTTP headers to send with the request.
            cookies: Cookies to send with the request.
            meta_data: Additional metadata for the fetcher.

        Raises:
            ValueError: If URL does not start with http/https and handle_exception is False.
            FailedFatchingError: If fetching fails and handle_exception is False.
            ImageLoadingError: If image loading fails. 

        Returns:
            LoadedImage or None: LoadedImage instance on success, None if failure and handle_exception is True.
        """
        logger.info(f"RequestsImageLoader loading image from {img_url}")
        utils.validate_dtypes(
            inputs=[img_url], 
            input_names=['img_url'], 
            required_dtypes=[str]
            )
        if not img_url.startswith('http'):
            if handle_exception:
                return None
            raise ValueError("URL must start with http/https.")
        image_responce = self.fetcher.fetch(url=img_url, 
                                            params=params, 
                                            headers=headers, 
                                            cookies=cookies, 
                                            meta_data=meta_data
                                            )
        if image_responce.success is False:
            msg = "RequestsImageLoader cannot load image from {img_url}: website_response.success is False."
            logger.error(msg)
            if handle_exception:
                return None
            raise fetch_exceptions.FatchingError(msg) from e
        try:
            loaded_image = LoadedImage(url=img_url, 
                                       image=Image.open(BytesIO(image_responce.response.content))
                                       )
            logger.info(f"RequestsImageLoader successfully loaded image from {img_url}")
            return loaded_image
        except Exception as e:
            msg = f"RequestsImageLoader failed to load image from {img_url}"
            logger.exception(msg)
            if handle_exception:
                return None
            raise preprocessing_exceptions.ImageLoadingError(msg) from e