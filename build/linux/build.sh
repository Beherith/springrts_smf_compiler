#!/usr/bin/sh

SRC=$(readlink -f ${BASH_SOURCE[0]})
DIR=$(dirname ${SRC})

if [ -z "$1" ]; then
    distpath="$DIR/../../bin"
    echo "No dist path provided. Using default: $distpath"
else
    distpath=$1
fi

python3 -m PyInstaller --noconfirm --workpath=$DIR/build --distpath=$distpath $DIR/.spec