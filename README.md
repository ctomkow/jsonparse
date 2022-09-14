# jsonparse
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jsonparse)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/ctomkow/jsonparse?label=version&sort=semver)
[![jsonparse](https://github.com/ctomkow/jsonparse/actions/workflows/jsonparse-buildtest.yml/badge.svg)](https://github.com/ctomkow/jsonparse/actions/workflows/jsonparse-buildtest.yml)
[![codecov](https://codecov.io/gh/ctomkow/jsonparse/branch/master/graph/badge.svg?token=affX7FZaFk)](https://codecov.io/gh/ctomkow/jsonparse)

</br>

> **jsonparse** is a simple JSON parsing library. Extract what's needed from key:value pairs.

### Install
```
pip install jsonparse
```

### Usage
```python
from jsonparse import Parser

parser = Parser(stack_trace=False, queue_trace=False)

data = [
    {"key": 1},
    {"key": 2},
    {"my": 
        {"key": 
            {
                "chain": "A",
                "rope": 5,
                "string": 1.2,
                "cable": False
            }
        }
    },
    {"your":
    	{"key":
    		{
                "chain": "B"
            }
    	}
    }
]


parser.find_key(data, 'chain')
['B', 'A']

parser.find_key(data, 'key')
[{'chain': 'B'}, {'chain': 'A', 'rope': 5, 'string': 1.2, 'cable': False}, 2, 1]


parser.find_key_chain(data, ['my', 'key', 'chain'])
['A']

parser.find_key_chain(data, ['key'])
[1, 2]

parser.find_key_chain(data, ['*', 'key', 'chain'])
['A', 'B']

parser.find_key_chain(data, ['*', 'key', '*'])
['A', 5, 1.2, False, 'B']


parser.find_key_value(data, 'cable', False)
[{'chain': 'A', 'rope': 5, 'string': 1.2, 'cable': False}]

parser.find_key_value(data, 'chain', 'B')
[{'chain': 'B'}]
```
### API
`find_key(data: dict | list, key: str) -> list`
 
- Provide JSON data as a dictionary or a list, as well as the key as a string
- Returns a list of values that match the corresponding key.

`find_key_chain(data: dict | list, keys: list) -> list`

- Provide JSON data as a dictionary or a list, as well as a list of keys as strings.
- Returns a list of values that match the corresponding key chain.

    > Wildcard **'*'** can be used as key(s) to match any.

`find_key_value(data: dict | list, key: str, value: str | int | float | bool) -> list`

- Provide JSON data as a dictionary or a list, a key as a string,
  and a value as a string, integer, float, or boolean.
- Returns a list of set(s) that contain the key:value pair.
