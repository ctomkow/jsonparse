# Craig Tomkow
#
# Test the webapi endpoints

# local imports
from jsonparse import webapi

# 3rd part imports
import pytest


@pytest.fixture
def data():

    return [{"a": "A"}]


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


def test_key(client, data):

    response = client.post("/v1/key/id", json=data)
    assert response.status_code == 200


def test_key_no_key(client, data):

    response = client.post("/v1/key/", json=data)
    assert response.status_code == 404


def test_keys(client, data):

    response = client.post("/v1/keys?key=exists&key=ppu", json=data)
    assert response.status_code == 200


def test_keys_with_group(client, data):

    response = client.post(
        "/v1/keys?key=exists&key=ppu&group=False",
        json=data)
    assert response.status_code == 200


def test_keys_empty_param_key(client, data):

    response = client.post("/v1/keys?key=", json=data)
    assert response.status_code == 400


def test_keys_bad_params_key(client, data):

    response = client.post("/v1/keys?key=a&notkey=b&key=c", json=data)
    assert response.status_code == 400


def test_keys_no_params(client, data):

    response = client.post("/v1/keys?", json=data)
    assert response.status_code == 400


def test_keychain(client, data):

    response = client.post("/v1/keychain?key=a&key=b", json=data)
    assert response.status_code == 200


def test_keychain_empty_param_key(client, data):

    response = client.post("/v1/keychain?key=", json=data)
    assert response.status_code == 400


def test_keychain_bad_params_key(client, data):

    response = client.post("/v1/keychain?key=a&notkey=b&key=c", json=data)
    assert response.status_code == 400


def test_keyvalue(client, data):

    response = client.post('/v1/keyvalue?key=a&value="A"', json=data)
    assert response.status_code == 200


def test_keyvalue_empty_param_key(client, data):

    response = client.post('/v1/keyvalue?key=&value="B"', json=data)
    assert response.status_code == 400


def test_keyvalue_bad_params_key(client, data):

    response = client.post('/v1/keyvalue?key=a&notvalue="B"', json=data)
    assert response.status_code == 400


def test_keyvalue_bad_json_value(client, data):

    response = client.post('/v1/keyvalue?key=a&value=A', json=data)
    assert response.status_code == 400


def test_value(client, data):

    response = client.post('/v1/value/42', json=data)
    assert response.status_code == 200


def test_value_valid_json_str_value(client, data):

    response = client.post('/v1/value/"a"', json=data)
    assert response.status_code == 200


def test_value_no_value(client, data):

    response = client.post('/v1/value/', json=data)
    assert response.status_code == 404


def test_value_bad_json_value(client, data):

    response = client.post('/v1/value/A', json=data)
    assert response.status_code == 400
