#!/usr/bin/env python
# Craig Tomkow
# 2022-09-18
#
# Web api. Decorated functions that call the Parser methods

# local imports
from .parser import Parser

# python imports
import json

# 3rd party imports
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)


@app.route('/')
def get_root():
    return render_template('index.html')


@app.route('/v1/docs')
def get_docs():
    return render_template('swaggerui.html')


# accept a singular key
# /v1/key/mykey
@app.post('/v1/key/<path:key>')
def _find_key(key: str):

    if not key:
        return (jsonify(error="key must not be empty"), 400)

    return jsonify(Parser().find_key(request.json, key))


# query parameters of keys
# /v1/keys?key=first&key=second&key=third&group=False
@app.post('/v1/keys')
def _find_keys():

    # validate parameter keys
    param_keys = request.args.keys()
    if not param_keys:
        return (jsonify(error="parameter key incorrect"), 400)
    for k in param_keys:
        if (k != 'key') and (k != 'group'):
            return (jsonify(error="parameter key incorrect"), 400)

    keys = request.args.getlist('key')
    for key in keys:
        if not isinstance(key, str):
            return (jsonify(error="key must be a string"), 400)
        elif not key:
            return (jsonify(error="key must not be empty"), 400)

    group = request.args.get('group')
    if not group:
        group_status = True
    elif group.lower() == 'false':
        group_status = False
    else:
        group_status = True

    return jsonify(Parser().find_keys(request.json, keys, group_status))


# query parameters of keys
# /v1/keychain?key=first&key=second&key=third
@app.post('/v1/keychain')
def _find_key_chain():

    # validate parameter keys
    param_keys = request.args.keys()
    for k in param_keys:
        if k != 'key':
            return (jsonify(error="parameter key incorrect"), 400)

    key_chain = request.args.getlist('key')
    for key in key_chain:
        if not isinstance(key, str):
            return (jsonify(error="key must be a string"), 400)
        elif not key:
            return (jsonify(error="key must not be empty"), 400)

    return jsonify(Parser().find_key_chain(request.json, key_chain))


# query parameters for key and value
# /v1/keyvalue?key=mykey&value="myvalue"
@app.post('/v1/keyvalue')
def _find_key_value():

    # validate parameter keys
    param_keys = request.args.keys()
    for k in param_keys:
        if k != 'key' and k != 'value':
            return (jsonify(error="parameter key incorrect"), 400)

    key = request.args.get('key')
    value = request.args.get('value')
    if not isinstance(key, str):
        return (jsonify(error="key must be a string"), 400)
    elif not key:
        return (jsonify(error="key must not be empty"), 400)
    elif not value:
        return (jsonify(error="value must not be empty"), 400)
    try:
        value = json.loads(value)
    except json.JSONDecodeError:
        return (jsonify(error="value must be valid json"), 400)

    return jsonify(Parser().find_key_value(request.json, key, value))


# accept a singular value
# /v1/value/myvalue
@app.post('/v1/value/<path:value>')
def _find_value(value: str):

    if not value:
        return jsonify(error="value must not be empty"), 400
    try:
        value = json.loads(value)
    except json.JSONDecodeError:
        return jsonify(error="value must be valid json"), 400

    return jsonify(Parser().find_value(request.json, value))
