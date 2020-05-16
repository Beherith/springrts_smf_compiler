# springrts_smf_compiler
This tool allows the compilation and decompilation of image files to SpringRTS's binary SMF (Spring Map Format) map format. 

https://springrts.com/

To use the tool, place it in your /maps folder and launch pymapconv.py or start pymapconv.exe

Miraculously self documenting:
![gooey](https://raw.githubusercontent.com/Beherith/springrts_smf_compiler/master/pymapconv_gui.png)


#### 2019 UPDATE: Windows EXE available, pymapconv.exe works as long as nvdxt.exe is next to it :)

The windows build is 64 bit, thus allowing the compilation of maps up 64x64 size!


#### 2014 Outdated: Under Windows, you will need the following to make this work:

Dowload the precompiled version from here 
https://springrts.com/phpbb/viewtopic.php?f=56&t=34378&start=20

OR


Python 2.7, 32bit -  https://www.python.org/downloads/

PIL (Python Image Library) -http://www.pythonware.com/products/pil/ 

PyQt4 - https://riverbankcomputing.com/software/pyqt/download (note: PyQt no longer provides Windows binaries, but you can obtain slightly old and suitable ones from https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/)

#### Under Linux (e.g. Ubuntu 14.04 and up), it requires:
Youre a big boy, go get the libs:
Python 2.7
Pillow (sudo pip install Pillow)
PyQt4  (sudo apt-get install python-Qt4)
ImageMagick (sudo apt-get install imagemagick)

