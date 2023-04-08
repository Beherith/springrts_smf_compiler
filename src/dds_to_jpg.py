import os
import sys

for file in os.listdir(os.getcwd()):
	base = file.replace('_mini.dds','')
	base = base.rpartition('_')[0]
	if file.endswith('_mini.dds'):
		os.system('magick convert "%s" -quality 50 "%s.jpg"'%(file,base))
		os.system('magick convert "%s" -resize 64x64 "%s.png"'%(file,base))