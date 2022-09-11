# jsonparse
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jsonparse)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/ctomkow/jsonparse?label=version&sort=semver)
[![jsonparse](https://github.com/ctomkow/jsonparse/actions/workflows/jsonparse.yml/badge.svg)](https://github.com/ctomkow/jsonparse/actions/workflows/jsonparse.yml)
[![codecov](https://codecov.io/gh/ctomkow/jsonparse/branch/master/graph/badge.svg?token=affX7FZaFk)](https://codecov.io/gh/ctomkow/jsonparse)

</br>

> **jsonparse** is a simple JSON parsing library. Extract the values from key:value pairs providing the key(s).

### Install
```
pip install jsonparse
```

### Usage
```python
from jsonparse import Parser

parse = Parser(stack_trace=False, queue_trace=False)
data = [
    {"key": 1},
    {"key": 2},
    {"my": 
        {"key": 
            {"chain":"A"}
        }
    },
    {"your":
    	{"key":
    		{"chain":"B"}
    	}
    }
]


print(parse.key(data, 'key'))
[{'chain': 'B'}, {'chain': 'A'}, 2, 1]

print(parse.key(data, 'chain'))
['B', 'A']

print(parse.key_chain(data, ['my', 'key', 'chain']))
['A']

print(parse.key_chain(data, ['key']))
[1, 2]

print(parse.key_chain(data, ['*', 'key', 'chain']))
['A', 'B']

print(parse.key_chain(data, ['*', 'key', '*']))
['A', 'B']
```
### API
`key(data: dict | list, key: str): -> list`

- Provide JSON data as a dictionary or a list, as well as the key as a string
- Returns a list of values that match the corresponding key.

`key_chain(data: dict | list, keys: list): -> list`

- Provide JSON data as a dictionary or a list, as well as a list of keys as strings.
- Returns a list of values that match the corresponding key chain.

> Wildcard **'*'** can be used as key(s) to match any.
