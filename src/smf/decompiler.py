import os


class SMFMapDecompiler:

    def __init__(self, filename, minimaponly=False, skiptexture=False):
        verbose = True
        self.savedir, self.filename = os.path.split(filename)
        self.basename = filename.rpartition('.')[0]
        self.smffile = open(os.path.join(self.savedir, filename), 'rb').read()
        self.SMFHeader = SMFHeader_struct.unpack_from(self.smffile, 0)

        self.magic = self.SMFHeader[0]  # ;      ///< "spring map file\0"
        self.version = self.SMFHeader[1]  # ;         ///< Must be 1 for now
        self.mapid = self.SMFHeader[
            2]  # ;           ///< Sort of a GUID of the file, just set to a random value when writing a map

        self.mapx = self.SMFHeader[3]  # ;            ///< Must be divisible by 128
        self.mapy = self.SMFHeader[4]  # ;            ///< Must be divisible by 128
        self.squareSize = self.SMFHeader[5]  # ;      ///< Distance between vertices. Must be 8
        self.texelPerSquare = self.SMFHeader[6]  # ;  ///< Number of texels per square, must be 8 for now
        self.tilesize = self.SMFHeader[7]  # ;        ///< Number of texels in a tile, must be 32 for now
        self.minHeight = self.SMFHeader[8]  # ;     ///< Height value that 0 in the heightmap corresponds to
        self.maxHeight = self.SMFHeader[9]  # ;     ///< Height value that 0xffff in the heightmap corresponds to

        self.heightmapPtr = self.SMFHeader[10]  # ;    ///< File offset to elevation data (short int[(mapy+1)*(mapx+1)])
        self.typeMapPtr = self.SMFHeader[11]  # ;      ///< File offset to typedata (unsigned char[mapy//2 * mapx//2])
        self.tilesPtr = self.SMFHeader[12]  # ;        ///< File offset to tile data (see MapTileHeader)
        self.minimapPtr = self.SMFHeader[
            13]  # ;      ///< File offset to minimap (always 1024*1024 dxt1 compresed data plus 8 mipmap sublevels)
        self.metalmapPtr = self.SMFHeader[14]  # ;     ///< File offset to metalmap (unsigned char[mapx//2 * mapy//2])
        self.featurePtr = self.SMFHeader[15]  # ;      ///< File offset to feature data (see MapFeatureHeader)

        self.numExtraHeaders = self.SMFHeader[16]  # ; ///< Numbers of extra headers following main header'''
        if verbose:
            attrs = vars(self)
            print_flushed(self.SMFHeader)

        print_flushed('Writing minimap')
        miniddsheaderstr = ([68, 68, 83, 32, 124, 0, 0, 0, 7, 16, 10, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0,
                             11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 0, 0, 0, 4, 0, 0, 0, 68, 88, 84, 49, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 8, 16, 64, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.minimap = self.smffile[self.minimapPtr:self.minimapPtr + MINIMAP_SIZE]
        if minimaponly:
            minimap_file = open(
                os.path.join(self.savedir, self.basename + '_%ix%i_mini.dds' % (self.mapx // 64, self.mapy // 64)),
                'wb')
        else:
            minimap_file = open(os.path.join(self.savedir, self.basename + '_mini.dds'), 'wb')
        for c in miniddsheaderstr:
            minimap_file.write(struct.pack('< B', c))
        minimap_file.write(self.minimap)
        minimap_file.close()

        if minimaponly:
            return

        self.heightmap = struct.unpack_from('< %iH' % ((1 + self.mapx) * (1 + self.mapy)), self.smffile,
                                            self.heightmapPtr)

        print_flushed('Writing heightmap PNG')
        heightmap_png_file = open(os.path.join(self.savedir, self.basename + '_height.png'), 'wb')
        heightmap_png_writer = png.Writer(width=1 + self.mapx, height=1 + self.mapy, greyscale=True, bitdepth=16)
        heightmap_per_rows = []
        for y in range(self.mapy + 1):
            heightmap_per_rows.append(self.heightmap[(self.mapx + 1) * y: (self.mapx + 1) * (y + 1)])
        heightmap_png_writer.write(heightmap_png_file, heightmap_per_rows)
        heightmap_png_file.close()

        print_flushed('Writing MetalMap')
        self.metalmap = struct.unpack_from('< %iB' % ((self.mapx // 2) * (self.mapy // 2)), self.smffile,
                                           self.metalmapPtr)
        metalmap_img = Image.new('RGB', (self.mapx // 2, self.mapy // 2), 'black')
        metalmap_img_pixels = metalmap_img.load()
        for x in range(metalmap_img.size[0]):
            for y in range(metalmap_img.size[1]):
                metal = self.metalmap[(metalmap_img.size[0]) * y + x]
                metalmap_img_pixels[x, y] = (metal, 0, 0)
        metalmap_img.save(self.basename + '_metal.bmp')

        print_flushed('Writing typemap')
        self.typemap = struct.unpack_from('< %iB' % ((self.mapx // 2) * (self.mapy // 2)), self.smffile,
                                          self.typeMapPtr)
        typemap_img = Image.new('RGB', (self.mapx // 2, self.mapy // 2), 'black')
        typemap_img_pixels = typemap_img.load()
        for x in range(typemap_img.size[0]):
            for y in range(typemap_img.size[1]):
                typep = self.typemap[(typemap_img.size[0]) * y + x]
                typemap_img_pixels[x, y] = (typep, 0, 0)
        typemap_img.save(self.basename + '_type.bmp')

        print_flushed('Writing grassmap')
        # vegmapoffset = SMFHeader_struct.size+ExtraHeader_struct.size+4
        for extraheader_index in range(self.numExtraHeaders):
            extraheader = ExtraHeader_struct.unpack_from(self.smffile,
                                                         extraheader_index * ExtraHeader_struct.size + SMFHeader_struct.size)
            if verbose:
                print_flushed('Extraheader:', extraheader, '(size, type, extraoffset)')
            extraheader_size, extraheader_type, extraoffset = extraheader
            # print_flushed ('ExtraHeader',extraheader)
            if extraheader_type == 1:  # grass
                # self.grassmap=struct.unpack_from('< %iB'%((self.mapx//4)*(self.mapy//4)),self.smffile,ExtraHeader_struct.size+SMFHeader_struct.size+extraheader_size)
                self.grassmap = struct.unpack_from('< %iB' % ((self.mapx // 4) * (self.mapy // 4)), self.smffile,
                                                   extraoffset)
                grassmap_img = Image.new('RGB', (self.mapx // 4, self.mapy // 4), 'black')
                grassmap_img_pixels = grassmap_img.load()

                grassValuemax = 0
                for x in range(grassmap_img.size[0]):
                    for y in range(grassmap_img.size[1]):
                        grass = self.grassmap[(grassmap_img.size[0]) * y + x]
                        grassValuemax = max(grassValuemax, grass)

                for x in range(grassmap_img.size[0]):
                    for y in range(grassmap_img.size[1]):
                        grass = self.grassmap[(grassmap_img.size[0]) * y + x]
                        if grassValuemax == 1 and grass == 1:
                            grass = 255
                        grassmap_img_pixels[x, y] = (grass, grass, grass)

                if grassValuemax == 0:
                    print_flushed("Map has no grass, but writing image anyway")
                elif grassValuemax == 1:
                    print_flushed("Map seems to have old style (binary) grass")
                else:
                    print_flushed("Map seems to have new style 0-254 awesome grass", grassValuemax)
                grassmap_img.save(self.basename + '_grass.bmp')

        # MapFeatureHeader is followed by numFeatureType zero terminated strings indicating the names
        # of the features in the map. Then follow numFeatures MapFeatureStructs.
        self.mapfeaturesheader = MapFeatureHeader_struct.unpack_from(self.smffile, self.featurePtr)
        if verbose:
            print_flushed('MapFeatureHeader=', self.mapfeaturesheader, '(numFeatureType, numFeatures)')
            print_flushed('MapTileHeader=', MapTileHeader_struct.unpack_from(self.smffile, self.tilesPtr),
                          '(numTileFiles, numTiles)')
            self.somelulz = self.smffile[self.tilesPtr - 10:self.tilesPtr + 30]
        self.numFeatureType, self.numFeatures = self.mapfeaturesheader
        self.featurenames = []
        featureoffset = self.featurePtr + MapFeatureHeader_struct.size
        while len(self.featurenames) < self.numFeatureType:
            featurename = unpack_null_terminated_string(self.smffile, featureoffset)
            self.featurenames.append(featurename)
            featureoffset += len(featurename) + 1  # cause of null terminator
            print_flushed(featurename)

        print_flushed('Features found in map definition', self.featurenames)
        feature_offset = self.featurePtr + MapFeatureHeader_struct.size + sum(
            [len(fname) + 1 for fname in self.featurenames])
        self.features = []
        for feature_index in range(self.numFeatures):
            feat = MapFeatureStruct_struct.unpack_from(self.smffile,
                                                       feature_offset + MapFeatureStruct_struct.size * feature_index)
            # print_flushed (feat)
            self.features.append(
                {'name': self.featurenames[feat[0]], 'x': feat[1], 'y': feat[2], 'z': feat[3], 'rotation': feat[4],
                 'relativeSize': feat[5], })
        # print_flushed (self.features[-1])
        print_flushed('Writing feature placement file')
        feature_file = open(os.path.join(self.savedir, self.basename + '_featureplacement.lua'), 'w')
        for feature in self.features:
            feature_file.write('{ name = \'%s\', x = %i, z = %i, rot = "%i" ,scale = %f },\n' % (
                feature['name'], feature['x'], feature['z'], feature['rotation'], feature['relativeSize']))
        feature_file.close()

        if not skiptexture:
            print_flushed('loading tile files')
            self.maptileheader = MapTileHeader_struct.unpack_from(self.smffile, self.tilesPtr)
            self.numtilefiles, self.numtiles = self.maptileheader
            self.tilefiles = []
            tileoffset = self.tilesPtr + MapTileHeader_struct.size
            for i in range(self.numtilefiles):
                numtilesinfile = struct.unpack_from('< i', self.smffile, tileoffset)[0]
                tileoffset += 4  # sizeof(int)
                tilefilename = unpack_null_terminated_string(self.smffile, tileoffset)
                tileoffset += len(tilefilename) + 1  # cause of null terminator
                self.tilefiles.append(
                    # [tilefilename, numtilesinfile, open(filename.rpartition('\\')[0] + '\\' + tilefilename, 'rb').read()])
                    [tilefilename, numtilesinfile, open(os.path.join(self.savedir, tilefilename), 'rb').read()])
                print_flushed(tilefilename, 'has', numtilesinfile, 'tiles')
            self.tileindices = struct.unpack_from('< %ii' % ((self.mapx // 4) * (self.mapy // 4)), self.smffile,
                                                  tileoffset)

            self.tiles = []
            for tilefile in self.tilefiles:
                tileFileHeader = TileFileHeader_struct.unpack_from(tilefile[2], 0)
                magic, version, numTiles, tileSize, compressionType = tileFileHeader
                # print_flushed (tilefile[0],': magic,version,numTiles,tileSize,compressionType',magic,version,numTiles,tileSize,compressionType)
                for i in range(numTiles):
                    self.tiles.append(struct.unpack_from('< %is' % (SMALL_TILE_SIZE), tilefile[2],
                                                         TileFileHeader_struct.size + i * SMALL_TILE_SIZE)[0])

            # TODO: Parallelize?
            print_flushed('Generating texture, this is very very slow (few minutes)')
            textureimage = Image.new('RGB', (self.mapx * 8, self.mapy * 8), 'black')
            textureimagepixels = textureimage.load()
            for ty in range(self.mapy // 4):
                # print_flushed ('row',ty)
                for tx in range(self.mapx // 4):
                    currtile = self.tiles[self.tileindices[(self.mapx // 4) * ty + tx]]
                    # print_flushed ('Tile',(self.mapx//4)*ty+tx)
                    # one tile is 32x32, and pythonDecodeDXT1 will need one 'row' of data, assume this is 8*8 bytes
                    for rows in range(8):
                        # print_flushed ("currtile",currtile)
                        dxdata = currtile[rows * 64:(rows + 1) * 64]
                        # print_flushed (len(dxdata),dxdata)
                        dxtrows = pythonDecodeDXT1(dxdata)  # decode in 8 block chunks
                        for x in range(tx * 32, (tx + 1) * 32):
                            for y in range(ty * 32 + 4 * rows, ty * 32 + 4 + 4 * rows):
                                # print_flushed (rows, tx,ty,x,y)
                                # print_flushed (dxtrows)
                                oy = (ty * 32 + 4 * rows)
                                textureimagepixels[x, y] = (
                                    ord(dxtrows[y - oy][3 * (x - tx * 32) + 0]),
                                    ord(dxtrows[y - oy][3 * (x - tx * 32) + 1]),
                                    ord(dxtrows[y - oy][3 * (x - tx * 32) + 2]))
            textureimage.save(self.basename + '_texture.bmp')
        infofile = open(os.path.join(self.savedir, self.basename + '_compilation_settings.txt'), 'w')

        infofile.write('-%s\n%s\n' % ('n', str(self.minHeight)))
        infofile.write('-%s\n%s\n' % ('x', str(self.maxHeight)))
        infofile.write('-%s\n%s\n' % ('o', self.basename + '_recompiled.smf'))
        infofile.write('-%s\n%s\n' % ('m', self.basename + '_metal.bmp'))
        infofile.write('-%s\n%s\n' % ('t', self.basename + '_texture.bmp'))
        infofile.write('-%s\n%s\n' % ('a', self.basename + '_height.png'))
        infofile.write('-%s\n%s\n' % ('g', ''))
        infofile.write('-%s\n%s\n' % ('y', self.basename + '_type.bmp'))
        infofile.write('-%s\n%s\n' % ('r', self.basename + '_grass.bmp'))
        infofile.write('-%s\n%s\n' % ('k', self.basename + '_featureplacement.lua'))

        infofile.close()

        print_flushed('Done, one final bit of important info: the maps maxheight is %i, while the minheight is %i' % (\
            self.maxHeight, self.minHeight))
