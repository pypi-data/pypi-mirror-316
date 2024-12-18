from __future__ import annotations

from collections.abc import Callable
from typing import Any, Generic, TypeVar, final

import jax.numpy as jnp
import pytest
from numpy.random import Generator
from tjax import JaxComplexArray, NumpyComplexArray, Shape
from typing_extensions import override

from efax import ExpectationParametrization, NaturalParametrization, Structure, SubDistributionInfo

NP = TypeVar('NP', bound=NaturalParametrization[Any, Any])
EP = TypeVar('EP', bound=ExpectationParametrization[Any])
Domain = TypeVar('Domain', bound=NumpyComplexArray | dict[str, Any])


class DistributionInfo(Generic[NP, EP, Domain]):
    def __init__(self, dimensions: int = 1) -> None:
        super().__init__()
        self.dimensions = dimensions

    def exp_to_scipy_distribution(self, p: EP) -> Any:
        """Produce a corresponding scipy distribution from expectation parameters.

        Args:
            p: Expectation parameters.
        """
        return self.nat_to_scipy_distribution(p.to_nat())

    def nat_to_scipy_distribution(self, q: NP) -> Any:
        """Produce a corresponding scipy distribution from natural parameters.

        Args:
            q: Natural parameters.
        """
        return self.exp_to_scipy_distribution(q.to_exp())

    @final
    def exp_parameter_generator(self, rng: Generator, shape: Shape) -> EP:
        """Generate expectation parameters.

        Defaults to converting values generated by nat_parameter_generator.
        """
        return self.nat_parameter_generator(rng, shape).to_exp()

    @final
    def nat_parameter_generator(self, rng: Generator, shape: Shape) -> NP:
        """Generate natural parameters."""
        return self.nat_structure().generate_random(rng, shape)

    def scipy_to_exp_family_observation(self, x: Domain) -> JaxComplexArray | dict[str, Any]:
        """The observation that's expected by the exponential family.

        Args:
            x: The observation that's produced by the scipy distribution.
        """
        return jnp.asarray(x)

    def exp_structure(self) -> Structure[EP]:
        return Structure([SubDistributionInfo((), self.exp_class(), self.dimensions, [])])

    def nat_structure(self) -> Structure[NP]:
        return Structure([SubDistributionInfo((), self.nat_class(), self.dimensions, [])])

    def exp_class(self) -> type[EP]:
        raise NotImplementedError

    def nat_class(self) -> type[NP]:
        raise NotImplementedError

    @classmethod
    def name(cls) -> str:
        return cls.__name__.removesuffix('Info')

    @classmethod
    def tests_selected(cls, distribution_name: str | None) -> bool:
        return distribution_name is None or cls.name() == distribution_name

    @classmethod
    def skip_if_deselected(cls, distribution_name: str | None) -> None:
        if not cls.tests_selected(distribution_name):
            pytest.skip(f"Deselected {cls.name()}")

    @override
    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        if (cls.exp_to_scipy_distribution is DistributionInfo.exp_to_scipy_distribution
                and cls.nat_to_scipy_distribution is DistributionInfo.nat_to_scipy_distribution):
            raise TypeError

        for method in ('exp_parameter_generator', 'nat_parameter_generator',
                       'scipy_to_exp_family_observation'):
            old_method = getattr(cls, method)

            def new_method(*args: Any,
                           old_method: Callable[..., Any] = old_method,
                           **kwargs: Any) -> Any:
                return old_method(*args, **kwargs)

            setattr(cls, method, new_method)
