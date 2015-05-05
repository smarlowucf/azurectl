from mock import patch

import nose_helper

from azure_cli.logger import log


class TestLogger:
    @patch('sys.stdout')
    def test_progress(self, mock_stdout):
        log.progress(50, 100, 'foo')
        mock_stdout.write.assert_called_once_with(
            '\rfoo: [####################                    ] 50%'
        )
        mock_stdout.flush.assert_called_once_with()
