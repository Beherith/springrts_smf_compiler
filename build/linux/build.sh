#!/usr/bin/sh

if [ -z "$1" ]; then
    distpath="../../bin"
    echo "No dist path provided. Using cwd: $distpath"
else
    distpath=$1
fi

python3 -m PyInstaller --noconfirm --distpath=$distpath .spec