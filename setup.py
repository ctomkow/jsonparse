# local imports
import jsonparse

# python imports
from setuptools import setup, find_namespace_packages
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
DESCRIPTION = 'Search through JSON data key:values'
URL = url = 'https://github.com/ctomkow/jsonparse'
EMAIL = 'ctomkow@gmail.com'
AUTHOR = 'Craig Tomkow'
REQUIRES_PYTHON = '>=3.6.0'

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
        classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
        ],
        extras_require={
          'webapi': [
                        'flask==2.0.3',
                        'gunicorn==20.1.0',
                        'werkzeug==2.0.0',
                    ]
        },
        entry_points={
            'console_scripts': [
                'jsonparse=jsonparse.cli:entrypoint',
                'jp=jsonparse.cli:entrypoint',
            ],
        },
        packages=find_namespace_packages(include=["jsonparse"]),
        package_dir={"jsonparse": "jsonparse"},
        package_data={
            'jsonparse': ['VERSION'],
            'jsonparse.static.css': ['*.css'],
            'jsonparse.static.img': ['*.png'],
            'jsonparse.static.js': ['*.js'],
            'jsonparse.static': ['openapi.yaml'],
            'jsonparse.templates': ['*.html'],
        },
)
