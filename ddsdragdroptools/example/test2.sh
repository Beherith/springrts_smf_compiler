#!/bin/bash
./dragon-dxt1 --target | while read -r input 
do
      ./"nvtt_export.exe" --output "$(echo "$input"|sed -r "s/.+\/(.+)\..+/\1/").dds" --save-flip-y --mip-filter 0 --quality 3 --format bc1 "$(echo "$input"|sed -e 's/%20/ /g;s/^.......//g;s/^/z:/g')"
   ##     ./magick convert "$(echo "$input"|sed -e 's/%20/ /g')" -define dd:mipmaps=1 -define dds:compression=dtx1 -set filename:base "%[basename]" "%[filename:base].dds"
done
