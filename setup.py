# python imports
from setuptools import setup, find_packages
from codecs import open

# read from the VERSION file
with open('src/jsonparse/VERSION') as version_file:
    version = version_file.read().strip()

# long description as readme
with open("README.md", "r", "utf-8") as f:
    readme = f.read()

# Package meta-data.
NAME = 'jsonparse'
DESCRIPTION = 'Search through JSON data key:values'
URL = url = 'https://github.com/ctomkow/jsonparse'
EMAIL = 'ctomkow@gmail.com'
AUTHOR = 'Craig Abt Tomkow'
REQUIRES_PYTHON = ">=2.7,!=3.0,!=3.1,!=3.2,!=3.3,!=3.4,!=3.5"

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
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13',
        ],
        extras_require={
          'webapi': [
                'flask==2.0.3',
                'gunicorn==20.1.0',
                'werkzeug==2.0.0',
            ],
        },
        entry_points={
            'console_scripts': [
                'jsonparse=jsonparse.cli:entrypoint',
                'jp=jsonparse.cli:entrypoint',
            ],
        },
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        package_data={
            'jsonparse': ['VERSION'],
            'jsonparse.static.css': ['*.css'],
            'jsonparse.static.img': ['*.png'],
            'jsonparse.static.js': ['*.js'],
            'jsonparse.static': ['openapi.yaml'],
            'jsonparse.templates': ['*.html'],
        },
)