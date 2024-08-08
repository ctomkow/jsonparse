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
                                {"id": "1001", "type": "Reg"},
                                {"id": "1002", "type": "Chocolate"},
                                {"id": "1003", "type": "Blueberry"},
                                {"id": "1004", "type": "Devil's Food"},
                                {"start": 5, "end": 8}
                            ]
                    },
                "topping":
                    [
                        {"id": "5001", "ty": "None"},
                        {"id": "5002", "type": "Glazed"},
                        {"id": "5003", "type": "Sugar"},
                        {"id": "5004", "type": "Powdered Sugar"},
                        {"id": "5005", "type": "Chocolate with Sprinkles"},
                        {"id": "5006", "type": "Chocolate"},
                        {"id": "5007", "type": "Maple"}
                    ],
                "start": 22,
                "end": 99
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
                                {"id": "1001", "type": "Rul"}
                            ]
                    },
                "top_stuff":
                    [
                        {"id": "5001", "typ": "None"},
                        {"id": "5002", "type": "Glazed"},
                        {"id": "5003", "type": "Sugar"},
                        {"id": "5004", "type": "Chocolate"},
                        {"id": "5005", "type": "Maple"}
                    ],
                "start": 1,
                "end": 9
            },
            {
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
            }
        ]

    def test_find_key(self, parser, complex_json):

        result = parser.find_key(complex_json, "id")

        assert result == [
            '1001', '1002', '1003', '1004', '5001',
            '5002', '5003', '5004', '5005', '5006', '5007', '0001',
            '1001', '5001', '5002', '5003', '5004', '5005', '0002',
            '1001', '1002', '5001', '5002', '5003', '5004', '0003']

    def test_find_key_not_found(self, parser, complex_json):

        result = parser.find_key(complex_json, "key_not_in_data")
        assert result == []

    def test_find_key_empty_key(self, parser, complex_json):

        try:
            parser.find_key(
                complex_json,
                ""
            )
        except ValueError:
            assert True

    def test_find_key_not_str_key(self, parser, complex_json):

        try:
            parser.find_key(
                complex_json,
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

    def test_find_key_chain(self, parser, complex_json):

        result = parser.find_key_chain(
            complex_json,
            [
                "batters",
                "batter",
                "type"
            ]
        )
        assert result == [
            'Reg', 'Chocolate', 'Blueberry', "Devil's Food",
            'Rul', 'Lar', 'Chocolate']

    def test_find_key_chain_empty_key(self, parser, complex_json):

        try:
            parser.find_key_chain(
                complex_json,
                [""]
            )
        except ValueError:
            assert True

    def test_find_key_chain_not_str_key(self, parser, complex_json):

        try:
            parser.find_key_chain(
                complex_json,
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

    def test_find_key_chain_key_not_found(self, parser, complex_json):

        result = parser.find_key_chain(
                complex_json,
                ["key_not_in_data"]
            )
        assert result == []

    def test_find_key_chain_wildcard(self, parser, complex_json):

        result = parser.find_key_chain(
            complex_json,
            [
                "*",
                "id"
            ]
        )
        assert result == ["5001", "5002", "5003", "5004", "5005", "5006",
                          "5007", "5001", "5002", "5003", "5004", "5005",
                          "5001", "5002", "5003", "5004"]

    def test_find_key_value(self, parser, complex_json):

        result = parser.find_key_value(
            complex_json,
            "id",
            "1001"
        )

        assert result == [
            {'id': '1001', 'type': 'Reg'},
            {'id': '1001', 'type': 'Rul'},
            {'id': '1001', 'type': 'Lar'}]

    def test_find_key_value_not_found(self, parser, complex_json):

        result = parser.find_key_value(
            complex_json,
            "id",
            5.4
        )

        assert result == []

    def test_find_key_value_none(self, parser, complex_json):

        result = parser.find_key_value(
            complex_json,
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

    def test_find_keys(self, parser, complex_json):

        result = parser.find_keys(
            complex_json,
            ['start', 'end']
        )

        assert result == [[5, 8], [22, 99], [1, 9], [4, 7]]

    def test_find_keys_no_group(self, parser, complex_json):

        result = parser.find_keys(
            complex_json,
            ['start', 'end'],
            group=False
        )

        assert result == [5, 8, 22, 99, 1, 9, 4, 7]

    def test_find_keys_not_found(self, parser, complex_json):

        result = parser.find_keys(
            complex_json,
            ['key_does_not_exist', 'neither_does_this_one']
        )

        assert result == []

    def test_find_keys_one_not_found(self, parser, complex_json):

        result = parser.find_keys(
            complex_json,
            ['exists', 'key_does_not_exist', 'ppu']
        )

        assert result == [[True, 0.55], [False, 42], [None, 7]]

    def test_find_value(self, parser, complex_json):

        result = parser.find_value(complex_json, 42)
        assert result == ['ppu']

    def test_find_value_not_found(self, parser, complex_json):

        result = parser.find_value(complex_json, 0.0001)
        assert result == []

    def test_find_value_multiple(self, parser, complex_json):

        result = parser.find_value(complex_json, 'None')
        assert result == ['ty', 'typ', 'type']
