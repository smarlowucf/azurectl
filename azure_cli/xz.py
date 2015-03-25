# core
import subprocess

# extensions
import lzma

# project
from exceptions import *


class XZ:
    LZMA_STREAM_BUFFER_SIZE = 8192

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lzma_stream.close()

    def __init__(self, lzma_stream, buffer_size=LZMA_STREAM_BUFFER_SIZE):
        self.lzma_stream = lzma_stream
        self.buffer_size = int(buffer_size)
        self.lzma = lzma.LZMADecompressor()
        self.finished = False

    def read(self, size):
        if self.finished:
            # lzma stream end already reached
            return None
        chunks = self.lzma.decompress(
            self.lzma.unconsumed_tail, size
        )
        bytes_unpacked = len(chunks)
        if bytes_unpacked == size:
            # first decompression already completed the requested size
            return chunks
        while True:
            lzma_chunk = self.lzma_stream.read(self.buffer_size)
            if not lzma_chunk:
                if self.lzma.flush():
                    # must have zero data, otherwise raise
                    raise AssertionError
                # there is one superfluous newline with the last chunk
                chunks = chunks[:-1]
                self.finished = True
                break
            else:
                chunk = self.lzma.decompress(
                    self.lzma.unconsumed_tail + lzma_chunk,
                    size - bytes_unpacked
                )
                chunks += chunk
                bytes_unpacked += len(chunk)
                if bytes_unpacked == size:
                    # requested size unpacked
                    break
        return chunks

    @classmethod
    def open(self, file_name, buffer_size=LZMA_STREAM_BUFFER_SIZE):
        self.lzma_stream = open(file_name, 'rb')
        return XZ(self.lzma_stream, buffer_size)

    @classmethod
    def uncompressed_size(self, file_name):
        xz_info = subprocess.Popen(
            ['xz', '--robot', '--list', file_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, error = xz_info.communicate()
        if xz_info.returncode != 0:
            raise AzureXZError('xz: %s' % error)
        total = output.strip().split('\n').pop()
        return int(total.split()[4])
