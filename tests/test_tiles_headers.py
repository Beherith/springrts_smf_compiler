import unittest
import random
from src.smf.headers import TileFileHeader, TileHeader


class SmfHeaderBaseTests(unittest.TestCase):
    tile_file: TileFileHeader
    tile: TileHeader

    def setUp(self):
        self.tile_file = TileFileHeader()
        self.tile = TileHeader()

    def test_tile_file_same_after_pack_unpack(self):
        self.tile_file.tile_count = random.randint(0, 1000)

        test_payload = self.tile_file.pack()
        unpacked = TileFileHeader().unpack(test_payload)

        self.assertEqual(self.tile_file, unpacked)

    def test_tile_same_after_pack_unpack(self):
        self.tile.tile_file_count = 3
        self.tile.tile_count = 100

        test_payload = self.tile.pack()
        unpacked = TileHeader().unpack(test_payload)

        self.assertEqual(self.tile, unpacked)
