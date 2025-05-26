"""Defines an interface protocol for custom vector stores supporting document addition, similarity search, and persistence."""

from typing import Protocol, runtime_checkable

import numpy as np
 
from Schema.schema import BaseDocument

@runtime_checkable
class VectorStoreI(Protocol):
    """Interface class for custom VectorStore."""

    def __init__(self, persist_directory: str):
        ...

    def add_documents(self, 
                      documents: list[BaseDocument], 
                      embeddings: np.ndarray
                      ) -> None:
            ...
    
    def similarity_search(self, 
                          qeury: str, 
                          k: int, 
                          *args, 
                          **kwargs
                          ) -> list[BaseDocument]:
        ...

    def save(self) -> None:
     ...
     
    def load(self, vectorestore_path: str) ->  None:
        ...