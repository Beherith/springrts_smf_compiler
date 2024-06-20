import unittest
import struct

from src.smf.headers.base import SMFHeader


class SmfRootHeader(unittest.TestCase):
    _base_header: SMFHeader

    def setUp(self):
        self._base_header = SMFHeader()

    def test_should_throw_when_using_base(self):
        self.assertRaises(NotImplementedError, lambda: (self._base_header.pack()))

        test_payload = struct.pack("< i", 10)
        self.assertRaises(NotImplementedError, lambda: (self._base_header.unpack(test_payload)))
