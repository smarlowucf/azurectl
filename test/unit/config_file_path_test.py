import mock
from nose.tools import *
from mock import patch

import nose_helper

from azurectl.azurectl_exceptions import *
from azurectl.config_file_path import ConfigFilePath

import os


class TestConfigFilePath:
    def test_home_path_linux(self):
        with patch.dict('os.environ', {'HOME': 'foo'}):
            paths = ConfigFilePath('lin')
            print paths.default_new_config()
            assert paths.default_new_config() == \
                os.environ['HOME'] + '/.config/azurectl/config'

    def test_home_path_win(self):
        with patch.dict('os.environ', {'HOMEPATH': 'foo'}):
            paths = ConfigFilePath('win')
            assert paths.default_new_config() == \
                os.environ['HOMEPATH'] + '/.config/azurectl/config'
        with patch.dict('os.environ', {'UserProfile': 'foo'}):
            paths = ConfigFilePath('win')
            assert paths.default_new_config() == \
                os.environ['UserProfile'] + '/.config/azurectl/config'

    @patch('os.path.isfile')
    def test_default_path(self, mock_isfile):
        mock_isfile.return_value = True
        with patch.dict('os.environ', {'HOME': 'foo'}):
            paths = ConfigFilePath('lin')
            assert paths.default_config() == \
                os.environ['HOME'] + '/' + paths.config_files[0]