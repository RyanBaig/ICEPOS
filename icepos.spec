# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/home/ryanbaig/Desktop/Projects/Python/ICEPOS/icepos.py'],
    pathex=[],
    binaries=[],
    datas=[('/home/ryanbaig/Desktop/Projects/Python/ICEPOS/assets', 'assets/'), ('/home/ryanbaig/Desktop/Projects/Python/ICEPOS/custom_widgets.py', '.'), ('/home/ryanbaig/Desktop/Projects/Python/ICEPOS/functions.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='icepos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['/home/ryanbaig/Desktop/Projects/Python/ICEPOS/assets/images/icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='icepos',
)
