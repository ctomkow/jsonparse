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
                "topping":
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
                "topping":
                    [
                        {"id": "5001", "type": "None"},
                        {"id": "5002", "type": "Glazed"},
                        {"id": "5003", "type": "Chocolate"},
                        {"id": "5004", "type": "Maple"}
                    ]
            }
        ]

    # all_inst_of_key
    def test_key(self, parser, complex_json):

        result = parser.key(complex_json, "id")
        assert result == [
            '0003', '5004', '5003', '5002', '5001', '1002',
            '1001', '0002', '5005', '5004', '5003', '5002', '5001', '1001',
            '0001', '5007', '5006', '5005', '5004', '5003', '5002', '5001',
            '1004', '1003', '1002', '1001'
        ]

    # all_inst_of_key_chain
    def test_key_chain(self, parser, complex_json):

        result = parser.key_chain(
            complex_json,
            "batters",
            "batter",
            "type"
        )
        assert result == [
            'Regular', 'Chocolate', 'Blueberry', "Devil's Food",
            'Regular', 'Regular', 'Chocolate']
