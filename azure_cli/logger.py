class Logger:
    @classmethod
    def info(self, message):
        print Logger._print(message)

    @classmethod
    def error(self, message):
        print Logger._print(message, 'ERROR')

    @classmethod
    def _print(self, message, type='INFO'):
        return type + ': ' + str(message)
