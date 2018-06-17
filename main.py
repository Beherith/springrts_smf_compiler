from gooey import Gooey, GooeyParser

from smf_map_tools import compileSMF


@Gooey(dump_build_config=True,
       program_name="Spring SMF Tools",
       required_cols=1,
       optional_cols=2,
       image_dir='images')
def main():
    desc = "Spring RTS SMF map compiler/decompiler"

    parser = GooeyParser(description=desc)

    parser.add_argument('-x', '--maxheight',
                        metavar='Max Height',
                        required=True,
                        help='What altitude in spring\n'
                             'the max(0xff for 8 bit images or 0xffff for 16bit images)\n'
                             'level of the height map represents',
                        default=100.0, type=float)
    parser.add_argument('-n', '--minheight',
                        metavar='Min Height',
                        required=True,
                        help='What altitude in spring\n'
                             'the minimum level (0) of the height map represents',
                        default=-50.0, type=float)
    parser.add_argument('-o', '--outfile',
                        metavar='Output File',
                        required=True,
                        help='The name of the created map file.\n'
                             'Should end in .smf. A tilefile (extension .smt) is also created,\n'
                             'this name may contain spaces',
                        default='',
                        widget="FileSaver")
    parser.add_argument('-m', '--metalmap',
                        metavar='Metal Map',
                        help='Metal map to use, red channel is amount of metal.\n'
                             'Resized to xsize / 2 by ysize / 2.',
                        widget="FileChooser")
    parser.add_argument('-t', '--intex',
                        metavar='Map Texture',
                        required=True,
                        help='Input bitmap to use for the map.\n'
                             'Sides must be multiple of 1024 long.\n'
                             'Xsize and Ysize are determined from this file;\n'
                             'xsize = intex width / 8, ysize = height / 8',
                        default='',
                        widget="FileChooser")
    parser.add_argument('-a', '--heightmap',
                        metavar='Height Map Texture',
                        required=True,
                        help='Input heightmap to use for the map,\n'
                             'this should be 16 bit greyscale PNG image\n'
                             'or a 16bit intel byte order single channel\n'
                             '.raw image. Must be xsize*64+1 by ysize*64+1',
                        default='',
                        widget="FileChooser")

    parser.add_argument('-g', '--geoventfile',
                        metavar='Geovent Texture',
                        help='The decal for geothermal vents; appears on the compiled map at each vent.\n'
                             'Custom geovent decals should use all white as transparent,\n'
                             'clear this if you do not wish to have geovents drawn.',
                        default='',
                        widget="FileChooser")
    parser.add_argument('-y', '--typemap',
                        metavar='Type Map',
                        help='Type map to use, uses the red channel to decide terrain type.\n'
                             'types are defined in the .smd, if this argument is skipped\n'
                             'the entire map will TERRAINTYPE0')
    # parser.add_argument('-c', '--compress', help =  '<compression> How much we should try to compress the texture map. Values between [0;1] lower values make higher quality, larger files. [NOT IMPLEMENTED YET]',  default = 0.0, type = float )

    # parser.add_argument('-i', '--invert', help = 'Flip the height map image upside-down on reading.', default = False, action='store_true' )
    # parser.add_argument('-l', '--lowpass', help = '<int kernelsize> Smoothes the heightmap with a gaussian kernel size specified', default = 0, type=int)

    parser.add_argument('-k', '--featureplacement',
                        metavar='Feature Placement',
                        help='A feature placement text file defining the placement of each feature.\n'
                             '(Default: fp.txt). See README.txt for details.\n'
                             'The default format specifies it to have each line look like this: \n'
                             '{ name = \'agorm_talltree6\', x = 224, z = 3616, rot = "0" , scale = 1.0} \n'
                             'the [scale] argument currently does nothing in the engine. ')
    parser.add_argument('-j', '--featurelist',
                        metavar='Feature List',
                        help='(required if featuremap image is specified)\n'
                             'A file with the name of one feature on each line.\n'
                             'Specifying a number from 32767 to -32768 next to the feature name\n'
                             'will tell mapconv how much to rotate the feature.\n'
                             'specifying -1 will rotate it randomly.')
    parser.add_argument('-f', '--featuremap',
                        metavar='Feature Map Image',
                        help='Feature placement image, xsize by ysize. Green 255 pixels are geo vents, blue is grass,\n'
                             'green 201-215 are engine default trees, red 255-0 each correspond to a line in --featurelist')
    parser.add_argument('-p', '--minimap',
                        metavar='Mini Map',
                        help='If specified, will override generating a minimap from the texture file (intex) with the specified file.\n'
                             'Must be 1024x1024 size.')
    parser.add_argument('-r', '--grassmap',
                        metavar='Grass Map Texture',
                        help='If specified, will override the grass specified in the featuremap.\n'
                             'Expects an xsize/4 x ysize/4 sized bitmap, all values that are not 0 will result in grass')

    # parser.add_argument('-s', '--justsmf', help = 'Just create smf file, dont make tile file (for quick recompilations)', default = 0, type=int)
    parser.add_argument('-u', '--linux',
                        metavar="Linux",
                        help='Check this if you are running linux and wish to use imagemagicks convert utility instead of nvdxt.exe',
                        default=False,
                        widget="CheckBox")
    parser.add_argument('-v', '--nvdxt_options',
                        metavar="'NVDXT",
                        help='NVDXT compression options ',
                        default='-Sinc -quality_highest')
    parser.add_argument('-q', '--quick',
                        metavar="Quick",
                        default=False,
                        help='Quick compilation (lower texture quality)'
                        , action='store_true')
    parser.add_argument('-d', '--decompile',
                        metavar="Decompile",
                        help='Decompiles a map to everything you need to recompile it',
                        widget="FileChooser")

    args = parser.parse_args()

    compileSMF(args)


if __name__ == '__main__':
    main()
