# Craig Tomkow
# 2022-09-18
#
# Web api. Decorators that wrap the Parser methods

# local imports
from .parser import Parser

# python imports
import json

# 3rd party imports
from flask import Flask, request


app = Flask(__name__)

# TODO: Accept URL as an alternative to JSON in the body of the POST
#       It might not be a POST then...
#       THE URL could be a parameter, e.g.
#       ?url=http://mypublicapi.com/data


# accept a singular key
@app.post('/v1/key/<path:key>')  # use path as key might have a slash
def _find_key(key: str):

    # TODO: try except clause
    values = Parser().find_key(request.json, key)
    return values


# accept a comma delimited list of keys
@app.post('/v1/keys/<path:keys>')
def _find_keys(keys: str):

    # TODO: validation
    keys_list = keys.split(',')

    # TODO: try except clause
    values = Parser().find_keys(request.json, keys_list)
    return values


# accept comma delimited list of keys
@app.post('/v1/keychain/<path:key_chain>')
def _find_key_chain(key_chain: str):

    # TODO: validation
    key_chain_list = key_chain.split(',')

    # TODO: try except clause
    values = Parser().find_key_chain(request.json, key_chain_list)
    return values


# TODO: currently the value specificed has to be valid json, gotta think about
#       what is best to accept for the value type...
# accept comma delimited key value pair
@app.post('/v1/keyvalue/<path:key_value>')
def _find_key_value(key_value: str):

    # TODO: validation
    key = key_value.split(',')[0]
    value = key_value.split(',')[1]

    # TODO: try except clause
    values = Parser().find_key_value(request.json, key, json.loads(value))
    return values
