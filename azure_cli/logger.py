class Logger:
    @classmethod
    def info(self, message, message_type='INFO'):
        print Logger._print(message, message_type)

    @classmethod
    def error(self, message, message_type='ERROR'):
        print Logger._print(message, message_type)

    @classmethod
    def _print(self, message, message_type):
        return message_type + ': ' + str(message)
