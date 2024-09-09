# Craig Tomkow
#
# Tests only public methods

# local imports
from jsonparse.parser import Parser
from collections import OrderedDict

# 3rd part imports
import pytest


class TestParser:

    @pytest.fixture
    def parser(self):

        return Parser(stack_trace=False, queue_trace=False)

    @pytest.fixture
    def complex_json27(self):

        return [
            OrderedDict([
                ("id", "0001"),
                ("type", "donut"),
                ("exists", True),
                ("ppu", 0.55),
                ("batters", OrderedDict([
                    ("batter", [
                        OrderedDict([("id", "1001"), ("type", "Reg")]),
                        OrderedDict([("id", "1002"), ("type", "Chocolate")]),
                        OrderedDict([("id", "1003"), ("type", "Blueberry")]),
                        OrderedDict([("id", "1004"), ("type", "Devil's Food")]),
                        OrderedDict([("start", 5), ("end", 8)])
                    ])
                ])),
                ("topping", [
                    OrderedDict([("id", "5001"), ("ty", "None")]),
                    OrderedDict([("id", "5002"), ("type", "Glazed")]),
                    OrderedDict([("id", "5003"), ("type", "Sugar")]),
                    OrderedDict([("id", "5004"), ("type", "Powdered Sugar")]),
                    OrderedDict([("id", "5005"), ("type", "Chocolate with Sprinkles")]),
                    OrderedDict([("id", "5006"), ("type", "Chocolate")]),
                    OrderedDict([("id", "5007"), ("type", "Maple")])
                ]),
                ("start", 22),
                ("end", 99)
            ]),
            OrderedDict([
                ("id", "0002"),
                ("type", "donut"),
                ("exists", False),
                ("ppu", 42),
                ("batters", OrderedDict([
                    ("batter", [
                        OrderedDict([("id", "1001"), ("type", "Rul")])
                    ])
                ])),
                ("top_stuff", [
                    OrderedDict([("id", "5001"), ("typ", "None")]),
                    OrderedDict([("id", "5002"), ("type", "Glazed")]),
                    OrderedDict([("id", "5003"), ("type", "Sugar")]),
                    OrderedDict([("id", "5004"), ("type", "Chocolate")]),
                    OrderedDict([("id", "5005"), ("type", "Maple")])
                ]),
                ("start", 1),
                ("end", 9)
            ]),
            OrderedDict([
                ("id", "0003"),
                ("type", "donut"),
                ("exists", None),
                ("ppu", 7),
                ("batters", OrderedDict([
                    ("batter", [
                        OrderedDict([("id", "1001"), ("type", "Lar")]),
                        OrderedDict([("id", "1002"), ("type", "Chocolate")])
                    ])
                ])),
                ("on_top_thing", [
                    OrderedDict([("id", "5001"), ("type", "None")]),
                    OrderedDict([("id", "5002"), ("type", "Glazed")]),
                    OrderedDict([("id", "5003"), ("type", "Chocolate")]),
                    OrderedDict([("id", "5004"), ("type", "Maple")])
                ]),
                ("start", 4),
                ("end", 7)
            ])
        ]

    def test_find_key27(self, parser, complex_json27):

        result = parser.find_key(complex_json27, "id")

        assert result == [
            '1001', '1002', '1003', '1004', '5001',
            '5002', '5003', '5004', '5005', '5006', '5007', '0001',
            '1001', '5001', '5002', '5003', '5004', '5005', '0002',
            '1001', '1002', '5001', '5002', '5003', '5004', '0003']

    def test_find_key_not_found27(self, parser, complex_json27):

        result = parser.find_key(complex_json27, "key_not_in_data")
        assert result == []

    def test_find_key_empty_key27(self, parser, complex_json27):

        try:
            parser.find_key(
                complex_json27,
                ""
            )
        except ValueError:
            assert True

    def test_find_key_not_str_key27(self, parser, complex_json27):

        try:
            parser.find_key(
                complex_json27,
                5
            )
        except TypeError:
            assert True

    def test_find_key_not_list_or_dict_data(self, parser):

        try:
            parser.find_key(
                "string of data",
                "string"
            )
        except TypeError:
            assert True

    def test_find_key_chain27(self, parser, complex_json27):

        result = parser.find_key_chain(
            complex_json27,
            [
                "batters",
                "batter",
                "type"
            ]
        )
        assert result == [
            'Reg', 'Chocolate', 'Blueberry', "Devil's Food",
            'Rul', 'Lar', 'Chocolate']

    def test_find_key_chain_empty_key27(self, parser, complex_json27):

        try:
            parser.find_key_chain(
                complex_json27,
                [""]
            )
        except ValueError:
            assert True

    def test_find_key_chain_not_str_key27(self, parser, complex_json27):

        try:
            parser.find_key_chain(
                complex_json27,
                [5]
            )
        except TypeError:
            assert True

    def test_find_key_chain_not_list_or_dict_data(self, parser):

        try:
            parser.find_key_chain(
                "string of data",
                [
                    "string",
                    "of",
                    "data"
                ]
            )
        except TypeError:
            assert True

    def test_find_key_chain_key_not_found27(self, parser, complex_json27):

        result = parser.find_key_chain(
                complex_json27,
                ["key_not_in_data"]
            )
        assert result == []

    def test_find_key_chain_wildcard27(self, parser, complex_json27):

        result = parser.find_key_chain(
            complex_json27,
            [
                "*",
                "id"
            ]
        )
        assert result == ["5001", "5002", "5003", "5004", "5005", "5006",
                          "5007", "5001", "5002", "5003", "5004", "5005",
                          "5001", "5002", "5003", "5004"]

    def test_find_key_value27(self, parser, complex_json27):

        result = parser.find_key_value(
            complex_json27,
            "id",
            "1001"
        )

        assert result == [
            {'id': '1001', 'type': 'Reg'},
            {'id': '1001', 'type': 'Rul'},
            {'id': '1001', 'type': 'Lar'}]

    def test_find_key_value_not_found27(self, parser, complex_json27):

        result = parser.find_key_value(
            complex_json27,
            "id",
            5.4
        )

        assert result == []

    def test_find_key_value_none27(self, parser, complex_json27):

        result = parser.find_key_value(
            complex_json27,
            "exists",
            None
        )

        assert result == [{
                "id": "0003",
                "type": "donut",
                "exists": None,
                "ppu": 7,
                "batters":
                {
                    "batter":
                    [
                        {"id": "1001", "type": "Lar"},
                        {"id": "1002", "type": "Chocolate"}
                    ]
                },
                "on_top_thing":
                [
                    {"id": "5001", "type": "None"},
                    {"id": "5002", "type": "Glazed"},
                    {"id": "5003", "type": "Chocolate"},
                    {"id": "5004", "type": "Maple"}
                ],
                "start": 4,
                "end": 7
            }]

    def test_find_keys27(self, parser, complex_json27):

        result = parser.find_keys(complex_json27, ['start', 'end'])

        assert result == [[5, 8], [22, 99], [1, 9], [4, 7]]

    def test_find_keys_no_group27(self, parser, complex_json27):

        result = parser.find_keys(complex_json27, ['start', 'end'], group=False)

        assert result == [5, 8, 22, 99, 1, 9, 4, 7]

    def test_find_keys_not_found27(self, parser, complex_json27):

        result = parser.find_keys(complex_json27, ['key_does_not_exist', 'neither_does_this_one'])

        assert result == []

    def test_find_keys_one_not_found27(self, parser, complex_json27):

        result = parser.find_keys(complex_json27, ['exists', 'key_does_not_exist', 'ppu'])

        assert result == [[True, 0.55], [False, 42], [None, 7]]

    def test_find_value27(self, parser, complex_json27):

        result = parser.find_value(complex_json27, 42)
        assert result == ['ppu']

    def test_find_value_not_found27(self, parser, complex_json27):

        result = parser.find_value(complex_json27, 0.0001)
        assert result == []

    def test_find_value_multiple27(self, parser, complex_json27):

        result = parser.find_value(complex_json27, 'None')
        assert result == ['ty', 'typ', 'type']
