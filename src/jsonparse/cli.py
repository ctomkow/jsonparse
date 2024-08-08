#!/usr/bin/env python3
# Craig Tomkow
# 2022-10-03

# behold, the future!
from __future__ import print_function

# local imports
from .parser import Parser
from .version import __version__

# python imports
from typing import Any
import sys
import argparse
import io
import os
import json


def entrypoint():

    version = __version__
    parser = _flags(version)
    args = parser.parse_args()
    _parse_input(args)


def _flags(version):
    # type: (str) -> argparse.ArgumentParser
    parser = argparse.ArgumentParser(
        prog='jsonparse',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Parse deeply nested json based on key(s) and value(s)

examples
--------
jsonparse key-chain my key chain --file test.json
jsonparse key-chain my '*' chain --file test.json

jsonparse key-value mykey 42 --file test.json
jsonparse key-value mykey '"strValue"' --file test.json

echo '{"mykey": 42}' | jsonparse key mykey

jp value null --file test.json
jp value 42 --file test.json
jp value '"strValue"' --file test.json
""")

    # all flags here
    parser.add_argument('-v', '--version', action='version', version="%(prog)s"+version)

    sub_parser = parser.add_subparsers()

    key = sub_parser.add_parser('key', description='With no FILE, read standard input.')
    key.add_argument('KEY', action='store', type=str, nargs=1, help='search for key')
    key.add_argument('--file', type=argparse.FileType('r'), nargs='?', default=sys.stdin, help="json file as input")

    keys = sub_parser.add_parser('keys', description='With no FILE, read standard input.')
    keys.add_argument('--ungroup', action='store_false', help='return a one dimensional list')
    keys.add_argument('KEYS', metavar='KEY', action='store', type=str, nargs='+', help='search for keys')
    keys.add_argument('--file', type=argparse.FileType('r'), nargs='?', default=sys.stdin, help="json file as input")

    key_chain = sub_parser.add_parser('key-chain', description='With no FILE, read standard input.')
    key_chain.add_argument('KEYCHAIN', metavar='KEY', action='store', type=str, nargs='+', help='search for key chain')
    key_chain.add_argument('--file', type=argparse.FileType('r'), nargs='?', default=sys.stdin,
                           help="json file as input")

    key_value = sub_parser.add_parser('key-value', description='With no FILE, read standard input.')
    key_value.add_argument('KVKEY', metavar='KEY', action='store', type=str, nargs=1, help='search key part of key:value')
    key_value.add_argument('KVVALUE', metavar='VALUE', action='store', type=str, nargs=1,
                           help='must be valid json. String must have escaped double quotes. e.g. \'"asdf"\'')
    key_value.add_argument('--file', type=argparse.FileType('r'), nargs='?', default=sys.stdin,
                           help="json file as input")

    value = sub_parser.add_parser('value', description='With no FILE, read standard input.')
    value.add_argument('VALUE', action='store', type=str, nargs=1, help='Search for value. Must be a valid JSON value. If searching for a string value, ensure it is quoted. Returns all keys with that value')
    value.add_argument('--file', type=argparse.FileType('r'), nargs='?', default=sys.stdin, help="json file as input")

    return parser


def _parse_input(args):
    # type: (argparse.ArgumentParser) -> None
    try:
        data = _pythonify(_input(args.file))
    except ValueError:
        print('input json not valid.')
        raise SystemExit(0)

    if 'KEY' in args:
        _print(_jsonify(Parser().find_key(data, args.KEY[0])))
    elif 'KEYS' in args:
        _print(_jsonify(Parser().find_keys(data, args.KEYS, group=args.ungroup)))
    elif 'KEYCHAIN' in args:
        _print(_jsonify(Parser().find_key_chain(data, args.KEYCHAIN)))
    elif ('KVKEY' in args) and ('KVVALUE' in args):
        try:
            value = _pythonify(args.KVVALUE[0])
        except ValueError:
            print('value is not valid json. example valid types: \'"value"\', 5, false, true, null')
            raise SystemExit(0)
        _print(_jsonify(Parser().find_key_value(data, args.KVKEY[0], value)))
    elif 'VALUE' in args:
        try:
            value = _pythonify(args.VALUE[0])
        except ValueError:
            print('value is not valid json. example valid types: \'"value"\', 5, false, true, null')
            raise SystemExit(0)
        _print(_jsonify(Parser().find_value(data, value)))


def _input(fp):
    # type: (io.TextIOWrapper) -> str
    data = ''
    for line in fp:
        data += line.rstrip()
    return data


def _pythonify(data):
    # type: (json) -> Any
    try:
        return json.loads(data)
    except ValueError:
        raise


def _jsonify(data):
    # type: (Any) -> json
    return json.dumps(data)


def _print(data):
    # type: (str) -> None
    for elem in json.loads(data):
        print(_jsonify(elem))


if __name__ == "__main__":

    entrypoint()
