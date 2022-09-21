# Craig Tomkow
# 2022-09-18
#
# Web api. Decorated functions that call the Parser methods

# local imports
from .parser import Parser

# python imports
import json

# 3rd party imports
from flask import Flask, request, jsonify


app = Flask(__name__)

# TODO: Accept URL as an alternative to JSON in the body of the POST
#       It might not be a POST then...
#       THE URL could be a parameter, e.g.
#       ?url=http://mypublicapi.com/data


# accept a singular key
# /v1/key/mykey
@app.post('/v1/key/<path:key>')  # use path as key might have a slash
def _find_key(key: str):
    print(key)
    try:
        values = Parser().find_key(request.json, key)
    except TypeError:
        return (jsonify(error="key must be a string"), 400)
    except ValueError:
        return (jsonify(error="key cannot be empty"), 400)
    return values


# query parameters of keys
# /v1/keys?key=first&key=second&key=third
@app.post('/v1/keys')
def _find_keys():

    keys = request.args.getlist('key')
    if not keys:
        return (jsonify(error="parameter key incorrect"), 400)

    try:
        values = Parser().find_keys(request.json, keys)
    except TypeError:
        return (jsonify(error="key must be a string"), 400)
    except ValueError:
        return (jsonify(error="key cannot be empty"), 400)
    return values


# query parameters of keys
# /v1/keychain?key=first&key=second&key=third
@app.post('/v1/keychain')
def _find_key_chain():

    key_chain = request.args.getlist('key')
    if not key_chain:
        return (jsonify(error="parameter key incorrect"), 400)

    try:
        values = Parser().find_key_chain(request.json, key_chain)
    except TypeError:
        return (jsonify(error="key must be a string"), 400)
    except ValueError:
        return (jsonify(error="key cannot be empty"), 400)
    return values


# query parameters for key and value
# /v1/keyvalue?key=mykey&value="myvalue"
@app.post('/v1/keyvalue')
def _find_key_value():

    key = request.args.get('key')
    value = request.args.get('value')

    if not key or not value:
        return (jsonify(error="key or value parameter missing"), 400)

    try:
        value = json.loads(value)
    except json.JSONDecodeError:
        return (jsonify(error="value must be valid json"), 400)

    try:
        values = Parser().find_key_value(request.json, key, value)
    except TypeError:
        return (jsonify(error="key must be a string"), 400)
    except ValueError:
        return (jsonify(error="key cannot be empty"), 400)
    return values
