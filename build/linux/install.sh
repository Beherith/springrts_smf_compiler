#!/usr/bin/sh

if [ "$USER" != "root" ]
then
    echo "Please run this as root or with sudo."
    exit 2
fi

mkdir -p /opt/pymapconv
cp ../../bin/pymapconv /opt/pymapconv/pymapconv
ln -fs /opt/pymapconv/pymapconv /usr/bin/pymapconv
ln -fs /opt/pymapconv/pymapconv /usr/bin/smfc
