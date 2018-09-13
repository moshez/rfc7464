# Copyright (c) AUTHORS
# See LICENSE for details.

from __future__ import unicode_literals

import json
import unittest

import rfc7464


class TestEmit(unittest.TestCase):

    def test_int(self):
        res = rfc7464.emit(1)
        self.assertEqual(res, b'\x1e1\n')

    def test_unicode(self):
        res = rfc7464.emit(u"hello")
        self.assertEqual(res, b'\x1e"hello"\n')

    def test_array(self):
        res = rfc7464.emit([1, 2, 3])
        self.assertEqual(res[0:1], b'\x1e')
        self.assertEqual(res[-1:], b'\n')
        sdarr = json.loads(res[1:-1].decode('utf-8'))
        self.assertEqual(sdarr, [1, 2, 3])

    def test_object(self):
        obj = {u'hello': 5, u'world': 6}
        res = rfc7464.emit(obj)
        self.assertEqual(res[0:1], b'\x1e')
        self.assertEqual(res[-1:], b'\n')
        sdobj = json.loads(res[1:-1].decode('utf-8'))
        self.assertEqual(obj, sdobj)


class TestParse(unittest.TestCase):

    def setUp(self):
        self.parser = rfc7464.Parser()

    def test_some_garbage(self):
        inp = b'1'
        lst = list(self.parser.receive(inp))
        self.assertEqual(lst, [])

    def test_simple_int(self):
        inp = b'\x1e' + b'1' + b'\n'
        lst = list(self.parser.receive(inp))
        self.assertEqual(lst, [1])

    def test_simple_str(self):
        inp = b'\x1e' + json.dumps(u"hello").encode('utf-8') + b'\n'
        lst = list(self.parser.receive(inp))
        self.assertEqual(lst, ["hello"])

    def test_arr_dict(self):
        inp = (b'\x1e' + json.dumps([1]).encode('utf-8') + b'\n' +
               b'\x1e' + json.dumps({u'hello': 5}).encode('utf-8') + b'\n')
        lst = list(self.parser.receive(inp))
        self.assertEqual(lst, [[1], {u'hello': 5}])

    def test_broken_str(self):
        dumped = json.dumps("hello").encode('utf-8')
        length = len(dumped) // 2
        part1, part2 = dumped[:length], dumped[length:]
        inp1 = b'\x1e' + part1
        inp2 = part2 + b'\n'
        lst = list(self.parser.receive(inp1))
        self.assertEqual(lst, [])
        lst = list(self.parser.receive(inp2))
        self.assertEqual(lst, [u"hello"])

    def test_bad_json(self):
        inp = b'\x1e' + json.dumps(u"hello").encode('utf-8')[:-1] + b'\n'
        lst = list(self.parser.receive(inp))
        self.assertEqual(lst, [])

    def test_bad_utf8(self):
        inp = b'\x1e' + b'\xd7\xa9\xd7\x9c\xd7\x95\xd7' + b'\n'
        lst = list(self.parser.receive(inp))
        self.assertEqual(lst, [])

    def test_good_recover(self):
        inp = b'\x1e' + json.dumps(u"hello").encode('utf-8')
        inp += b'\x1e' + json.dumps(u"goodbye").encode('utf-8') + b'\n'
        lst = list(self.parser.receive(inp))
        self.assertEqual(lst, [u"hello", u"goodbye"])

    def test_discard_recover(self):
        inp = b'\x1e' + json.dumps(10).encode('utf-8')
        inp += b'\x1e' + json.dumps(u"goodbye").encode('utf-8') + b'\n'
        lst = list(self.parser.receive(inp))
        self.assertEqual(lst, [u"goodbye"])

    def test_good_recover_in_parts(self):
        inp = b'\x1e' + json.dumps(u"hello").encode('utf-8')
        inp += b'\x1e' + json.dumps(u"goodbye").encode('utf-8') + b'\n'
        for i in range(1, len(inp) - 1):
            part1, part2 = inp[:i], inp[i:]
            lst = list(self.parser.receive(part1))
            lst.extend(self.parser.receive(part2))
            self.assertEqual(lst, [u"hello", u"goodbye"])
