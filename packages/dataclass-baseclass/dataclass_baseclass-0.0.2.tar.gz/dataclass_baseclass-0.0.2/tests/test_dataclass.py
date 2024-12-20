# mypy: disable-error-code=call-arg

from pytest import mark, raises

from dataclasses import FrozenInstanceError
from typing import Protocol

from dataclass_baseclass import DataClass

from .conftest import DataClassTestFactory, ToStr


class P(Protocol):
    s: str

    def gimme_s(self) -> str:
        return self.s


def test_wrong_params() -> None:
    with raises(
        TypeError,
        match=r"dataclass\(\) got an unexpected keyword argument 'something'",
    ):

        class UnknownArg(
            DataClass, dataclass_params={"something": "whatever"}
        ):
            pass

    with raises(AssertionError, match=r"kw_only"):

        class KWOnly(DataClass, dataclass_params={"kw_only": False}):
            pass


def test_load_interface(dc_test_factory: DataClassTestFactory) -> None:
    dc, loader = dc_test_factory()

    with raises(
        ValueError,
        match=r"strict mode not supported",
    ):
        loader(strict=True)


@mark.parametrize("frozen", [False, True])
def test_dataclass_base(
    dc_test_factory: DataClassTestFactory, str_test_data: ToStr, frozen: bool
) -> None:
    dc, loader = dc_test_factory(frozen, (P,))

    e = loader()
    assert e.gimme_s() == "what"
    assert e.d.gimme_s() == e.d.s

    with raises(
        TypeError,
        match=r"__init__\(\) got an unexpected keyword argument 'unexpected_attr'",
    ):
        dc(i=1, unexpected_attr=True)

    data = str_test_data()
    e = dc(**data)
    assert e.gimme_s() == "what"
    assert type(e.c) is dict


def test_dataclass_mutable(dc_test_factory: DataClassTestFactory) -> None:
    _dc, loader = dc_test_factory(frozen=False)

    e = loader()

    e.i = 12


def test_dataclass_frozen(dc_test_factory: DataClassTestFactory) -> None:
    _dc, loader = dc_test_factory(frozen=True)

    e = loader()

    with raises(FrozenInstanceError, match=r"cannot assign to field"):
        e.i = 12
