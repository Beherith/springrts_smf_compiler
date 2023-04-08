#!/usr/bin/sh

DIR="$( dirname -- "${BASH_SOURCE[0]}"; )";
DIR="$( realpath -e -- "$DIR"; )";

if [ -z "$1" ]; then
    distpath="$DIR/../../bin"
    echo "No dist path provided. Using default: $distpath"
else
    distpath=$1
fi

python3 -m PyInstaller --noconfirm --workpath=$DIR/build --distpath=$distpath $DIR/.spec