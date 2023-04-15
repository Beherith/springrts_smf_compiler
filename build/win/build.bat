python3 -m PyInstaller ^
    --noconfirm --onefile --log-level=WARN --noupx ^
    --icon icon.ico ^
    --paths '..\\..\\src' ^
    --distpath ..\\..\\bin ^
    --add-data '..\\..\\resources\\*:resources' ^
    --add-data '..\\..\\LICENSE:.' ^
    --add-binary 'nvdxt.exe:.' ^
    --noconfirm ^
    '..\\..\\src\\pymapconv.py'