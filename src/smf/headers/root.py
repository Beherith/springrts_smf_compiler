from struct import Struct
import random
from .base import SMFHeader


class SMFRootHeader(SMFHeader):
    """
    Python representation of the root map header struct. Maps to the following:

    char magic[16];
    int version;
    int mapId;

    int mapX;
    int mapY;
    int squareSize;
    int texelPerSquare;
    int tileSize;
    float minHeight;
    float maxHeight;

    int heightmapPtr;
    int typeMapPtr;
    int tilesPtr;
    int minimapPtr;
    int metalMapPtr;
    int featurePtr;

    int numExtraHeaders;
    """

    # Magic value. Null-terminated string of 15 characters.
    magic: bytes

    # Version (of the SMF protocol?) must be "1"
    version: int

    # Unique ID of the map, chosen randomly
    map_id: int

    # X-size of the map.
    map_x: int = None

    # Y-size of the map
    map_y: int = None

    # Spring-engine height corresponding to 0 on the heightmap
    min_height: float = None

    # Spring engine height corresponding to 0xFFFF on the heightmap
    max_height: float = None

    # Amount of headers following the main header
    extra_header_count: int

    # Distance between vertices. Must be 8.
    square_size: int

    # Number of texels per square. Must be 8.
    texel_per_square: int

    # Number of texels in a tile. Must be 32.
    tile_size: int

    # File offset to elevation data (short int[(mapy+1)*(mapx+1)])
    heightmap_offset: int = None

    # File offset to type data (unsigned char[mapy//2 * mapx//2])
    type_map_offset: int = None

    # File offset to tile data (see MapTileHeader)
    tiles_offset: int = None

    # File offset to minimap (always 1024*1024 dxt1 compressed data plus 8 mipmap sublevels)
    minimap_offset: int = None

    # File offset to metal map (unsigned char[mapx//2 * mapy//2])
    metal_map_offset: int = None

    # File offset to feature data (see MapFeatureHeader)
    feature_data_offset: int = None

    # Layout of the struct used for packing.
    _struct_def: Struct = Struct('< 16s i i i i i i i f f i i i i i i i')

    def __init__(self):
        self.magic = 'spring map file\0'.encode()
        self.version = 1
        self.map_id = random.randint(0, 31 ** 2)
        self.square_size = 8
        self.texel_per_square = 8
        self.tile_size = 32
        self.extra_header_count = 0

    def set_map_size(self, x: int, y: int):
        self.map_x = x
        self.map_y = y

    def set_map_heights(self, min_height: float, max_height: float):
        self.min_height = min_height
        self.max_height = max_height

    def set_heightmap_offset(self, offset: int):
        self.heightmap_offset = offset

    def set_metal_map_offset(self, offset: int):
        self.metal_map_offset = offset

    def pack(self):
        return self._struct_def.pack(
            self.magic,
            self.version,
            self.map_id,
            self.map_x,
            self.map_y,
            self.square_size,
            self.texel_per_square,
            self.tile_size,
            self.min_height,
            self.max_height,
            self.heightmap_offset,
            self.type_map_offset,
            self.tiles_offset,
            self.minimap_offset,
            self.metal_map_offset,
            self.feature_data_offset,
            self.extra_header_count
        )

    def validate(self):
        if self.map_x is None or self.map_y is None:
            raise ValueError("Map size is not set")
        if self.min_height is None or self.max_height is None:
            raise ValueError("Map min/max heights are not set")
        if self.heightmap_offset is None:
            raise ValueError("Heightmap is not set")
        if self.type_map_offset is None:
            raise ValueError("Type map is not set")
        if self.tiles_offset is None:
            raise ValueError("Tile data is not set")
        if self.minimap_offset is None:
            raise ValueError("Minimap data is not set")
        if self.metal_map_offset is None:
            raise ValueError("Metal map is not set")
        if self.feature_data_offset is None:
            raise ValueError("Feature data is not set")

    def unpack(self, payload: bytes) -> SMFHeader:
        unpacked = self._struct_def.unpack(payload)
        self.magic,\
            self.version,\
            self.map_id,\
            self.map_x,\
            self.map_y,\
            self.square_size,\
            self.texel_per_square,\
            self.tile_size,\
            self.min_height,\
            self.max_height,\
            self.heightmap_offset,\
            self.type_map_offset,\
            self.tiles_offset,\
            self.minimap_offset,\
            self.metal_map_offset,\
            self.feature_data_offset,\
            self.extra_header_count = unpacked

        return self
