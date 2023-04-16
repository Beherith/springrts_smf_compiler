@ECHO OFF
@ECHO Drag And drop IMAGE (.PNG,.TGA,.BMP) files onto this from anywhere to convert them to DDS without flipping them, placing the results next to the original file.
@ECHO U8888 uncompressed sinc sharpened mips are best
@ECHO Make sure nvdxt.exe and Freeimage.dll are next to this script
@ECHO by [teh]Beherith (mysterme@gmail.com) https://github.com/Beherith/springrts_smf_compiler

@REM https://stackoverflow.com/questions/19835849/batch-script-iterate-through-arguments/19837690#19837690

@REM https://docs.microsoft.com/en-us/windows/win32/direct3d10/d3d10-graphics-programming-guide-resources-block-compression

setlocal enabledelayedexpansion

for %%x in (%*) do (
   echo .
   echo "%~dp0nvdxt.exe" -file "%%~x" -u8888 -Sinc -quality_highest -output "%%~nx.dds"
   @REM "%~dp0nvdxt.exe" -file "%%~x" -u8888 -Sinc -quality_highest -output "%%~nx.dds"
   "%~dp0nvdxt.exe" -file "%%~x" -u8888 -Sinc -output "%%~nx.dds"
@REM   "%~dp0nvtt_export.exe" --output "%%~nx.dds" --save-flip-y --mip-filter 0 --quality 3 --format bc3 "%%~x"
)

echo .

@REM old version with single command line arg: "%~dp0nvtt_export.exe" --output "%~n1.dds" --save-flip-y --mip-filter 0 --quality 2 --format bc3 "%~1"

@ECHO "Press any key to close window, automatically closing in 5 secons"
timeout /t 5
