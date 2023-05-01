# Changelog

Here you can find rough outline of the changes.
Most of the relevant changes to different versions can be found on the [release page](https://github.com/Beherith/springrts_smf_compiler/releases) for a given version.

### Version 4.1
 - Now uses python3, thanks to grshafer!
 - Linux version now uses compressionator instead of imagemagick for speed and quality, thanks The-Yak!
 - Executables are now built using github actions! Such magic!

### Version 4.0
- Multithreaded compilation is now super fast (windows only)
- Add mapnormals, splatdistribution, and specular map dds compressors via nvtt_export.exe in a separate process (windows only)
- Also generate minimap preview jpg, and thumbnail png for Chobby
- Highresolution heightmap support, with multiple scaling options (nearest recommended)
- Better print_flush (thanks grschafer!)
- Linux tooling for dds drag-and-drop support (thanks The-Yak!)

Added NVTT_DragAndDropConvertToDDSTools.7z, a set of tools for very easy conversion of map images of any size to .DDS format! Just drag and drop images onto the .bat files!
### Version 3.4
- Minimap autosizing is supported now
- Minor bugfixes :D

### Version 3.1
- Heightmaps same size as the diffuse texture are supported, and resized intelligently to get pixel-perfect heightmaps (solves the X to X/8 + 1 image interpolation problem)
- Grass map is resized with nearest neighbour
- Metal map is resized with bilinear filtering
- More verbose and informative output
- Works from anywhere (it is no longer required to copy into the maps working directory)