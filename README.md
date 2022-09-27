# jsonparse: ctrl-f for json
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jsonparse)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/ctomkow/jsonparse?label=version&sort=semver)
[![jsonparse](https://github.com/ctomkow/jsonparse/actions/workflows/jsonparse-buildtest.yml/badge.svg)](https://github.com/ctomkow/jsonparse/actions/workflows/jsonparse-buildtest.yml)
[![codecov](https://codecov.io/gh/ctomkow/jsonparse/branch/master/graph/badge.svg?token=affX7FZaFk)](https://codecov.io/gh/ctomkow/jsonparse)

</br>

> **jsonparse** is a simple JSON parsing library. Extract what's needed from key:value pairs.

## Install
```bash
pip install jsonparse
```

## Usage
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
                "chain": "B",
                "rope": 7,
                "string": 0.7,
                "cable": True
            }
    	}
    }
]


parser.find_key(data, 'chain')
['A', 'B']

parser.find_key(data, 'key')
[1, 2, {'chain': 'A', 'rope': 5, 'string': 1.2, 'cable': False}, {'chain': 'B', 'rope': 7, 'string': 0.7, 'cable': True}]


parser.find_keys(data, ['rope', 'cable'])
[[5, False], [7, True]]

parser.find_keys(data, ['rope', 'cable'], group=False)
[5, False, 7, True]


parser.find_key_chain(data, ['my', 'key', 'chain'])
['A']

parser.find_key_chain(data, ['key'])
[1, 2]

parser.find_key_chain(data, ['*', 'key', 'chain'])
['A', 'B']

parser.find_key_chain(data, ['*', 'key', '*'])
['A', 5, 1.2, False, 'B', 7, 0.7, True]


parser.find_key_value(data, 'cable', False)
[{'chain': 'A', 'rope': 5, 'string': 1.2, 'cable': False}]

parser.find_key_value(data, 'chain', 'B')
[{'chain': 'B', 'rope': 7, 'string': 0.7, 'cable': True}]
```
## API
`find_key(data: dict | list, key: str) -> list`
 
-  Provide JSON data as a dictionary or a list. The key to be found is a string.

-  Returns a list of values that match the corresponding key.

`find_keys(data: dict | list, keys: list, group: bool = True) -> list`

-  Provide JSON data as a dictionary or a list. The keys are a list of strings. The order of the keys does not matter.

-  Returns a two dimensional list of values matching the keys. The order of values is returned in the same order as the original data.

-  To return a one dimensional list, pass the keyword parameter group=False

`find_key_chain(data: dict | list, keys: list) -> list`

-  Provide JSON data as a dictionary or a list. The key chain is a list of keys that are all strings. The order of the keys **does** matter.

-  Returns a list of values that match the corresponding key chain. The order of values is returned in the same order as the original data.

  > Wildcard **'*'** can be used as key(s) to match any.

`find_key_value(data: dict | list, key: str, value: str | int | float | bool | None) -> list`

-  Provide JSON data as a dictionary or a list. The key is a string. The value is a string, integer, float, boolean, or None.

-  Returns a list of dictionaries that contain the key:value pair.
