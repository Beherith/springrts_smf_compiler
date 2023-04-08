import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os"],
    "excludes": ["Tkinter", "Tk", "Tcl"],
    "include_files": [
        "icon.ico",
        "nvdxt.exe",
        "../../LICENSE",
        "../../README.md",
        "../geovent.bmp"
    ]
}

# GUI applications require a different base on Windows
# (the default is for a console application).
base = None

if sys.platform == "win32":
    base = "Win32GUI"

target = Executable(
    script="pymapconv.py",
    base=base,
    targetName="pyMapConv.exe",
    compress=False,
    copyDependentFiles=True,
    appendScriptToExe=True,
    appendScriptToLibrary=False,
    icon="icon.ico",
    shortcutName="SMF compiler/decompiler",
    shortcutDir="DesktopFolder",
)

setup(
    name="pyMapConv",
    version="0.1",
    author="Beherith (mysterme@gmail.com)",
    description="SMF compiler/decompiler",
    options={"build_exe": build_exe_options},
    executables=[target]
)
