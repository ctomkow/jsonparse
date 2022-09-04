# local imports
import jsons

# python imports
from setuptools import setup
import os

# read from the VERSION file
with open(os.path.join(os.path.dirname(jsons.__file__), 'VERSION')) as version_file:
    version = version_file.read().strip()

# Package meta-data.
NAME = 'jsons'
DESCRIPTION = 'Search through JSON data for what you need'
URL = url='https://github.com/ctomkow/jsons'
EMAIL = 'ctomkow@gmail.com'
AUTHOR = 'Craig Tomkow'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = version

setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        url=URL,
        author=AUTHOR,
        author_email=EMAIL,
        license='MIT',
        packages=['jsons'],
    )
