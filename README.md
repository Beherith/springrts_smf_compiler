# PyMapConv
# springrts_smf_compiler
This tool allows the compilation and decompilation of image files to SpringRTS's binary SMF (Spring Map Format) map format. 

https://springrts.com/

To use the tool, place it in your /maps folder and launch pymapconv.py or start pymapconv.exe

Miraculously self documenting.

Read my guide on how to actually make maps for Spring: https://docs.google.com/document/d/1PL8U2bf-c5HuSVAihdldDTBA5fWKoeHKNb130YDdd-w/edit#

![gooey](https://raw.githubusercontent.com/Beherith/springrts_smf_compiler/master/pymapconv_gui.png)

## NEW FEATURES:

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


## Usage:

### Windows

Download the whole repository as a zip file, and launch the precompiled version in pymapconv.exe in this repository
The windows build is 64 bit, thus allowing the compilation of maps up 64x64 size!
Ensure that nvdxt.exe is next to it. 

### Linux

1. Download and install a recent version of Python 3
	1. You'll likely install with a package manager (e.g. `apt install python3.9`)
	2. If you want to install and isolate multiple python versions, check out [pyenv](https://github.com/pyenv/pyenv)

2. Install requirements with pip:

    ```
	# Navigate your shell or terminal into this repo
	cd springrts_smf_compiler

	# Install dependencies listed in requirements file using the version of python you installed
	/usr/bin/python3.9 -m pip install -r requirements.txt
	```

3. Some scripts or options may require ImageMagick, which you can install like:

    ```
	sudo apt install imagemagick
	```

4. Run the program (you can use the GUI or provide command-line arguments):

    ```
	/usr/bin/python3.9 pymapconv.py
	```

## Development:

### Windows

1. Download and install a recent version of Python 3 - https://www.python.org/downloads/
    1. Most likely you want to download and run the "Windows installer"
	    1. Take note of the path you install python to!

2. Install requirements with pip:

    ```
	# Navigate your shell or command prompt into this repo
	cd springrts_smf_compiler

	# Install dependencies listed in requirements file using the version of python you installed
	C:\Users\YourName\AppData\Local\Programs\Python\Python310\python.exe -m pip install -r requirements.txt
	```

3. (Optional) If you want to build an exe, install and use pyinstaller:

    ```
	# Install pyinstaller
	C:\Users\YourName\AppData\Local\Programs\Python\Python310\python.exe -m pip install -r requirements-dev.txt

	# Use pyinstaller to create an exe
	C:\Users\YourName\AppData\Local\Programs\Python\Python310\Scripts\pyinstaller.exe --onefile pymapconv.py
	```

4. (Optional) If you wish to compress the resulting exe file, download and extract a release of [UPX](https://github.com/upx/upx) then run [pyinstaller](https://pyinstaller.org/en/stable/usage.html#using-upx) as 

    ```
	# Substitute the path to your pyinstaller.exe file and extracted upx folder
	C:\Users\YourName\AppData\Local\Programs\Python\Python310\Scripts\pyinstaller.exe --upx-dir E:\Apps\upx-3.96-win64 --onefile pymapconv.py
	```

### Linux

Follow the Linux Usage instructions above and you're all set for development!

## by Beherith 

Note2self for exe build:
activate pymapconv
pyinstaller --onefile pymapconv.py

