# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pamela-lib",
    packages=find_packages(include=["pamela"]),
    description="Pamela is a python library to simplify API usage in programs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MPL-2.0",
    version="0.1.3",
    author="zlElo",
    author_email="mail@zlelo.de",
    url="https://github.com/zlElo/Pamela",
    keywords=["api", "library", "api-wrapper", "simplify"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
