
from parser import Parser


def find_key(data, key):

    return Parser(data, key).find_key(key).data


# todo: add rest of functions