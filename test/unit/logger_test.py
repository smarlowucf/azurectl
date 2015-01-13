from azure_cli.logger import Logger

class TestLogger:
    def test_info(self):
        assert Logger._print('bob') == 'INFO: bob'

    def test_error(self):
        assert Logger._print('bob', 'ERROR') == 'ERROR: bob'
