# jsonparse
A simple JSON key parsing library. It's use-case is to extract the values from key:value pairs in JSON data.

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
    }
]


print(parse.key(data, 'key'))
[{'chain': 'A'}, 2, 1]

print(parse.key_chain(data, ['my', 'key', 'chain']))
['A']

print(parse.key_chain(data, ['key']))
[1, 2]
```
### API
`key(data: dict | list, key: str): -> list`

Returns a list of values that have the corresponding key.

`key_chain(data: dict | list, keys: list): -> list`

Returns a list of values that have the corresponding key chain.
