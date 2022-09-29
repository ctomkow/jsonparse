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

## Quickstart
Here is a quick example of what jsonparse is able to do.

```python
from jsonparse import Parser

p = Parser()

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

p.find_key(data, 'key1')
['result2', 'result1', 'result']

p.find_key_chain(data, ['key0', 'key2', 'key3', 'key1'])
['result2']
```

## API

- [Parser class](#parser)
    - [find_key](#find_key)
    - [find_keys](#find_keys)
    - [find_key_chain](#find_key_chain)
    - [find_key_value](#find_key_value)

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

<!--
# Web API
If you want to use a jsonparse web API, currently you can host it yourself.

## Install + Run
```bash
pip install "jsonparse[webapi]"

gunicorn -b 0.0.0.0:8000 jsonparse.webapi:app
```

> Alternatively, run the docker container

```bash
docker run -d ctomkow/jsonparse
```


## Quickstart
The following quickstart section assumes you are running the web API locally on your machine (127.0.0.1). If the address of where
the web API is hosted is different (e.g. docker container or external server), change the IP accordingly.

```bash
curl -X POST "http://127.0.0.1:8000/v1/key/key1" \
-H 'Content-Type: application/json' \
-d '[{"key0":{"key1":"result","key2":{"key1":"result1","key3":{"key1":"result2"}}}}]'

["result2","result1","result"]
```

> OR

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

requests.post('http://127.0.0.1:8000/v1/key/key1', json=data).json()

['result2', 'result1', 'result']
```

## Web API Endpoints

Visit https://api.jsonparse.dev to view the swagger API documentation
-->