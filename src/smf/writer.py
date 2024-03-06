import logging

from .headers.root import SMFRootHeader
from .smf_file import SMFFile

from contextlib import AbstractContextManager


class SMFWriter(AbstractContextManager):

    _root_header: SMFRootHeader = None
    _output: SMFFile

    def __init__(self, output: SMFFile):
        if not output.is_writeable():
            raise AssertionError("""Output map is not writable.""")

    def set_map_size(self, x: int, y: int):
        self.__ensure_root_header()
        self._root_header.set_map_size(x, y)

    def set_map_heights(self, min_height: float, max_height: float):
        self.__ensure_root_header()
        self._root_header.set_map_heights(min_height, max_height)

    def set_heightmap(self, heightmap_data: bytes):


    def write(self):
        self.__validate()

        root_header_bytes = self._root_header.pack()
        logging.info("Writing SMF Root header(%i bytes)", len(root_header_bytes))
        self._output.write(root_header_bytes)

    def __ensure_root_header(self):
        self._root_header = self._root_header or SMFRootHeader()

    def __validate(self):
        self.__ensure_root_header()
        self._root_header.validate()

    def close(self):
        self._output.close()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
