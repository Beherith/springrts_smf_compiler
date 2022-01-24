# PyMapConv
# springrts_smf_compiler
This tool allows the compilation and decompilation of image files to SpringRTS's binary SMF (Spring Map Format) map format. 

https://springrts.com/

To use the tool, place it in your /maps folder and launch pymapconv.py or start pymapconv.exe

Miraculously self documenting.

Read my guide on how to actually make maps for Spring: https://docs.google.com/document/d/1PL8U2bf-c5HuSVAihdldDTBA5fWKoeHKNb130YDdd-w/edit#

![gooey](https://raw.githubusercontent.com/Beherith/springrts_smf_compiler/master/pymapconv_gui.png)

## NEW FEATURES:

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

##  Windows usage:

Dowload and use the precompiled version in pymapconv.exe in this repository
The windows build is 64 bit, thus allowing the compilation of maps up 64x64 size!
Ensure that nvdxt.exe is next to it. 

### Windows development:

Download Anaconda2 64bit - https://repo.anaconda.com/archive/Anaconda2-2019.10-Windows-x86_64.exe
Download upx - https://github.com/upx/upx/releases/download/v3.96/upx-3.96-win64.zip
Download PyQt4 https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/
	Install to pymapconv environment see below

## In anaconda console - Create environment and install pyinstaller
* conda create -n pymapconv python=2.7
* conda activate pymapconv
* conda install -c conda-forge pyinstaller - https://stackoverflow.com/a/66363079/7671671

## Compile instructions
activate pymapconv
pyinstaller --upx-dir c:\somepath\Anaconda2\upx\ --onefile pymapconv.py



### Linux (e.g. Ubuntu 14.04 and up), or for development it requires:
Youre a big boy, go get the libs:
Python 2.7
Pillow (sudo pip install Pillow)
PyQt4  (sudo apt-get install python-Qt4)
ImageMagick (sudo apt-get install imagemagick)

## by Beherith 

Note2self for exe build:
activate pymapconv
pyinstaller --onefile pymapconv.py

