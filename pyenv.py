import os
import re
import uuid

from pathlib import Path
from decimal import Decimal


ENV_PARSE_REGEX = "(.+)=(.+)"


VALUE_CONVERTERS = {
    r"(true|false)": bool,
    r"(^\d+$)": int,
    r"(\d*\.\d*)": lambda value: Decimal(str(value)),
    r"(\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)": uuid.UUID,
    r"\[(.*)\]": lambda value: list(_convert_iterable(value)),
    r"\((.*)\)": lambda value: tuple(_convert_iterable(value)),
    r"\{(\D+\s*:\s*.+)\}": lambda value: _convert_dictionary(value),
    r"\{(.*)\}": lambda value: set(_convert_iterable(value)),
    '"(.*)"': str,
    "'(.*)'": str
}


def _convert_iterable(items):
    items = re.sub("\s*,\s*", ",", items)

    for item in items.split(","):
        yield _convert_value(item)


def _convert_dictionary(string):
    dictionary = {}
    string = re.sub("\s*,\s*", ",", string)
    string = re.sub("\s*:\s*", ":", string)

    for item in string.split(","):
        key, value = item.split(":")

        key = _convert_value(key)
        dictionary[key] = _convert_value(value)

    return dictionary


def _convert_value(string, value_converters=VALUE_CONVERTERS):
    for regex, converter in value_converters.items():

        if match := re.match(regex, string, flags=re.IGNORECASE):
            return converter(match.group(1))

    else:
        raise ValueError(f"Invalid value. {string}")


class Env:
    def __init__(self, path=os.path.join(os.getcwd(), ".env"), extra_value_converters=None):
        if extra_value_converters is None:
            extra_value_converters = {}

        if isinstance(path, Path):
            self.path = path
        elif isinstance(path, str):
            self.path = Path(path)
        else:
            raise ValueError(f"Expected pathlib.Path object or string. Got {type(path).__name__}")

        if not self.path.exists():
            raise ValueError("Given path does not exist")

        self.value_converters = VALUE_CONVERTERS | extra_value_converters
        self.raw_values = re.findall(ENV_PARSE_REGEX, self.path.read_text())

        converted_values = {}

        for name, value in self.raw_values:
            converted_values[name] = _convert_value(value, self.value_converters)

        self._values = converted_values

    @classmethod
    def parse(cls, string, extra_value_converters={}):
        """Method for parsing a string manually"""
        raw_values = re.findall(ENV_PARSE_REGEX, string)
        value_converters = VALUE_CONVERTERS | extra_value_converters

        converted_values = {}

        for name, value in raw_values:
            converted_values[name] = _convert_value(value, value_converters)

        env = cls.__new__(cls)
        env.value_converters = value_converters
        env.raw_values = raw_values
        env._values = converted_values
        env.path = None
        return env

    @property
    def values(self):
        return self._values

    def __getitem__(self, item):
        return self.values[item]

    def __setitem__(self, key, value):
        self.values[key] = value
        with self.path.open("a") as file:
            file.write(f"{key}={value}")
