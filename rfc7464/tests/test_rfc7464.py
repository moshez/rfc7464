# Copyright (c) AUTHORS
# See LICENSE for details.

from __future__ import unicode_literals

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
        self.assertEquals(res[0:1], b'\x1e')
        self.assertEquals(res[-1:], b'\n')
        sdarr = json.loads(res[1:-1].decode('utf-8'))
        self.assertEquals(sdarr, [1, 2, 3])

    def test_object(self):
        obj = {u'hello': 5, u'world': 6}
        res = rfc7464.emit(obj)
        self.assertEquals(res[0:1], b'\x1e')
        self.assertEquals(res[-1:], b'\n')
        sdobj = json.loads(res[1:-1].decode('utf-8'))
        self.assertEquals(obj, sdobj)


class TestParse(unittest.TestCase):

    def setUp(self):
        self.parser = rfc7464.Parser()

    def test_some_garbage(self):
        inp = b'1'
        l = list(self.parser.receive(inp))
        self.assertEquals(l, [])

    def test_simple_int(self):
        inp = b'\x1e' + b'1' + b'\n'
        l = list(self.parser.receive(inp))
        self.assertEquals(l, [1])

    def test_simple_str(self):
        inp = b'\x1e' + json.dumps(u"hello").encode('utf-8') + b'\n'
        l = list(self.parser.receive(inp))
        self.assertEquals(l, ["hello"])

    def test_arr_dict(self):
        inp = (b'\x1e' + json.dumps([1]).encode('utf-8') + b'\n' +
               b'\x1e' + json.dumps({u'hello': 5}).encode('utf-8') + b'\n')
        l = list(self.parser.receive(inp))
        self.assertEquals(l, [[1], {u'hello': 5}])

    def test_broken_str(self):
        dumped = json.dumps("hello").encode('utf-8')
        length = len(dumped) // 2
        part1, part2 = dumped[:length], dumped[length:]
        inp1 = b'\x1e' + part1
        inp2 = part2 + b'\n'
        l = list(self.parser.receive(inp1))
        self.assertEquals(l, [])
        l = list(self.parser.receive(inp2))
        self.assertEquals(l, [u"hello"])

    def test_bad_json(self):
        inp = b'\x1e' + json.dumps(u"hello").encode('utf-8')[:-1] + b'\n'
        l = list(self.parser.receive(inp))
        self.assertEquals(l, [])

    def test_bad_utf8(self):
        inp = b'\x1e' + b'\xd7\xa9\xd7\x9c\xd7\x95\xd7' + b'\n'
        l = list(self.parser.receive(inp))
        self.assertEquals(l, [])

    def test_good_recover(self):
        inp = b'\x1e' + json.dumps(u"hello").encode('utf-8')
        inp += b'\x1e' + json.dumps(u"goodbye").encode('utf-8') + b'\n'
        l = list(self.parser.receive(inp))
        self.assertEquals(l, [u"hello", u"goodbye"])

    def test_discard_recover(self):
        inp = b'\x1e' + json.dumps(10).encode('utf-8')
        inp += b'\x1e' + json.dumps(u"goodbye").encode('utf-8') + b'\n'
        l = list(self.parser.receive(inp))
        self.assertEquals(l, [u"goodbye"])

    def test_good_recover_in_parts(self):
        inp = b'\x1e' + json.dumps(u"hello").encode('utf-8')
        inp += b'\x1e' + json.dumps(u"goodbye").encode('utf-8') + b'\n'
        for i in range(1, len(inp) - 1):
            part1, part2 = inp[:i], inp[i:]
            l = list(self.parser.receive(part1))
            l.extend(self.parser.receive(part2))
            self.assertEquals(l, [u"hello", u"goodbye"])
