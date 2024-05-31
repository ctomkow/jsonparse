
from .parser import Parser

from typing import Union


def find_key(data: Union[dict, list], key: str) -> list:

    return Parser().find_key(data, key)


def find_keys(data: Union[dict, list], keys: list, group: bool = True) -> list:

    return Parser().find_keys(data, keys, group=group)


def find_key_chain(data: Union[dict, list], keys: list) -> list:

    return Parser().find_key_chain(data, keys)


def find_key_value(data: Union[dict, list], key: str, value: Union[str, int, float, bool, None]) -> list:

    return Parser().find_key_value(data, key, value)


def find_value(data: Union[dict, list], value: Union[str, int, float, bool, None]) -> list:

    return Parser().find_value(data, value)
