
# springrts_smf_compiler
This tool allows the compilation and decompilation of image files to SpringRTS's binary SMF (Spring Map Format) map format. 

https://springrts.com/

To use the tool, place it in your /maps folder and launch pymapconv.py or start pymapconv.exe

Miraculously self documenting.

![gooey](https://raw.githubusercontent.com/Beherith/springrts_smf_compiler/master/pymapconv_gui.png)

## NEW FEATURES:

Added NVTT_DragAndDropConvertToDDSTools.7z, a set of tools for very easy conversion of map images of any size to .DDS format! Just drag and drop images onto the .bat files!

### Version 3.1
- Heightmaps same size as the diffuse texture are supported, and resized intelligently to get pixel-perfect heightmaps (solves the X to X/8 + 1 image interpolation problem)
- Grass map is resized with nearest neighbour
- Metal map is resized with bilinear filtering
- More verbose and informative output
- Works from anywhere (it is no longer required to copy into the maps working directory)

##  Windows usage:

Dowload and use the precompiled version in pymapconv.exe in this repository
The windows build is 64 bit, thus allowing the compilation of maps up 64x64 size!
Ensure that nvdxt.exe is next to it. 

### Windows development:

Python 2.7, 32bit -  https://www.python.org/downloads/

PIL (Python Image Library) -http://www.pythonware.com/products/pil/ 

PyQt4 - https://riverbankcomputing.com/software/pyqt/download (note: PyQt no longer provides Windows binaries, but you can obtain slightly old and suitable ones from https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/)

## Linux (e.g. Ubuntu 14.04 and up), or for development it requires:
Youre a big boy, go get the libs:
Python 2.7
Pillow (sudo pip install Pillow)
PyQt4  (sudo apt-get install python-Qt4)
ImageMagick (sudo apt-get install imagemagick)

## by Beherith 
