import lzma

class XZ:
    lzma_stream_buffer = 8192

    @classmethod
    def open(self, file_name, buffer_size = lzma_stream_buffer):
        self.lzma_stream = open(file_name, 'rb')
        return XZ(self.lzma_stream, buffer_size)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lzma_stream.close()

    def __init__(self, lzma_stream, buffer_size = lzma_stream_buffer):
        self.lzma_stream = lzma_stream
        self.buffer_size = buffer_size
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
