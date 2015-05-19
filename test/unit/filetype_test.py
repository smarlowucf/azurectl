from nose.tools import *

from azurectl.filetype import FileType

from azurectl.azurectl_exceptions import *


class TestFileType:
    def setup(self):
        self.filetype = FileType('../data/blob.xz')

    def test_is_xz(self):
        assert self.filetype.is_xz() == True
