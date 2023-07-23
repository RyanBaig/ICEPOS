# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:/Users/Hp/PycharmProjects/ICEPOS/icepos.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/Hp/PycharmProjects/ICEPOS/background.png', '.'), ('C:/Users/Hp/PycharmProjects/ICEPOS/formatted_image.png', '.'), ('C:/Users/Hp/PycharmProjects/ICEPOS/ice-answers.db', '.'), ('C:/Users/Hp/PycharmProjects/ICEPOS/rates.json', '.'), ('C:/Users/Hp/PycharmProjects/ICEPOS/rates_creation.py', '.'), ('C:/Users/Hp/PycharmProjects/ICEPOS/zipcodes_creation.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='icepos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\Hp\\PycharmProjects\\ICEPOS\\icon.ico'],
)
