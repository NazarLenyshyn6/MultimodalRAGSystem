
import numpy as np
from abc import ABC, abstractmethod
 
from schema import BaseDocument

class VectorStoreI(ABC):
    """Interface class for VectorStore."""
    @abstractmethod
    def add_documents(self, 
                      documents: list[BaseDocument], 
                      embeddings: np.ndarray
                      ) -> None:
            ...

    @abstractmethod
    def clean(self) -> None:
         ...
    
    @abstractmethod
    def similarity_search(self, 
                          qeury: str, 
                          k: int, 
                          *args, 
                          **kwargs
                          ) -> list[BaseDocument]:
        ...