
ECHO "Drag And drop .TGA files onto this to convert them to DDS (while flipping them and inverting G channel"

nvdxt.exe -dxt5 -Sinc -quality_highest -flip -contrast 1.0 -1.0 1.0 1.0 -file "%~1"
