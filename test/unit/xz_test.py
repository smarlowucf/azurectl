from nose.tools import *

import nose_helper

from azurectl.xz import XZ


class TestXZ:
    def setup(self):
        self.xz = XZ.open('../data/blob.xz')

    def test_read(self):
        assert self.xz.read(128) == 'foo'

    def test_uncompressed_size(self):
        assert XZ.uncompressed_size('../data/blob.xz') == 4
