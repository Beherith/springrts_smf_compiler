from pymapconv import SMFMapDecompiler

import os
import sys

print("Usage: command line parameter is a path to unzip maps from, defaults to cwd, puts minimap dds into cwd")
print("Works best if maps are in cwd, otherwise it bugs out. Also appends map size to .smf name")
workdir = os.getcwd() if len(sys.argv) < 2 else sys.argv[1]
workdir = "N:/maps/SPRINGFILES/temp/maps"

for smffile in os.listdir(workdir):
    if smffile.lower().endswith('.smf'):
        try:
            SMFMapDecompiler(os.path.join(workdir, smffile), skiptexture=True)
        except:
            print("Failed to decompile:", smffile)
