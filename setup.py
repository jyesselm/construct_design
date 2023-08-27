#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()


with open("README.md", "r", encoding="UTF-8") as f:
    readme = f.read()

with open("requirements.txt", "r", encoding="UTF-8") as f:
    requirements = f.read().splitlines()

setup(
    name="construct_design",
    version="0.1.0",
    description="Collecting a set of common tools I use often for construct design of RNA",
    long_description=readme,
    long_description_content_type="test/markdown",
    author="Joe Yesselman",
    author_email="jyesselm@unl.edu",
    url="https://github.com/jyesselm/construct_design",
    packages=[
        "construct_design",
    ],
    package_dir={"construct_design": "construct_design"},
    py_modules=[
        "construct_design/finalize_libraries",
        "construct_design/formatting",
        "construct_design/logging",
        "construct_design/processing",
        "construct_design/rld",
        "construct_design/rnamake",
    ],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords="construct_design",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points={"console_scripts": []},
)
