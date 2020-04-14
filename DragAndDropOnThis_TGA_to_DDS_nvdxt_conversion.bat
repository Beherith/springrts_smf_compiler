
ECHO "Drag And drop .TGA files onto this to convert them to DDS (while flipping them and inverting G channel"
ECHO "Because TGA has bottom left origin, while DDS has top right, and this top-down flipping needs the Green (Y) channel inverted"

nvdxt.exe -dxt5 -Sinc -quality_highest -flip -contrast 1.0 -1.0 1.0 1.0 -file "%~1"
