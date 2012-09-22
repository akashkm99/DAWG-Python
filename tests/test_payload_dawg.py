# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pytest
import dawg_python
from .utils import data_path

class TestBytesDAWG(object):

    DATA = (
        ('foo', b'data1'),
        ('bar', b'data2'),
        ('foo', b'data3'),
        ('foobar', b'data4')
    )

    def dawg(self):
        return dawg_python.BytesDAWG().load(data_path("small", "bytes.dawg"))

    def test_contains(self):
        d = self.dawg()
        for key, val in self.DATA:
            assert key in d

        assert 'food' not in d
        assert 'x' not in d
        assert 'fo' not in d


    def test_getitem(self):
        d = self.dawg()

        assert d['foo'] == [b'data1', b'data3']
        assert d['bar'] == [b'data2']
        assert d['foobar'] == [b'data4']


    def test_getitem_missing(self):
        d = self.dawg()

        with pytest.raises(KeyError):
            d['x']

        with pytest.raises(KeyError):
            d['food']

        with pytest.raises(KeyError):
            d['foobarz']

        with pytest.raises(KeyError):
            d['f']

    def test_keys(self):
        d = self.dawg()
        assert d.keys() == ['bar', 'foobar', 'foo', 'foo'] # order?

    def test_key_completion(self):
        d = self.dawg()
        assert d.keys('fo') == ['foobar', 'foo', 'foo'] # order?

    def test_items(self):
        d = self.dawg()
        assert sorted(d.items()) == sorted(self.DATA)

    def test_items_completion(self):
        d = self.dawg()
        assert d.items('foob') == [('foobar', b'data4')]


class TestRecordDAWG(object):

    STRUCTURED_DATA = (  # payload is (length, vowels count, index) tuple
        ('foo',     (3, 2, 0)),
        ('bar',     (3, 1, 0)),
        ('foo',     (3, 2, 1)),
        ('foobar',  (6, 3, 0))
    )

    def dawg(self):
        path = data_path("small", "record.dawg")
        return dawg_python.RecordDAWG("=3H").load(path)

    def test_getitem(self):
        d = self.dawg()
        assert d['foo'] == [(3, 2, 0), (3, 2, 1)]
        assert d['bar'] == [(3, 1, 0)]
        assert d['foobar'] == [(6, 3, 0)]

    def test_getitem_missing(self):
        d = self.dawg()

        with pytest.raises(KeyError):
            d['x']

        with pytest.raises(KeyError):
            d['food']

        with pytest.raises(KeyError):
            d['foobarz']

        with pytest.raises(KeyError):
            d['f']

    def test_record_items(self):
        d = self.dawg()
        assert sorted(d.items()) == sorted(self.STRUCTURED_DATA)

    def test_record_keys(self):
        d = self.dawg()
        assert sorted(d.keys()) == ['bar', 'foo', 'foo', 'foobar',]

    def test_record_keys_prefix(self):
        d = self.dawg()
        assert sorted(d.keys('fo')) == ['foo', 'foo', 'foobar']
        assert d.keys('bar') == ['bar']
        assert d.keys('barz') == []