from struct import Struct


class SMFHeader:

    # Data layout for the header
    _struct_def: Struct

    def pack(self) -> bytes:
        raise NotImplementedError("Pack not implemented for header type!")

    def unpack(self, payload: bytes):
        raise NotImplementedError("Unpack not implemented for header type!")

    def validate(self):
        raise NotImplementedError("Validate is not implemented for header type!")
