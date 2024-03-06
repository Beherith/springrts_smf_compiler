from struct import Struct
from .base import SMFHeader


class SMFExtraHeader(SMFHeader):
    """
    Python representation of the extra header. Maps to the following:

    int size;
    int type;
    int extraOffset;
    """

    # Size of the extra header
    _size: int

    # Type of the extra header. e.g. 1=vegetation map
    _type: int

    # Missing from docs. Only exists if type=1 (vegetation map)
    _extra_offset: int

    # Layout of the struct used for packing.
    __struct_def: Struct = Struct('< i i i')

    def pack(self):
        return self.__struct_def.pack(
            self._size,
            self._type,
            self._extra_offset
        )
