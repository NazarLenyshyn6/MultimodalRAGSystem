"""Data transfer objects for encapsulating the results of website fetch operations."""


from typing import Optional, Any, Protocol, runtime_checkable
from datetime import datetime

import pydantic
import  requests

@runtime_checkable
class FetchResultI(Protocol):
    """
    Interface class for encapsulating the results of website fetch operations.
    
    This protocol defines the expected fields for a fetch result. Any conforming implementation 
    should store metadata about the success or failure of a web fetch operation.
    """

    def __init__(
            self, 
            success: bool,
            status_code: int,
            responce: requests.models.Response,
            data: Optional[str],
            url: str,
            headers: Optional[dict],
            error_message: Optional[str],
            timestamp: datetime,
            meta: Optional[dict[str, Any]]
            ) -> None:
        raise NotImplementedError
    
class FetchResult(pydantic.BaseModel):
    """
    Data Transfer Object for the result of a web fetch operation.
    
    Attributes:
        success: Whether the fetch was successful.
        url: The URL that was fetched.
        data: The main body of the response in string format.
        status_code: HTTP status code returned by the server.
        headers: Response headers.
        error_message: Error details, if the fetch failed.
        timestamp: Time when the fetch occurred.
        meta: Additional metadata.
    """
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    success: bool 
    url: str
    response: Optional[requests.models.Response] = pydantic.Field(default=None, repr=False)
    status_code: Optional[int] = pydantic.Field(default=None, repr=False)
    data: Optional[str] = pydantic.Field(default=None, repr=False)
    headers: Optional[dict] = pydantic.Field(default=None, repr=False)
    error_message: Optional[str] =pydantic.Field(default=None, repr=False)
    timestamp: datetime = pydantic.Field(default_factory=datetime.now, repr=False)
    meta: Optional[dict[str, Any]] = pydantic.Field(default=None, repr=False)

    def __str__(self) -> str:
        return (
            "FetchResult(\n"
            f"  success: {self.success},\n"
            f"  status_code: {self.status_code},\n"
            f"  url: {self.url},\n"
            f"  responce: {self.response},\n"
            f"  data: {self.data},\n"
            f"  headers: {self.headers},\n"
            f"  error_message: {self.error_message},\n"
            f"  timestamp: {self.timestamp},\n"
            f"  meta: {self.meta}\n"
            ")"
        )