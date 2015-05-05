from nose.tools import *

from azure_cli.filetype import FileType

from azure_cli.azurectl_exceptions import *


class TestFileType:
    def setup(self):
        self.filetype = FileType('../data/blob.xz')

    def test_is_xz(self):
        assert self.filetype.is_xz() == True
