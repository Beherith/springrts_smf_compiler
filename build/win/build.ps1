python3 -m PyInstaller `
    --noconfirm --onefile --log-level=WARN --noupx `
    --icon icon.ico `
    --paths '../../src' `
    --distpath '../../bin' `
    --noconfirm `
    '../../src/pymapconv.py'
