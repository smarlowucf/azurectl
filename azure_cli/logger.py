# core
import sys


class Logger:
    @classmethod
    def info(self, message, message_type='INFO'):
        sys.stdout.write("{0}: {1}\n".format(message_type, message))

    @classmethod
    def error(self, message, message_type='ERROR'):
        sys.stdout.write("{0}: {1}\n".format(message_type, message))

    @classmethod
    def progress(self, current, total, prefix, bar_length=40):
        try:
            percent = float(current) / total
        except:
            # we don't want the progress to raise an exception
            # In case of any error e.g division by zero the current
            # way out is to skip the progress update
            return
        hashes = '#' * int(round(percent * bar_length))
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\r{0}: [{1}] {2}%".format(
            prefix, hashes + spaces, int(round(percent * 100))
        ))
        sys.stdout.flush()
