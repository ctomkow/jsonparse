#!/usr/bin/env python3
# Craig Tomkow
# 2022-10-03

# python imports
import sys
import argparse
import io


class Cli:

    def __init__(self):

        args = self.parse_args('1.0.0')
        self._input(args.FILE)

    def parse_args(self, version: str) -> argparse.Namespace:

        parser = argparse.ArgumentParser(
            prog='jsonparse',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="""\
Parse deeply nested json based on key(s) and value(s).

With no FILE, read standard input.""")
        # all flags here
        parser.add_argument(
            'FILE', type=argparse.FileType('r'), nargs='?',
            default=sys.stdin, help="json file to read as input")
        parser.add_argument(
            '-v', '--version', action='version', version=f"%(prog)s {version}")
        group = parser.add_mutually_exclusive_group()
        # TODO: decide if I want --key AND --keys or just --key x --key y --key z
        # TODO: also, how to do, --keys asdf fdsa zzzz
        group.add_argument(
            '--key', action='store', metavar='KEY', type=str,
            help="search for KEY")
        group.add_argument(
            '--keys', action='append', metavar='KEYS', type=str,
            help="search for KEYS")
        group.add_argument(
            '--key-chain', action='append', metavar='KEY-CHAIN', type=str,
            help="search for ordered KEY-CHAIN")
        group.add_argument(
            '--key-value', action='append', metavar='KEY-VALUE', type=str,
            help="search for KEY:VALUE pair returning the containing set")
        return parser.parse_args()

    def _input(self, fp: io.TextIOWrapper):

        for line in fp:
            print(line.rstrip())


if __name__ == "__main__":

    Cli()
