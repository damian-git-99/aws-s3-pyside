# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_submodules, collect_all

# PyInstaller runs the spec file with the working directory set to the spec location
# so we can use the current directory as the project root
block_cipher = None

# Collect all submodules from src package automatically
hiddenimports = collect_submodules('src')

# Collect external dependencies
datas = []
binaries = []

# Collect PySide6
tmp_datas, tmp_binaries, tmp_hiddenimports = collect_all('PySide6')
datas.extend(tmp_datas)
binaries.extend(tmp_binaries)
hiddenimports.extend(tmp_hiddenimports)

# Collect boto3 and botocore
tmp_datas, tmp_binaries, tmp_hiddenimports = collect_all('boto3')
datas.extend(tmp_datas)
binaries.extend(tmp_binaries)
hiddenimports.extend(tmp_hiddenimports)

tmp_datas, tmp_binaries, tmp_hiddenimports = collect_all('botocore')
datas.extend(tmp_datas)
binaries.extend(tmp_binaries)
hiddenimports.extend(tmp_hiddenimports)

a = Analysis(
    ['src/main.py'],
    pathex=[os.getcwd()],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='pyside-crud',
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
    onefile=True,
)
