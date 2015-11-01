import json
import unittest

import rfc7464


class TestEmit(unittest.TestCase):

    def test_int(self):
        res = rfc7464.emit(1)
        self.assertEquals(res, b'\x1e1\n')

    def test_unicode(self):
        res = rfc7464.emit(u"hello")
        self.assertEquals(res, b'\x1e"hello"\n')

    def test_array(self):
        res = rfc7464.emit([1, 2, 3])
        self.assertEquals(res[0], b'\x1e')
        self.assertEquals(res[-1], b'\n')
        sdarr = json.loads(res[1:-1])
        self.assertEquals(sdarr, [1, 2, 3])

    def test_object(self):
        obj = {u'hello': 5, u'world': 6}
        res = rfc7464.emit(obj)
        self.assertEquals(res[0], b'\x1e')
        self.assertEquals(res[-1], b'\n')
        sdobj = json.loads(res[1:-1])
        self.assertEquals(obj, sdobj)
