# SMF File Structure
This document outlines the structure of the spring map format file. It shows how the map data is packed into the binary
representation as is expected by the sprint engine.

# Header structure
SMF map file is made up of bits of structured data called "headers" which all have fixed structure. The chunks are
serialized into the binary format and are placed in the file.
Different headers can have links to different chunks of binary data through offsets specified in the header.
For example, the root header of the map has a few links to additional headers which are set through offsets.

In order to specify additional information, SMF uses `ExtraHeader`s which have a well-known size.
These headers must directly follow the root header. In order for the engine to know the exact amount
of headers to read, `extra_header_count` property has to be set on the root header.

Note that the order of binary data chunks in the map is arbitrary.
The chunks on the diagram are presented in the way they currently are packaged by the
map compiler. The overall structure of the map is as follows.
```mermaid
---
title: SMF Map Logical Structure
---
classDiagram
    note "All header properties are listed in the order they are packed.
      File must begin with root header and continue with all Extra Headers.
      Chunks of data could be placed arbitrarily so long as the offsets are setup
      to correctly point at them."
    note for SMFRootHeader "See smf.headers.root.py for additional information on generic data.
      All of the PTR properties refer to an offset of the data chunk inside the file.
      e.g. metal_map_offset should be equal to the byte offset at which the binary data for metal map begins.
      "
    note for SMFExtraHeader_1 "Extra headers must directly follow the root header.
      D"
    note for MinimapData "Minimal data has to be exactly 699048 bytes long
      which seems pretty weird considering it doesnt align to KiB or MiB.
      More investigation is needed."
    note for TileData "Tile data is structured. Refer to additional diagrams for details."
    note for FeatureData "Feature data is structured. Refer to additional diagrams for details."
    
    %% Order of appearance in the binary file %%
    SMFRootHeader <-- SMFExtraHeader_1: Directly Follows
    SMFExtraHeader_1 <-- SMFExtraHeader_2: Directly Follows
    SMFExtraHeader_2 <-- SMFExtraHeader_N: ...
    VegetationMapData --> SMFExtraHeader_N: Follows
    HeightMapData --> VegetationMapData: Follows
    TypeMapData --> HeightMapData: Follows
    MinimapData --> TypeMapData: Follows
    MetalMapData --> MinimapData: Follows
    TileData --> MetalMapData: Follows
    FeatureData --> TileData: Follows
    
    class SMFRootHeader {
        ==Generic Map Data==
        
        +heightmap_offset : ptr
        +type_map_offset : ptr
        +tiles_offset : ptr
        +minimap_offset : ptr
        +metal_map_offset : ptr
        +feature_data_offset : ptr
        +extra_header_count : ptr
    }

    class SMFExtraHeader_1 {
        +size: int
        +type: int
        +extra_offset : ptr
    }
    class SMFExtraHeader_2 {
        +size: int
        +type: int
        +extra_offset : ptr
    }
    class SMFExtraHeader_N {
        +size: int
        +type: int
        +extra_offset : ptr
    }
    class VegetationMapData {
        == BINARY DATA ==
    }
    class HeightMapData {
        == BINARY DATA ==
    }
    class TypeMapData {
        == BINARY DATA ==
    }
    class MinimapData {
        == BINARY DATA ==
    }
    class MetalMapData {
        == BINARY DATA ==
    }
    class TileData {
        == BINARY DATA ==
    }
    class FeatureData {
        == BINARY DATA ==
    }
```
