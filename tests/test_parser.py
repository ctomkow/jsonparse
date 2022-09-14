# Craig Tomkow
#
# Tests only public methods

# local imports
from jsonparse.parser import Parser

# 3rd part imports
import pytest


class TestParser:

    @pytest.fixture
    def parser(self):

        return Parser(stack_trace=True, queue_trace=True)

    @pytest.fixture
    def complex_json(self):

        return [
            {
                "id": "0001",
                "type": "donut",
                "exists": True,
                "ppu": 0.55,
                "batters":
                    {
                        "batter":
                            [
                                {"id": "1001", "type": "Regular"},
                                {"id": "1002", "type": "Chocolate"},
                                {"id": "1003", "type": "Blueberry"},
                                {"id": "1004", "type": "Devil's Food"}
                            ]
                    },
                "topping":
                    [
                        {"id": "5001", "type": "None"},
                        {"id": "5002", "type": "Glazed"},
                        {"id": "5003", "type": "Sugar"},
                        {"id": "5004", "type": "Powdered Sugar"},
                        {"id": "5005", "type": "Chocolate with Sprinkles"},
                        {"id": "5006", "type": "Chocolate"},
                        {"id": "5007", "type": "Maple"}
                    ]
            },
            {
                "id": "0002",
                "type": "donut",
                "exists": False,
                "ppu": 42,
                "batters":
                    {
                        "batter":
                            [
                                {"id": "1001", "type": "Regular"}
                            ]
                    },
                "top_stuff":
                    [
                        {"id": "5001", "type": "None"},
                        {"id": "5002", "type": "Glazed"},
                        {"id": "5003", "type": "Sugar"},
                        {"id": "5004", "type": "Chocolate"},
                        {"id": "5005", "type": "Maple"}
                    ]
            },
            {
                "id": "0003",
                "type": "donut",
                "exists": True,
                "ppu": 7,
                "batters":
                    {
                        "batter":
                            [
                                {"id": "1001", "type": "Regular"},
                                {"id": "1002", "type": "Chocolate"}
                            ]
                    },
                "on_top_thing":
                    [
                        {"id": "5001", "type": "None"},
                        {"id": "5002", "type": "Glazed"},
                        {"id": "5003", "type": "Chocolate"},
                        {"id": "5004", "type": "Maple"}
                    ]
            }
        ]

    def test_key(self, parser, complex_json):

        result = parser.key(complex_json, "id")
        assert result == [
            '0003', '5004', '5003', '5002', '5001', '1002',
            '1001', '0002', '5005', '5004', '5003', '5002', '5001', '1001',
            '0001', '5007', '5006', '5005', '5004', '5003', '5002', '5001',
            '1004', '1003', '1002', '1001'
        ]

    def test_key_not_found(self, parser, complex_json):

        result = parser.key(complex_json, "key_not_in_data")
        assert result == []

    def test_key_empty_key(self, parser, complex_json):

        try:
            parser.key(
                complex_json,
                ""
            )
        except ValueError:
            assert True

    def test_key_not_str_key(self, parser, complex_json):

        try:
            parser.key(
                complex_json,
                5
            )
        except TypeError:
            assert True

    def test_key_not_list_or_dict_data(self, parser):

        try:
            parser.key(
                "string of data",
                "string"
            )
        except TypeError:
            assert True

    def test_key_chain(self, parser, complex_json):

        result = parser.key_chain(
            complex_json,
            [
                "batters",
                "batter",
                "type"
            ]
        )
        assert result == [
            'Regular', 'Chocolate', 'Blueberry', "Devil's Food",
            'Regular', 'Regular', 'Chocolate']

    def test_key_chain_empty_key(self, parser, complex_json):

        try:
            parser.key_chain(
                complex_json,
                [""]
            )
        except ValueError:
            assert True

    def test_key_chain_not_str_key(self, parser, complex_json):

        try:
            parser.key_chain(
                complex_json,
                [5]
            )
        except TypeError:
            assert True

    def test_key_chain_not_list_or_dict_data(self, parser):

        try:
            parser.key_chain(
                "string of data",
                [
                    "string",
                    "of",
                    "data"
                ]
            )
        except TypeError:
            assert True

    def test_key_chain_key_not_found(self, parser, complex_json):

        result = parser.key_chain(
                complex_json,
                ["key_not_in_data"]
            )
        assert result == []

    def test_key_chain_wildcard(self, parser, complex_json):

        result = parser.key_chain(
            complex_json,
            [
                "*",
                "id"
            ]
        )
        assert result == ["5001", "5002", "5003", "5004", "5005", "5006",
                          "5007", "5001", "5002", "5003", "5004", "5005",
                          "5001", "5002", "5003", "5004"]

    def test_key_value(self, parser, complex_json):

        result = parser.key_value(
            complex_json,
            "id",
            "1001"
        )

        assert result == [{'id': '1001', 'type': 'Regular'},
                          {'id': '1001', 'type': 'Regular'},
                          {'id': '1001', 'type': 'Regular'}]

    def test_key_value_not_found(self, parser, complex_json):

        result = parser.key_value(
            complex_json,
            "id",
            5.4
        )

        assert result == []
