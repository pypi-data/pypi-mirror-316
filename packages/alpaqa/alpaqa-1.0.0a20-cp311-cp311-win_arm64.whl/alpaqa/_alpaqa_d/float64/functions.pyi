"""
(Proximal) functions and operators.
"""
from __future__ import annotations
import numpy
import typing
__all__ = ['L1Norm', 'L1NormElementwise', 'NuclearNorm']
M = typing.TypeVar("M", bound=int)
N = typing.TypeVar("N", bound=int)
class L1Norm:
    """
    C++ documentation :cpp:class:`alpaqa::functions::L1Norm`
    ℓ₁-norm regularizer (with a single scalar regularization factor).
    
    .. seealso:: :py:func:`alpaqa.prox`
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, λ: float = 1) -> None:
        ...
    @property
    def λ(self) -> float:
        """
        Regularization factor.
        """
class L1NormElementwise:
    """
    C++ documentation :cpp:class:`alpaqa::functions::L1NormElementwise`
    ℓ₁-norm regularizer (with element-wise regularization factors).
    
    .. seealso:: :py:func:`alpaqa.prox`
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, λ: numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    @property
    def λ(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Regularization factors.
        """
class NuclearNorm:
    """
    C++ documentation :cpp:class:`alpaqa::functions::NuclearNorm`
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, λ: float) -> None:
        ...
    @typing.overload
    def __init__(self, λ: float, rows: int, cols: int) -> None:
        ...
    @property
    def U(self) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]:
        """
        Left singular vectors.
        """
    @property
    def V(self) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]:
        """
        Right singular vectors.
        """
    @property
    def singular_values(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Vector of singular values of the last output of the prox method.
        
        .. seealso:: :py:func:`alpaqa.prox`
        """
    @property
    def singular_values_input(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Vector of singular values of the last input of the prox method.
        """
    @property
    def λ(self) -> float:
        """
        Regularization factor.
        """
