from struct import Struct


class TileFileHeader:
    """
    Python representation of the TileFile header. Maps to the following:

    char magic[16];
    int version;

    int numTiles;
    int tileSize;
    int compressionType;
    """

    # Total number of tiles in this file
    tile_count: int

    # Magic value. Null-terminated string of 15 characters.
    magic: bytes

    # Version (of the SMF protocol?) must be "1"
    version: int

    # Number of texels in a tile. Must be 32 for now.
    tile_size: int

    # Compression type used for tiles. 1 = DTX1 is currently supported.
    compression_type: int

    # Data layout for the header
    _struct_def: Struct = Struct('< 16s i i i i')

    def __init__(self):
        self.magic = 'spring tilefile\0'.encode()
        self.version = 1
        self.tile_size = 32
        self.compression_type = 1  # 1=DXT1

    def __eq__(self, other):
        if not isinstance(other, TileFileHeader):
            return False

        # Magic values don't strictly matter so long as they are correct size
        return self.version == other.version\
            and self.tile_size == other.tile_size\
            and self.compression_type == other.compression_type

    def pack(self):
        return self._struct_def.pack(
            self.magic,
            self.version,
            self.tile_count,
            self.tile_size,
            self.compression_type
        )

    def unpack(self, payload: bytes):
        self.magic, self.version, self.tile_count, self.tile_size, self.compression_type =\
            self._struct_def.unpack(payload)
        return self


class TileHeader:
    """
    Python representation of the Map Tile Header. Maps to the following:

    int numTileFiles;
    int numTiles;
    """

    # Number of tile files to read in (usually 1)
    tile_file_count: int

    # Total number of tiles
    tile_count: int

    # Data layout for the header
    _struct_def: Struct = Struct('< i i')

    def __init__(self):
        self.tile_file_count = 1

    def __eq__(self, other):
        if not isinstance(other, TileHeader):
            return False

        return self.tile_file_count == other.tile_file_count\
            and self.tile_count == other.tile_count

    def pack(self):
        return self._struct_def.pack(
            self.tile_file_count,
            self.tile_count
        )

    def unpack(self, payload: bytes):
        self.tile_file_count, self.tile_count = self._struct_def.unpack(payload)
        return self
