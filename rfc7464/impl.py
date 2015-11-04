import json

import automat

def emit(thing):
    return b'\x1e' + json.dumps(thing) + b'\n'


class Parser(object):

    buffer = b''

    def receive(self, data):
        begin = 0
        if self.buffer != b'':
            self.buffer, data = b'', self.buffer + data
        while begin < len(data):
            begin = data.find(b'\x1e', begin)
            if begin == -1:
                return
            end = data.find(b'\n', begin)
            if end == -1:
                self.buffer = data[begin:]
                break
            yield json.loads(data[begin + 1:end])
            begin = end + 1
