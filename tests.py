import uuid
from decimal import Decimal

import pytest

from pyenv import Env


STRING = """
integer=1234
decimal=3.14159265359
double_quote_string="Hello world"
single_quote_string='Hello world'
dictionary={"foo": 1234, "bar": "test", "spam": 3.14159265359}
list=[1, 2, 3, 4, 5]
tuple=(1, 2, 3, 4 , 5)
set={1, 2, 3, 4, 5}
uuid=6ba7b810-9dad-11d1-80b4-00c04fd430c8
custom_type=foooooo
"""


class Foo:
    def __init__(self, value):
        self.value = value


env = Env.parse(STRING, extra_value_converters={"(foo+)": lambda value: Foo(value)})


def test_basic_types():
    assert env["integer"] == 1234

    assert env["decimal"] == Decimal("3.14159265359")

    assert env["double_quote_string"] == "Hello world"
    assert env["single_quote_string"] == "Hello world"

    assert isinstance(env["dictionary"], dict)
    assert env["dictionary"]["foo"] == 1234
    assert env["dictionary"]["bar"] == "test"
    assert env["dictionary"]["spam"] == Decimal("3.14159265359")


def test_iterables():
    assert env["list"] == [1, 2, 3, 4, 5]

    assert env["tuple"] == (1, 2, 3, 4, 5)

    assert env["set"] == {1, 2, 3, 4, 5}

    assert env["uuid"] == uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")


def test_custom_types():
    assert isinstance(env["custom_type"], Foo)
    assert env["custom_type"].value.count("o") == 6
