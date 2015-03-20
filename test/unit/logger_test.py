from azure_cli.logger import Logger

from mock import patch

class TestLogger:
    @patch('sys.stdout')
    def test_info(self, mock_stdout):
        Logger.info('bob')
        mock_stdout.write.assert_called_once_with('INFO: bob\n')

    @patch('sys.stdout')
    def test_error(self, mock_stdout):
        Logger.error('bob')
        mock_stdout.write.assert_called_once_with('ERROR: bob\n')

    @patch('sys.stdout')
    def test_progress(self, mock_stdout):
        Logger.progress(50, 100, 'foo')
        mock_stdout.write.assert_called_once_with(
            '\rfoo: [####################                    ] 50%'
        )
        mock_stdout.flush.assert_called_once_with()
