
from .parser import Parser

from typing import Union


def find_key(data, key):
    # type: (Union[dict, list], str) -> list
    """
    Search JSON data that consists of key:value pairs for all instances of provided key. The data can have complex
    nested dictionaries and lists. If duplicate keys exist in the data (at any layer) all matching key values will
    be returned. Data is parsed using a depth first search with a stack.

    Keyword arguments:

    data -- The python object representing JSON data with key:value pairs. This could be a dictionary or a list.

    key  -- The key that will be searched for in the JSON data. The key must be a string.
    """
    return Parser().find_key(data, key)


def find_keys(data, keys, group=True):
    # type: (Union[dict, list], list, bool) -> list
    """
    Search JSON data that consists of key:value pairs for all instances of provided keys. The data can have complex
    nested dictionaries and lists. If duplicate keys exist in the data (at any layer) all matching key values will
    be returned. Each instance of matching keys within a dictionary will be returned as a list. The final return
    value is a two dimensional list. If a one dimensional list is needed where matched key values of the same
    dictionaries are not returned as a list, pass the group=False keyword parameter.

    Keyword arguments:

    data -- The python object representing JSON data with key:value pairs. This could be a dictionary or a list.

    keys  -- The keys that will be searched for in the JSON data. The keys argument is a list of dictionary keys.

    group -- Determines whether the found values of the same dictionary will be returned as a list or not.
             Default is True which results in a two dimensional list. Pass False to return a one dimensional list.
    """
    return Parser().find_keys(data, keys, group=group)


def find_key_chain(data, keys):
    # type: (Union[dict, list], list) -> list
    """
    Search JSON data that consists of key:value pairs for the first instance of provided key chain. The data can
    have complex nested dictionaries and lists. If duplicate key chains exist in the data, all key chain values will
    be returned. The data is parsed using breadth first search using a queue.

    Keyword arguments:

    data -- The python object representing JSON data with key:value pairs. This could be a dictionary or a list.

    keys -- A list of keys that will be searched for in the JSON data. The first key will be depth 1,
            second key depth 2, and so on. The ordering of the keys matter. The keys must be strings within a list.
            A wildcard '*' key(s) can be used to match any.
    """
    return Parser().find_key_chain(data, keys)


def find_key_value(data, key, value):
    # type: (Union[dict, list], str, Union[str, int, float, bool, None]) -> list
    """
    Search JSON data that consists of key:value pairs for all instances of provided key and value pair.
    The parent set that contains the key:value pair will be returned. The data can have complex nested
    dictionaries and lists. If duplicate key and value pairs exist in the data (at any layer),
    all matching key and value pair set(s) that contain the key:value pair will be returned. Data is parsed
    using a depth first search with a stack.

    Keyword arguments:

    data -- The python object representing JSON data with key:value pairs. This could be a dictionary or a list.

    key  -- The key that will be searched for in the JSON data. The key must be a string.

    value -- The value that will be searched for in the JSON data. The value must be a string, integer, float, or boolean.
    """
    return Parser().find_key_value(data, key, value)


def find_value(data, value):
    # type: (Union[dict, list], Union[str, int, float, bool, None]) -> list
    """
    Search JSON data that consists of key:value pairs for all instances of provided value, returning the associated key (opposite of find_key).
    The data can have complex nested dictionaries and lists. If duplicate values exist in the data (at any layer),
    all associated keys will be returned. Data is parsed using a depth first search with a stack.

    Keyword arguments:

    data -- The python object representing JSON data with key:value pairs. This could be a dictionary or a list.

    value  -- The value that will be searched for in the JSON data. Must be a valid JSON value.
    """
    return Parser().find_value(data, value)
