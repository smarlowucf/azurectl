from nose.tools import *

from azurectl.filetype import FileType

from azurectl.azurectl_exceptions import *


class TestFileType:
    def setup(self):
        self.filetype_xz = FileType('../data/blob.xz')
        self.filetype_not_xz = FileType('../data/id_test')

    def test_is_xz(self):
        assert self.filetype_xz.is_xz() is True

    def test_not_xz(self):
        assert self.filetype_not_xz.is_xz() is False
