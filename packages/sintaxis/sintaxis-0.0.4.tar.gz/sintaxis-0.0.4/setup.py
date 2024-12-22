from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = "0.0.4"
DESCRIPTION = "Sintaxis es un comando line interface (CLI) que permite crear y testear ejercicios de programación."
PACKAGE_NAME = "sintaxis"
AUTHOR = "Paolo Soncco"
EMAIL = "paolosonccodev@gmail.com"
GITHUB = "https://github.com/12aptor"

setup(
    name=PACKAGE_NAME,
    packages=[PACKAGE_NAME],
    version=VERSION,
    license="Apache License 2.0",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=GITHUB,
    keywords=[],
    install_requires=[
        "colorama",
        "python-socketio[asyncio_client]"
    ],
    entry_points={
        "console_scripts": [
            "sintaxis=sintaxis.main:main",
        ],
    },
)
