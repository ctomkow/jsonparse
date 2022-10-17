#!/usr/bin/env python3
# Craig Tomkow
# 2022-10-03

# local imports
from typing import Any
from parser import Parser

# python imports
import sys
import argparse
import io
import os
import json


class Cli:

    def __init__(self):

        # read from the VERSION file
        with open(os.path.join(
                os.path.dirname(__file__), 'VERSION')) as version_file:
            version = version_file.read().strip()

        args = self.parse_args(version)
        data = self._pythonify(self._input(args.FILE))

        if 'KEY' in args:
            print(self._jsonify(Parser().find_key(data, args.KEY[0])))
        elif 'KEYS' in args:
            print(self._jsonify(Parser().find_keys(data, args.KEYS, group=args.ungroup)))
        elif 'KEYCHAIN' in args:
            print(self._jsonify(Parser().find_key_chain(data, args.KEYCHAIN)))
        elif ('KVKEY' in args) and ('KVVALUE' in args):
            print(args)
            try:
                value = self._pythonify(args.KVVALUE[0])
            except json.decoder.JSONDecodeError:
                print('value is not valid json. example valid types: \\"value\\", 5, false, true, null')
                raise SystemExit(0)
            print(self._jsonify(Parser().find_key_value(data, args.KVKEY[0], value)))

    def parse_args(self, version: str) -> argparse.Namespace:

        parser = argparse.ArgumentParser(
            prog='jsonparse',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description='Parse deeply nested json based on key(s) and value(s)')

        # all flags here
        parser.add_argument(
            '-v', '--version', action='version', version=f"%(prog)s {version}")

        sub_parser = parser.add_subparsers()

        key = sub_parser.add_parser('key', description='With no FILE, read standard input.')
        key.add_argument('KEY', action='store', type=str, nargs=1, help='search for key')
        key.add_argument(
            'FILE', type=argparse.FileType('r'), nargs='?',
            default=sys.stdin, help="json file or stdin to read as input")

        # TODO: how to read from FILE when you specify variable number of keys? ...
        keys = sub_parser.add_parser('keys', description='With no FILE, read standard input.')
        keys.add_argument('--ungroup', action='store_false', help='return a one dimensional list')
        keys.add_argument('KEYS', metavar='KEY', action='store', type=str, nargs='+', help='search for keys')
        keys.add_argument(
            'FILE', type=argparse.FileType('r'), nargs='?',
            default=sys.stdin, help="json file or stdin to read as input")

        # TODO: how to read from FILE when you specify variable number of keys? ...
        key_chain = sub_parser.add_parser('key-chain', description='With no FILE, read standard input.')
        key_chain.add_argument('KEYCHAIN', metavar='KEY', action='store', type=str, nargs='+', help='search for key chain')
        key_chain.add_argument(
            'FILE', type=argparse.FileType('r'), nargs='?',
            default=sys.stdin, help="json file or stdin to read as input")

        key_chain = sub_parser.add_parser('key-value', description='With no FILE, read standard input.')
        key_chain.add_argument('KVKEY', metavar='KEY', action='store', type=str, nargs=1,
                               help='search for key part of key:value')
        key_chain.add_argument('KVVALUE', metavar='VALUE', action='store', type=str, nargs=1,
                               help='must be valid json. For a string, must have escaped double quotes. e.g. \\"asdf\\"')
        key_chain.add_argument(
            'FILE', type=argparse.FileType('r'), nargs='?',
            default=sys.stdin, help="json file or stdin to read as input")

        return parser.parse_args()

    def _input(self, fp: io.TextIOWrapper) -> str:

        data = ''
        for line in fp:
            data += line.rstrip()
        return data

    def _pythonify(self, data: json) -> Any:

        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            raise

    def _jsonify(self, data: Any) -> json:

        return json.dumps(data)


if __name__ == "__main__":

    Cli()
