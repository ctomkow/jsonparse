# Craig Tomkow
#
# Test the webapi endpoints

# local imports
from jsonparse import webapi

# 3rd part imports
import pytest


@pytest.fixture
def complex_json():

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
                    {"id": "5001", "type": "None"},
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
                    {"id": "5001", "type": "None"},
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


@pytest.fixture()
def app():

    app = webapi.app
    app.config.update({"TESTING": True})

    # other setup can go here
    yield app
    # clean up / reset resources here


@pytest.fixture()
def client(app):

    return app.test_client()


def test_key(client, complex_json):

    response = client.post("/v1/key/id", json=complex_json)
    breakpoint()
    assert response.json == [
            '1001', '1002', '1003', '1004', '5001',
            '5002', '5003', '5004', '5005', '5006', '5007', '0001',
            '1001', '5001', '5002', '5003', '5004', '5005', '0002',
            '1001', '1002', '5001', '5002', '5003', '5004', '0003']
