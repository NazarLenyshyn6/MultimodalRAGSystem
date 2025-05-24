

from typing_extensions import override
from abc import ABC, abstractmethod


import numpy as np
from sklearn import random_projection

from Internals import utils
from CustomExceptions import embedding_exceptions

class VectorProjectionI:
    """Interface class for vector projection."""
    @abstractmethod
    def project(self, vector: np.ndarray, target_dim) -> np.ndarray:
        ...

class GaussianRandomVectorProjection(VectorProjectionI):
    """Reduce dimensionality through Gaussian random projection."""

    @staticmethod
    @override
    def project(vector: np.ndarray, target_dim: np.ndarray):
        """Project input vector to taget dimention.

        Args:
            vector: Input vector for dimentionality reduction.
            target_dim: Target dimentionality.

        Raises:
            TypeError: If argument type does not match exptected data type.
            VectorProjectionError: .

        Returns:
            np.ndarray: Vector with target dimentionality.
        """
        utils.validate_dtypes(
            inputs=[
                vector, 
                target_dim
                ], 
            input_names=[
                'vector', 
                'target_dim'
                ], 
            required_dtypes=[
                np.ndarray, 
                int
                ]
            )
        try:
            return random_projection.GaussianRandomProjection(n_components=target_dim).fit_transform(vector)
        except Exception as e:
            raise embedding_exceptions.VectorProjectionError(message=f"GaussianrandomVectorProjection failed vector projection: {e}")
        