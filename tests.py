import os

import pytest

from pyenv import Env


TEST_ENV_FILE_NAME = "test.env"


with open(TEST_ENV_FILE_NAME, "w+") as file:
    file.write("""
    integer=1234
    decimal=3.14159265359
    string=Hello world""")


env = Env(TEST_ENV_FILE_NAME)

