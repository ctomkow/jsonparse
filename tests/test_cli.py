# Craig Tomkow
#
# Tests only public methods


# local imports
from jsonparse import cli

# python imports
import os

# 3rd part imports
import pytest


class TestCli:

    # set working dir to tests directory to read from json file
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    @pytest.fixture
    def version(self):

        return '0.14.1'

    def test_flags_key(self):

        parser = cli._flags('v0.0.1-test')
        args = parser.parse_args(['key', 'ppu', '--file', 'tests.json'])
        args = cli._parse_input(args)

        assert True

    def test_flags_keys(self):

        parser = cli._flags('v0.0.1-test')
        args = parser.parse_args(['keys', 'ppu', '--file', 'tests.json'])
        args = cli._parse_input(args)

        assert True

    def test_flags_keychain(self):

        parser = cli._flags('v0.0.1-test')
        args = parser.parse_args(['key-chain', 'ppu', '--file', 'tests.json'])
        args = cli._parse_input(args)

        assert True

    def test_flags_keyvalue(self):

        parser = cli._flags('v0.0.1-test')
        args = parser.parse_args(['key-value', 'ppu', '0.55', '--file', 'tests.json'])
        args = cli._parse_input(args)

        assert True

    def test_flags_keyvalue_invalid_json_input(self):

        parser = cli._flags('v0.0.1-test')
        args = parser.parse_args(['key-value', 'exists', 'False', '--file', 'tests.json'])

        with pytest.raises(SystemExit):
            args = cli._parse_input(args)


    def test_flags_value(self):

        parser = cli._flags('v0.0.1-test')
        args = parser.parse_args(['value', '42', '--file', 'tests.json'])
        args = cli._parse_input(args)

        assert True
