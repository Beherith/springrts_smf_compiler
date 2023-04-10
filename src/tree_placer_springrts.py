from PIL import Image
import random
import numpy as np
import sys

input_imagefile_name = "tetrad_v3_feature_distribution.png"
base_treename = "allpinesb_ad0_%s_%s_%s"  # color type size
outputline = '{ name = \'%s\', x = %d, z = %d, rot = "%d" ,scale = 1.000000 },'
colors = ['green', 'brown', 'snow', 'snowgreen']
types = ['a', 'b', 'c']
sizes = ['m', 'l', 'xl', 'xxl']
snowy_pine_trees = []
green_pine_trees = []
for size in sizes:
    for type in types:
        for color in colors:
            if 'snow' in color:
                snowy_pine_trees.append(base_treename % (color, type, size))
            else:
                green_pine_trees.append(base_treename % (color, type, size))
rocks = ['agorm_rock1', 'agorm_rock2', 'agorm_rock3', 'agorm_rock4', 'agorm_rock5']
palm_trees = ['ad0_senegal_1', 'ad0_senegal_2', 'ad0_senegal_3', 'ad0_senegal_4', 'ad0_senegal_5', 'ad0_senegal_6',
              'ad0_senegal_7', 'ad0_senegal_1_large', 'ad0_senegal_2_large', 'ad0_senegal_3_large',
              'ad0_senegal_4_large', 'ad0_senegal_5_large', 'ad0_senegal_6_large', 'ad0_senegal_7_large']
shrooms = ['mushroom0%d' % i for i in range(1, 10)]
ferns = ['cycas%d' % i for i in range(1, 9)]

# SPECIFY WHAT KIND OF FEATURES YOU WANT
RED_FEATURES = shrooms
GREEN_FEATURES = ferns
BLUE_FEATURES = green_pine_trees

# SPECIFY THE PROBABILITY THAT A FEATURE WILL BE PLACED
red_probability = 0.03 * 5
green_probability = 0.005 * 5
blue_probability = 0.03 * 5

# SPECIFY WHETHER YOU WANT HIGHER INPUT PIXEL COLOR INTERPRETED AS A SIZE BIAS OR AS A PROBABILITY FOR PLACEMENT # TODO
red_sizebias = False
green_sizebias = False
blue_sizebias = False

geos = []  # list of geo clusters, [centerx, centery, [pointsx],[pointsy] ]
print(
    "Usage: specify a .bmp image to work on\n Red, Green and Blue channels specify different feature classes that will be randomly placed\n Alpha channel small values mark geovents.\nEdit the feature lists in this file to change what kind of features you want.")
if len(sys.argv) >= 2:
    input_imagefile_name = sys.argv[1]


def clusterGeos(x, y):
    newGeo = True
    for geo in geos:
        if (abs(geo[0] - x) + abs(geo[1] - y)) < 10:
            geo[2].append(x)
            geo[3].append(y)
            geo[0] = int(sum(geo[2]) / len(geo[2]))
            geo[1] = int(sum(geo[3]) / len(geo[3]))
            newGeo = False
    if newGeo:
        geos.append([x, y, [x], [y]])


def pixelvalue_choice(p, treegroup, sizebias=False):
    if len(treegroup) > 0:
        if sizebias:
            return treegroup[int((p) * len(treegroup))]
        else:
            return treegroup[int((p) * len(treegroup))]
    else:
        return None


input_featureimage = Image.open(input_imagefile_name)
imshape = input_featureimage.size
input_pixels = input_featureimage.load()

output_featureimage = Image.new('RGB', imshape, color=(0, 0, 0))
output_pixels = output_featureimage.load()
print("Image shape is:", imshape, input_featureimage)
new_features = []
for x in range(imshape[0]):
    for y in range(imshape[1]):
        pix = input_pixels[x, y]
        # print (pix)
        cx = 8 * x + 4
        cz = 8 * y + 4
        if pix[0] > 0:  # snowy
            if random.random() < (red_probability * pix[0] / 255.0):
                feature = [pixelvalue_choice(random.random(), RED_FEATURES), cx, cz]
                new_features.append(feature)
        if pix[1] > 0:
            if random.random() < (green_probability * pix[1] / 255.0):
                feature = [pixelvalue_choice(random.random(), GREEN_FEATURES), cx, cz]
                new_features.append(feature)
        if pix[2] > 0:  # snowy
            if random.random() < (blue_probability * pix[2] / 255.0):
                feature = [pixelvalue_choice(random.random(), BLUE_FEATURES), cx, cz]
                new_features.append(feature)
        if len(pix) >= 4:
            if pix[3] < 10:
                clusterGeos(x, y)

for geo in geos:
    cx = 8 * geo[0] + 4
    cz = 8 * geo[1] + 4
    new_features.append(['geovent', cx, cz])
    print("Placing geovent at:", cx, cz)

outf = open('feature_placer_springrts_featureplacement.lua', 'w')
typecounts = {}
for featurename, cx, cz in new_features:
    if feature[0] is not None:
        output_pixel = [0, 0, 0]
        if featurename in RED_FEATURES:
            output_pixel[0] = 255 - RED_FEATURES.index(featurename)
        if featurename in GREEN_FEATURES:
            output_pixel[1] = 255 - GREEN_FEATURES.index(featurename)
        if featurename in BLUE_FEATURES:
            output_pixel[2] = 255 - BLUE_FEATURES.index(featurename)
        output_pixels[int(cx / 8), int(cz / 8)] = tuple(output_pixel)
        # { name = 'ad0_senegal_2', x = 7884, z = 228, rot = "3852" ,scale = 1.000000 },
        outf.write(outputline % (featurename, cx, cz, random.randint(-32700, 32700)) + '\n')
        typecounts[featurename] = 1 if featurename not in typecounts else typecounts[featurename] + 1

# print ('\n'.join(['%s:%d'%(ftype,fcount) for ftype, fcount in typecounts.items()]))
print('\n'.join(['%s:%d' % (ftype, typecounts[ftype]) for ftype in sorted(typecounts.keys())]))
outf.close()
print("total trees=", len(new_features))

output_featureimage.save(input_imagefile_name + "_featuremapout.bmp")
