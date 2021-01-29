from pymapconv import SMFMapDecompiler
import pyunpack
import os
import sys
import shutil
print ("Usage: command line parameter is a path to unzip maps from, defaults to cwd, puts minimap dds into cwd")
print ("Works best if maps are in cwd, otherwise it bugs out. Also appends map size to .smf name")
workdir =  os.getcwd() if len(sys.argv)<2 else sys.argv[1]
tmpdir = os.path.join(workdir,'temp')
os.mkdir(tmpdir)
for file in os.listdir( workdir):
	if file.lower().endswith('.sd7') or file.lower().endswith('.sdz'):
		if file.endswith('7'):
			renamedmapfile = file[:-3]+'7z'
			shutil.copyfile(os.path.join(workdir,file),os.path.join(tmpdir,renamedmapfile))
		else:
			renamedmapfile = file[:-3]+'zip'
			shutil.copyfile(os.path.join(workdir,file),os.path.join(tmpdir,renamedmapfile))
		unzipdir = os.path.join(tmpdir,file)
		pyunpack.Archive(os.path.join(tmpdir,renamedmapfile)).extractall(unzipdir, auto_create_dir = True)
		for smffile in os.listdir(os.path.join(unzipdir,'maps')):
			if smffile.lower().endswith('.smf'):
				SMFMapDecompiler(os.path.join(unzipdir,'maps',smffile),minimaponly = True)
try:
	shutil.rmtree(tmpdir)
except:
	print ("Failed to remove ",tmpdir)