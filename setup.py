import setuptools
import pathlib

# The text of the README file
README = pathlib.Path("./Readme.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="pyenv",
    version="0.1.0",
    description="A module to parse values from text files",
    long_description=README,
    py_modules=["pyenv"],
    long_description_content_type="text/markdown",
    url="https://github.com/Rashaad1268/PyEnv",
    author="Rashaad",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
    install_requires=[],
)