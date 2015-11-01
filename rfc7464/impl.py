import json


def emit(thing):
    return '\x1e' + json.dumps(thing) + '\n'
