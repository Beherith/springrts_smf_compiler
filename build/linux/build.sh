#!/usr/bin/sh

if [ -z "$1" ]; then
    distpath="../../bin"
    echo "No dist path provided. Using cwd: $distpath"
else
    distpath=$1
fi

python3 -m PyInstaller \
    --noconfirm --onefile --log-level=WARN --noupx \
    --paths '../../src' \
    --distpath $distpath \
    --add-data '../../resources/*:resources' \
    --add-data '../../LICENSE:.' \
    --noconfirm \
    '../../src/pymapconv.py'