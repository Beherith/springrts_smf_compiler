#!/bin/bash
chmod +x dragon-dxt5 magick nvtt_export.exe
./dragon-dxt5 --target | while read -r input 
do
    ##  ./"nvtt_export.exe" --output "$(echo "$input"|sed -r "s/.+\/(.+)\..+/\1/").dds" --save-flip-y --mip-filter 0 --quality 3 --format bc3 "$(echo "$input"|sed -e 's/%20/ /g;s/^.......//g;s/^/z:/g')"
        ./magick convert "$(echo "$input"|sed -e 's/%20/ /g')" -flip -define dds:compression=dtx5 -define dds:fast-mipmaps=false -set filename:base "%[basename]" "%[filename:base].dds"
done
