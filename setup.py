# local imports
import jsonparse

# python imports
from setuptools import setup
import os
from codecs import open

# read from the VERSION file
with open(os.path.join(
          os.path.dirname(jsonparse.__file__), 'VERSION')) as version_file:
    version = version_file.read().strip()

# long description as readme
with open("README.md", "r", "utf-8") as f:
    readme = f.read()

# Package meta-data.
NAME = 'jsonparse'
DESCRIPTION = 'Search through JSON data key:values by key(s)'
URL = url = 'https://github.com/ctomkow/jsonparse'
EMAIL = 'ctomkow@gmail.com'
AUTHOR = 'Craig Tomkow'
REQUIRES_PYTHON = '>=3.7.0'

setup(
        name=NAME,
        version=version,
        description=DESCRIPTION,
        long_description=readme,
        long_description_content_type="text/markdown",
        url=URL,
        author=AUTHOR,
        author_email=EMAIL,
        license='MIT',
        packages=['jsonparse'],
        classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
        ],
)
