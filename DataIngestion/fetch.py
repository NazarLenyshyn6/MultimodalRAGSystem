"""Provides an interface and a requests-based implementation for fetching web content."""


from typing import Any, Union, Tuple
from abc import ABC, abstractmethod
from typing_extensions import override

import requests

from DataIngestion import fetching_result
from Internals import utils
from Internals.logger import logger

TimeoutType = Union[int, float, Tuple[Union[int, float], Union[int, float]]]

class FetcherI(ABC):
    """Interface class for website fetcher."""

    @abstractmethod
    def fetch(self, 
              url: str, 
              *fetching_args, 
              **fetching_kwargs
              ) -> fetching_result.FetchResultI:
        ...

class RequestsFetcher(FetcherI):
    """Fetch data from a website using the requests library.

    Args:
        timeout: Maximum amount of time (in seconds) that the request will wait for.
    
    Raises:
        TypeError: If timeout is not a single int | float number or tuple with two int | flaot numbers.
    """
    def __init__(self, timeout: TimeoutType = 10):
        self._validate_timeout(timeout)
        self.timeout = timeout

    def __repr__(self) -> str:
        return f'RequestsFetcher(timeout={self.timeout})'
    
    @staticmethod
    def _validate_timeout(timeout: Any) -> None:
        if isinstance(timeout, (int, float)):
            return
        if (isinstance(timeout, tuple) and 
            len(timeout) == 2 and 
            all(isinstance(t, (int, float)) for  t  in timeout)
            ):
            return
        raise TypeError("Timeout must be a single int/float or a tuple of two int/float values.")
    
    @override
    def fetch(
        self, 
        url: str, 
        params: dict = None, 
        headers: dict = None, 
        cookies: dict =None, 
        meta_data: dict = None
        ) -> fetching_result.FetchResult:
        """Fetch data from Website.

        Args:
            url: The URL to request.
            params: Dictionary to send in the query string. 
            headers: Custom HTTP headers to send. 
            cookies: Cookies to send with the request.
            meta_data: Additional metadata.

        Raises:
            TypeError: If any of argument does not match expected data type.

        Returns:
            FetchResult: The result of a web fetch operation.
        """
        utils.validate_dtypes(
            inputs=[
                url, 
                params, 
                headers, 
                cookies, 
                meta_data
                ],
            input_names=[
                'url', 
                'params', 
                'headers', 
                'cookies', 
                'meta_data'
                ],
            required_dtypes=[
                str, 
                (dict, type(None)), 
                (dict, type(None)), 
                (dict, type(None)), 
                (dict, type(None))]
                )
        try:
            logger.info('RequestsFetcher fetching url %s', url)
            response = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=self.timeout)
            response.raise_for_status()
            fetch_result = fetching_result.FetchResult(success=True,
                                                       url=url,
                                                       response=response,
                                                       data=response.text,
                                                       status_code=response.status_code,
                                                       headers=response.headers,
                                                       meta=meta_data
                                                       )
            logger.info('RequestsFetcher successfully fetched data from %s', url)
            return fetch_result
        except requests.exceptions.Timeout as e:
            logger.exception(
                "RequestsFetcher failed fetching data from %s", url
                )
            return fetching_result.FetchResult(success=False, 
                                               url=url, 
                                               error_message="Timeout occured.", 
                                               meta=meta_data
                                               )
        except requests.exceptions.HTTPError as e:
            logger.exception(
                "RequestsFetcher failed fetching data from %s due to HTTP error.", url
                )
            return fetching_result.FetchResult(
                success=False,
                url=url,
                status_code=e.response.status_code if e.response else None,
                error_message=f"HTTP error: {e}",
                headers=(e.response.headers) if e.response else None,
                meta=meta_data
            )
        except requests.exceptions.ConnectionError as e:
            logger.exception(
                "RequestsFetcher failed fetching data from %s due to Connection error.", url 
                )
            return fetching_result.FetchResult(success=False, 
                                               url=url, 
                                               error_message="Connection error: {e}", 
                                               meta=meta_data
                                               )
        except requests.exceptions.SSLError as e:
            logger.exception(
                "RequestsFetcher failed fetching data from %s due to SSL error.", url
                )
            return fetching_result.FetchResult(success=False, 
                                               url=url, 
                                               error_message="SSL error: {e}", 
                                               meta=meta_data
                                               )
        except requests.exceptions.RequestException as e:
            logger.exception("RequestsFethcher failed fethcing data from %s.", url)
            return fetching_result.FetchResult(success=False, 
                                               url=url, 
                                               error_message=str(e), 
                                               meta=meta_data
                                               )
        except Exception as e:
            logger.exception(
                "RequestsFetcher failed fetching data from %s", url, 
                )
            return fetching_result.FetchResult(success=False, 
                                               url=url, 
                                               error_message=str(e), 
                                               meta=meta_data
                                               )