from struct import Struct
import random


class SMFHeader:
    """
    Python representation of the SMFHeader struct. Maps to the following:

    char magic[16];
    int version;
    int mapid;

    int mapx;
    int mapy;
    int squareSize;
    int texelPerSquare;
    int tilesize;
    float minHeight;
    float maxHeight;

    int heightmapPtr;
    int typeMapPtr;
    int tilesPtr;
    int minimapPtr;
    int metalmapPtr;
    int featurePtr;

    int numExtraHeaders;
    """

    # Magic value - null-terminated 'spring map file' string
    _magic: bytes = []

    # Version (of the SMF protocol?) must be "1"
    _version: int

    # Unique ID of the map, chosen randomly
    _map_id: int

    # X-size of the map.
    _map_x: int

    # Y-size of the map
    _map_y: int

    # Spring-engine height corresponding to 0 on the heightmap
    _min_height: float

    # Spring engine height corresponding to 0xFFFF on the heightmap
    _max_height: float

    # Amount of headers following the main header
    _extra_header_count: int

    # Distance between vertices. Must be 8.
    __square_size: int

    # Number of texels per square. Must be 8.
    __texel_per_square: int

    # Number of texels in a tile. Must be 32.
    __tile_size: int

    # File offset to elevation data (short int[(mapy+1)*(mapx+1)])
    _heightmap_offset: int

    # File offset to type data (unsigned char[mapy//2 * mapx//2])
    _type_map_offset: int

    # File offset to tile data (see MapTileHeader)
    _tiles_offset: int

    # File offset to minimap (always 1024*1024 dxt1 compressed data plus 8 mipmap sublevels)
    _minimap_offset: int

    # File offset to metal map (unsigned char[mapx//2 * mapy//2])
    _metal_map_offset: int

    # File offset to feature data (see MapFeatureHeader)
    _feature_data_offset: int

    # Layout of the struct used for packing.
    __struct_def: Struct = Struct('< 16s i i i i i i i f f i i i i i i i')

    def __init__(self):
        self._magic = 'spring map file\0'.encode()
        self._version = 1
        self._map_id = random.randint(0, 31 ** 2)
        self.__square_size = 8
        self.__texel_per_square = 8
        self.__tile_size = 32

    def pack(self):
        """ Produces a binary representation of the SMF file """
        return self.__struct_def.pack(
            self._magic,
            self._version,
            self._map_id,
            self._map_x,
            self._map_y,
            self.__square_size,
            self.__texel_per_square,
            self.__tile_size,
            self._min_height,
            self._max_height
        )




SMFHeader_struct = Struct('< 16s i i i i i i i f f i i i i i i i')
