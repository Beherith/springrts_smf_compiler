# PyMapConv
### by Beherith <sub>[and the gang](https://github.com/Beherith/springrts_smf_compiler/graphs/contributors).</sub>
This tool allows the compilation and decompilation of image files to SpringRTS's binary SMF (Spring Map Format) map
format.

https://springrts.com/

To use the tool, place it in your /maps folder and launch pymapconv.py or start pymapconv.exe

Miraculously self documenting.

Read Beherith's guide on how to actually make maps for
Spring: https://docs.google.com/document/d/1PL8U2bf-c5HuSVAihdldDTBA5fWKoeHKNb130YDdd-w/edit#

![gooey](https://raw.githubusercontent.com/Beherith/springrts_smf_compiler/master/doc/pymapconv_gui.png)

## Recent Changes

Changes to individual releases should be listed on each individual release and/or in
the [change log.](/doc/CHANGELOG.md)

## Usage
Usage may vary depending on how you wish to run the tool. Recommended way is to download the latest release from GitHub:

[Releases Page](https://github.com/Beherith/springrts_smf_compiler/releases)

### Windows
Windows builds are self-contained and should have everything pre-packaged. Run the one-file executable to launch.
You may find the additional tools included in the `/tools` directory to be useful for converting textures.

### Linux
Builds for Linux have some additional dependencies not pre-packaged with the compiler.

Installation of these packages depends on your chosen distribution and is therefore up to you to figure out how to install.
Software you will need is:
- Compressonator CLI (https://github.com/GPUOpen-Tools/compressonator)
- ImageMagick (https://github.com/ImageMagick/ImageMagick)

### Running From Source
In order to run the compiler from source, you will need to install python and get the build dependencies **in addition**
to the runtime dependencies for your platform:
```
# Once required dependencies are installed (see the section for your OS)
# Navigate your shell or terminal into this repo
$ cd springrts_smf_compiler

# Install dependencies listed in requirements file using the version of python you installed
$ python3 -m pip install -r src/requirements.txt
```

You can then run the program either by launching it with no arguments (GUI mode) or providing the necessary arguments
(CLI mode).
```
$ python3 src/pymapconv.py
```

## Development
Follow the instructions above to run the compiler from source. If you wish to contribute to the software, check out the
[development guide](doc/DEV.md).
