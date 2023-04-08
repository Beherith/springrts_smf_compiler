from random import randint

outf = open("featureplacement_set.lua","w")
fdef = None
fx = None
fz = None
fy = None
def ex(s,k):
	return s.partition(k)[2].strip().strip(',').strip()
for line in open('model.lua').readlines():
	if 'defName = ' in line:
		fdef = ex(line," defName = ")
	if ' pos = {' in line:
		fx = 0
		fz = 0
	if fx == 0 or fz == 0:
		if ' x = ' in line:
			fx = int(float( ex(line," x = ")))
		if ' z = ' in line:
			fz = int(float( ex(line," z = ")))
	if ' rot = {' in line:
		fy = 0
	if fy == 0:
		if ' y = ' in line:
			fy = float(float(ex(line," y = ")))
			fy = int(fy*-10185.925)
			o = '{ name = %s, x = %d, z = %d, rot = %d },'%(fdef,fx,fz,fy)
			print (o)
			outf.write(o+'\n')
			name = None
			fx = None
			fz = None
			fy = None
