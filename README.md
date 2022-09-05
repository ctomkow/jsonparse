# jsonparse
A simple JSON key parsing library

### Install
```bash
pip install git+https://github.com/ctomkow/jsonparse.git
```

### Usage
```python
from jsonparse import Parser
import json

search    = Parse(stack_trace=True)
data = json.loads('[{"key":1}, {"key":2}, {"my":{"key":{"chain":"A"}}}]')

val = search.all_inst_of_key(data, 'key')
val = search.all_inst_of_key_chain(data, 'my', 'key', 'chain')
```
### Details
`all_inst_of_key()` is a depth-first search (stack-based) which returns all values of matching key:value pairs.
`all_inst_of_key_chain()` is a breadth-first search (queue-based) which returns all values of matching terminal key:value pairs where all previous keys in chain are found.
