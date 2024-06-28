# jsonparse: ctrl-f for json
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jsonparse)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/ctomkow/jsonparse?label=version&sort=semver)
[![jsonparse](https://github.com/ctomkow/jsonparse/actions/workflows/jsonparse-buildtest.yml/badge.svg)](https://github.com/ctomkow/jsonparse/actions/workflows/jsonparse-buildtest.yml)
[![codecov](https://codecov.io/gh/ctomkow/jsonparse/branch/master/graph/badge.svg?token=affX7FZaFk)](https://codecov.io/gh/ctomkow/jsonparse)
![Static Badge](https://img.shields.io/badge/powered_by-mead-E79A3F?style=flat)


</br>

> **jsonparse** is a simple JSON parsing library. Extract what's needed from key:value pairs.

## What's New
 - A new function, [find_value](#find_value), has been added. This function will return all keys of the matched value. :grinning:
 - [CLI tool](#CLI-tool). Parse json text files or stdin via the command line :tada:

# Python Library

## Install
```bash
pip install jsonparse
```

## Quickstart
Here is a quick example of what jsonparse is able to do.

```python
from jsonparse import find_key, find_keys, find_key_chain, find_key_value, find_value

data = [{
    "key0":
    {
        "key1": "result",
        "key2":
        {
            "key1": "result1",
            "key3": {"key1": "result2"}
        }
    }
}]

find_key(data, 'key1')
['result2', 'result1', 'result']

find_key_chain(data, ['key0', 'key2', 'key3', 'key1'])
['result2']
```

:heavy_plus_sign: See additional documentation in the [API section](#API) below.


# CLI tool

## Install
```bash
pip install jsonparse
```

## Quickstart
Summary of cli commands. For complete information, `jp --help`

Note, `jsonparse` and `jp` are equivalent.

`jp key key1 --file text.json`

`jp keys key1 key2 key3 --file text.json`

`jp key-chain my '*' chain --file text.json`

`jp key-value key1 '"result"' --file text.json`

`echo '{"key1": {"key2": 5}}' | jp key key2`

`jp value null --file text.json`

`jp value 42 --file text.json`

`jp value '"strValue"' --file text.json`


# API

- [Parser class](#parser)
    - [find_key](#find_key)
    - [find_keys](#find_keys)
    - [find_key_chain](#find_key_chain)
    - [find_key_value](#find_key_value)
    - [find_value](#find_value)

The API examples using the following test data.

```python
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
```

---

### Parser
<pre>
<b>Parser(</b><i>stack_trace</i>: bool = False, <i>queue_trace</i>: bool = False<b>)</b>
</pre>

&nbsp;&nbsp;&nbsp;&nbsp;Optionally instantiate the `Parser` class with tracing to print out the underlying data structures.

```python
p = Parser(stack_trace=True, queue_trace=True)
```

---

### find_key
<pre>
<b>find_key(</b><i>data</i>: dict | list, <i>key</i>: str<b>)</b> -> list
</pre>

&nbsp;&nbsp;&nbsp;&nbsp;Will return all values of the matched key.

```python
p.find_key(data, 'chain')
['A', 'B']

p.find_key(data, 'key')
[1, 2, {'chain': 'A', 'rope': 5, 'string': 1.2, 'cable': False}, {'chain': 'B', 'rope': 7, 'string': 0.7, 'cable': True}]
```

---

### find_keys
<pre>
<b>find_keys(</b><i>data</i>: dict | list, <i>keys</i>: list, <i>group</i>: bool = True<b>)</b> -> list
</pre>

&nbsp;&nbsp;&nbsp;&nbsp;The default return value is a two dimensional list. `[ [], [], ...]`.

&nbsp;&nbsp;&nbsp;&nbsp;To return all values as a one dimensional list, set `group=False`.

&nbsp;&nbsp;&nbsp;&nbsp;The ordering of the keys does not matter.

```python
p.find_keys(data, ['rope', 'cable'])
[[5, False], [7, True]]

p.find_keys(data, ['rope', 'cable'], group=False)
[5, False, 7, True]
```

---

### find_key_chain
<pre>
<b>find_key_chain(</b><i>data</i>: dict | list, <i>keys</i>: list<b>)</b> -> list
</pre>

&nbsp;&nbsp;&nbsp;&nbsp;The key chain is an ordered list of keys. The chain needs to start at the root level of the nested data.

&nbsp;&nbsp;&nbsp;&nbsp;Wildcard `*` can be used as key(s) to match any.

```python
p.find_key_chain(data, ['my', 'key', 'chain'])
['A']

p.find_key_chain(data, ['key'])
[1, 2]

p.find_key_chain(data, ['*', 'key', 'chain'])
['A', 'B']

p.find_key_chain(data, ['*', 'key', '*'])
['A', 5, 1.2, False, 'B', 7, 0.7, True]
```

---

### find_key_value
<pre>
<b>find_key_value(</b><i>data</i>: dict | list, <i>key</i>: str, <i>value</i>: str | int | float | bool | None) -> list
</pre>

&nbsp;&nbsp;&nbsp;&nbsp;The returned list contains the dictionaries that contain the specified key:value pair.

```python
p.find_key_value(data, 'cable', False)
[{'chain': 'A', 'rope': 5, 'string': 1.2, 'cable': False}]

p.find_key_value(data, 'chain', 'B')
[{'chain': 'B', 'rope': 7, 'string': 0.7, 'cable': True}]
```

---

### find_value
<pre>
<b>find_value(</b><i>data</i>: dict | list, <i>value</i>: str | int | float | bool | None<b>)</b> -> list
</pre>

&nbsp;&nbsp;&nbsp;&nbsp;Will return all keys of the matched value.

```python
p.find_value(data, 'A')
['chain']

p.find_value(data, False)
['cable']
```

# Web API

## Documentation

Visit [the swagger API documentation](https://jsonparse.dev/v1/docs)

All endpoints are HTTP POST requests where you include the searchable JSON data in the request body.

### Brief Endpoint Overiew
```bash
POST /v1/key/{key}
POST /v1/keys?key=1&key=2&key=3&key=4...
POST /v1/keychain?key=1&key=2&key=3&key=4...
POST /v1/keyvalue?key=a&value=1
POST /v1/value/{value}
```

## Quickstart
Let's practice using the public, free-to-use-no-authentication, web API hosted in GCP Cloud Run.

We are POST'ing the JSON data with curl, requesting to search for the key, 'key1'. The found key values are returned as JSON.

```bash
curl -X POST "https://jsonparse.dev/v1/key/key1" \
-H 'Content-Type: application/json' \
-d '[{"key0":{"key1":"result","key2":{"key1":"result1","key3":{"key1":"result2"}}}}]'

["result2","result1","result"]
```

> OR (using python and requests library)

```python
import requests

data = [{
    "key0":
    {
        "key1": "result",
        "key2":
        {
            "key1": "result1",
            "key3": {"key1": "result2"}
        }
    }
}]

requests.post('https://jsonparse.dev/v1/key/key1', json=data).json()

['result2', 'result1', 'result']
```

## Self-Hosted
```bash
pip install "jsonparse[webapi]"

gunicorn -b 0.0.0.0:8000 jsonparse.webapi:app
```

> Alternatively, run the docker container

```bash
docker run -d ctomkow/jsonparse
```