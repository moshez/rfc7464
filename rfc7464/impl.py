import json


def emit(thing):
    return b'\x1e' + json.dumps(thing).encode('utf-8') + b'\n'


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
            try:
                decoded = json.loads(data[begin + 1:end].decode('utf-8'))
            except ValueError:
                pass
            else:
                yield decoded
            begin = end + 1
