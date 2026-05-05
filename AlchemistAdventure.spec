# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import os

datas = []
binaries = []
hiddenimports = []

# Kumpulkan semua file mediapipe (library deteksi tangan)
tmp_ret = collect_all('mediapipe')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# Kumpulkan semua file cv2 (OpenCV)
tmp_ret2 = collect_all('cv2')
datas += tmp_ret2[0]; binaries += tmp_ret2[1]; hiddenimports += tmp_ret2[2]

# Sertakan folder assets (musik, gambar background, dll)
datas += [('assets', 'assets')]

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports + [
        'pygame', 'cv2', 'mediapipe',
        'engine.camera_tracker', 'engine.physics', 'engine.particles',
        'entities.player', 'entities.items', 'entities.enemies',
        'levels.level_manager',
        'ui.dashboard', 'ui.quiz_system', 'ui.screens',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AlchemistAdventure',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,   # False = tidak tampilkan jendela konsol hitam saat dijalankan
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AlchemistAdventure',
)
