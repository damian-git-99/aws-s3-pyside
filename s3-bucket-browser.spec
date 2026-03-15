# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# Siempre relativo al .spec, no al working directory
spec_dir = os.path.dirname(os.path.abspath(SPEC))
sys.path.insert(0, spec_dir)

from PyInstaller.utils.hooks import collect_all, collect_submodules

hiddenimports = collect_submodules('src')
hiddenimports += [
    'PySide6',
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'PySide6.QtNetwork',
    'boto3',
    'boto3.resources',
    'botocore',
    'botocore.exceptions',
    's3transfer',
    'jmespath',
    'dotenv',
    'urllib3',
    'certifi',
]

datas = []
binaries = []

try:
    from PyInstaller.utils.hooks import collect_data_files, collect_binaries
    pyside6_datas = collect_data_files('PySide6')
    pyside6_binaries = collect_binaries('PySide6')
    datas.extend(pyside6_datas)
    binaries.extend(pyside6_binaries)
except Exception:
    pass

a = Analysis(
    [os.path.join(spec_dir, 'src', 'main.py')],  # path absoluto al entry point
    pathex=[spec_dir],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[os.path.join(spec_dir, 'hooks', 'runtime_hook.py')],
    excludes=['test', 'tests'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='s3-bucket-browser',
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
)
