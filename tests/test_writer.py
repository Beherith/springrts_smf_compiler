import unittest
from io import BytesIO

from src.smf.writer import SMFWriter
from src.smf.smf_file import SMFFile


class InMemorySMFMap(SMFFile):
    """
    In-memory implementation of the SMFMap. Used for testing.
    """

    _buffer: BytesIO

    def __init__(self):
        super().__init__()
        self._buffer = BytesIO()

    def is_writeable(self):
        return self._buffer.writable()

    def write(self, data: bytes):
        self._buffer.write(data)

    def read(self) -> bytes:
        return self._buffer.read()

    def clean_up(self):
        self._buffer.close()


class SmfWriterTests(unittest.TestCase):

    _writer: SMFWriter
    _in_memory_map: InMemorySMFMap

    def setUp(self) -> None:
        self._in_memory_map = InMemorySMFMap()
        self._writer = SMFWriter(self._in_memory_map)

    def tearDown(self) -> None:
        self._in_memory_map.clean_up()

    def test_writing_non_configured_map_fails(self):
        self.assertRaises(ValueError, lambda: self._writer.write())

    def test_writing_configured_root_ok(self):
        writer = self._writer
        writer.set_map_size(24, 24)
        writer.set_map_heights(0, 100)
        writer.
        writer.write()
        map_bytes = self._in_memory_map.read()
        self.assertNotEquals(len(map_bytes), 0)
