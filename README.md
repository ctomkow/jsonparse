# json-search
A simple JSON key search library

### Install
```bash
pip install git+https://github.com/ctomkow/json-search.git
```

### Usage
```python
from jsons.jsons import JsonSearch

search = JsonSearch(stack_trace=True)
val = search.all_inst_of_key(json_data, 'key')
val = search.all_inst_of_key_chain(json_data, 'my', 'key', 'chain')
```
### Details
`all_inst_of_key()` is a depth-first search (stack-based) which returns all values of matching key:value pairs.
`all_inst_of_key_chain()` is a breadth-first search (queue-based) which returns all values of matching terminal key:value pairs where all previous keys in chain are found.
