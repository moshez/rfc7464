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
            max_end = data.find(b'\x1e', begin + 1)
            if max_end == -1:
                max_end = len(data)
            end = data.find(b'\n', begin, max_end)
            if end == -1:
                if max_end == len(data):
                    self.buffer = data[begin:]
                    break
                end = max_end
            try:
                yield json.loads(data[begin + 1:end].decode('utf-8'))
            except ValueError:
                pass
            begin = end
