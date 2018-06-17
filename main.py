from gooey import Gooey, GooeyParser

from smf_map_tools import compileSMF


def start(args):
    compileSMF(args)



@Gooey(dump_build_config=True, program_name="Spring SMF Tools")
def main():
    desc = "Spring RTS SMF map compiler/decompiler\nby Beherith (mysterme@gmail.com).\n" \
           "You must select at least a texture and a heightmap for compilation"

    help_msg = '''
       -k <feature placement file>,  --featureplacement <feature placement
          file>
         (value required)  A special text file defining the placement of each
         feature. (Default: fp.txt). See README.txt for details. The default
         format specifies it to have each line look like this (spacing is
         strict)

         { name = 'agorm_talltree6', x = 224, z = 3616, rot = "0" }

       -j <feature list file>,  --featurelist <feature list file>
         (value required)  A file with the name of one feature on each line.
         (Default: fs.txt). See README.txt for details.

         Specifying a number from 32767 to -32768 next to the feature name will
         tell mapconv how much to rotate the feature. specifying -1 will rotate
         it randomly.

         Example line from fs.txt

         btreeblo_1 -1

         btreeblo 16000

       -f <featuremap image>,  --featuremap <featuremap image>
         (value required)  Feature placement file, xsize by ysize. See
         README.txt for details. Green 255 pixels are geo vents, blue is grass,
         green 201-215 is default trees, red 255-0 correspont each to a line in
         fs.txt.

       -r <randomrotate>,  --randomrotate <randomrotate>
         (value required)  rotate features randomly, the first r features in
         featurelist (fs.txt) get random rotation, default 0

       -s,  --justsmf
         Just create smf file, dont make smt

       -l,  --lowpass
         Lowpass filters the heightmap

       -q,  --use_nvcompress
         Use NVCOMPRESS.EXE tool for ultra fast CUDA compression. Needs Geforce
         8 or higher nvidia card.

       -i,  --invert
         Flip the height map image upside-down on reading.

       -z <texcompress program>,  --texcompress <texcompress program>
         (value required)  Name of companion program texcompress from current
         working directory.

       -c <compression>,  --compress <compression>
         (value required)  How much we should try to compress the texture map.
         Default 0.8, lower -> higher quality, larger files.

       -x <max height>,  --maxheight <max height>
         (required)  (value required)  What altitude in spring the max(0xff or
         0xffff) level of the height map represents.

       -n <min height>,  --minheight <min height>
         (required)  (value required)  What altitude in spring the min(0) level
         of the height map represents.

       -o <output .smf>,  --outfile <output .smf>
         (value required)  The name of the created map file. Should end in
         .smf. A tilefile (extension .smt) is also created.

       -e <tile file>,  --externaltilefile <tile file>
         (value required)  External tile file that will be used for finding
         tiles. Tiles not found in this will be saved in a new tile file.

       -g <Geovent image>,  --geoventfile <Geovent image>
         (value required)  The decal for geothermal vents; appears on the
         compiled map at each vent. (Default: geovent.bmp).

       -y <typemap image>,  --typemap <typemap image>
         (value required)  Type map to use, uses the red channel to decide
         type. types are defined in the .smd, if this argument is skipped the
         map will be all type 0

       -m <metalmap image>,  --metalmap <metalmap image>
         (required)  (value required)  Metal map to use, red channel is amount
         of metal. Resized to xsize / 2 by ysize / 2.

       -a <heightmap file>,  --heightmap <heightmap file>
         (required)  (value required)  Input heightmap to use for the map, this
         should be in 16 bit raw format (.raw extension) or an image file. Must
         be xsize*64+1 by ysize*64+1.

       -t <texturemap file>,  --intex <texturemap file>
         (required)  (value required)  Input bitmap to use for the map. Sides
         must be multiple of 1024 long. xsize, ysize determined from this file:
         xsize = intex width / 8, ysize = height / 8.

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       -v,  --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Converts a series of image files to a Spring map. This just creates the
       .smf and .smt files. You also need to write a .smd file using a text
       editor.
    '''

    parser = GooeyParser(description=desc)

    parser.add_argument('-x', '--maxheight',
                        help='<max height> (required) What altitude in spring\n'
                             'the max(0xff for 8 bit images or 0xffff for 16bit images)\n'
                             'level of the height map represents',
                        default=100.0, type=float)
    parser.add_argument('-n', '--minheight',
                        help=' <min height> (required) What altitude in spring\n'
                             'the minimum level (0) of the height map represents',
                        default=-50.0, type=float)
    parser.add_argument('-o', '--outfile',
                        help=' <output mapname.smf> (required) The name of the created map file.\n'
                             'Should end in .smf. A tilefile (extension .smt) is also created,\n'
                             ' this name may contain spaces',
                        default='', type=str,  widget="FileSaver")
    parser.add_argument('-m', '--metalmap',
                        help='<metalmap.bmp> Metal map to use, red channel is amount of metal.'
                             'Resized to xsize / 2 by ysize / 2.',
                        type=str,  widget="FileChooser")
    parser.add_argument('-t', '--intex',
                        help='<texturemap.bmp> (required) Input bitmap to use for the map.'
                             'Sides must be multiple of 1024 long. Xsize and Ysize are determined from this file;'
                             'xsize = intex width / 8, ysize = height / 8',
                        default='', type=str,  widget="FileChooser")
    parser.add_argument('-a', '--heightmap',
                        help='<heightmap file> (required) Input heightmap to use for the map,'
                             'this should be 16 bit greyscale PNG image or a 16bit intel byte order single channel'
                             '.raw image. Must be xsize*64+1 by ysize*64+1',
                        default='', type=str, widget="FileChooser")

    parser.add_argument('-g', '--geoventfile',
                        help='<geovent.bmp> The decal for geothermal vents; appears on the compiled map at each vent.'
                             'Custom geovent decals should use all white as transparent,'
                             'clear this if you do not wish to have geovents drawn.',
                        default='geovent.bmp', type=str,  widget="FileChooser")
    parser.add_argument('-y', '--typemap',
                        help='<typemap.bmp> Type map to use, uses the red channel to decide terrain type.'
                             ' types are defined in the .smd, if this argument is skipped the entire map will TERRAINTYPE0',
                        type=str)
    # parser.add_argument('-c', '--compress', help =  '<compression> How much we should try to compress the texture map. Values between [0;1] lower values make higher quality, larger files. [NOT IMPLEMENTED YET]',  default = 0.0, type = float )

    # parser.add_argument('-i', '--invert', help = 'Flip the height map image upside-down on reading.', default = False, action='store_true' )
    # parser.add_argument('-l', '--lowpass', help = '<int kernelsize> Smoothes the heightmap with a gaussian kernel size specified', default = 0, type=int)

    parser.add_argument('-k', '--featureplacement',
                        help='<featureplacement.lua> A feature placement text file defining the placement of each feature. (Default: fp.txt). See README.txt for details. The default format specifies it to have each line look like this: \n { name = \'agorm_talltree6\', x = 224, z = 3616, rot = "0" , scale = 1.0} \n the [scale] argument currently does nothing in the engine. ',
                        type=str)
    parser.add_argument('-j', '--featurelist',
                        help='<feature_list_file.txt> (required if featuremap image is specified) A file with the name of one feature on each line. Specifying a number from 32767 to -32768 next to the feature name will tell mapconv how much to rotate the feature. specifying -1 will rotate it randomly.',
                        type=str)
    parser.add_argument('-f', '--featuremap',
                        help=' <featuremap.bmp> Feature placement image, xsize by ysize. Green 255 pixels are geo vents, blue is grass, green 201-215 are engine default trees, red 255-0 each correspond to a line in --featurelist',
                        type=str)
    parser.add_argument('-p', '--minimap',
                        help=' <minimap.bmp> If specified, will override generating a minimap from the texture file (intex) with the specified file. Must be 1024x1024 size.',
                        type=str)
    parser.add_argument('-r', '--grassmap',
                        help=' <grassmap.bmp> If specified, will override the grass specified in the featuremap. Expects an xsize/4 x ysize/4 sized bitmap, all values that are not 0 will result in grass',
                        type=str)

    # parser.add_argument('-s', '--justsmf', help = 'Just create smf file, dont make tile file (for quick recompilations)', default = 0, type=int)
    parser.add_argument('-u', '--linux',
                        help='Check this if you are running linux and wish to use imagemagicks convert utility instead of nvdxt.exe',
                        default=False, action='store_true')
    parser.add_argument('-v', '--nvdxt_options', help='NVDXT compression options ', default='-Sinc -quality_highest')
    parser.add_argument('-q', '--quick', help='Quick compilation (lower texture quality)', action='store_true')
    parser.add_argument('-d', '--decompile',
                        help='Decompiles a map to everything you need to recompile it', type=str, widget="FileChooser")

    args = parser.parse_args()


    start(args)



if __name__ == '__main__':
    main()
