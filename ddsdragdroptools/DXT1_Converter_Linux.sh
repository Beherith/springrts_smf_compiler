#!/bin/bash
##todo chmods
./dragon-dxt1 --target | while read -r input 
do
   ##   ./"nvtt_export.exe" --output "$(echo "$input"|sed -r "s/.+\/(.+)\..+/\1/").dds" --save-flip-y --mip-filter 0 --quality 3 --format bc1 "$(echo "$input"|sed -e 's/%20/ /g;s/^.......//g;s/^/z:/g')"
        ./magick convert "$(echo "$input"|sed -e 's/%20/ /g')" -flip -define dds:compression=dtx1 -define dds:fast-mipmaps=false -set filename:base "%[basename]" "%[filename:base].dds"
done
