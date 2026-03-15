# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Get the project root (directory where this spec file is located)
spec_file = os.path.abspath(__file__)
project_root = Path(os.path.dirname(spec_file))

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # Include any data files if needed
    ],
    hiddenimports=[
        'src',
        'src.config',
        'src.config.config_manager',
        'src.presenters',
        'src.presenters.config_presenter',
        'src.presenters.bucket_browser_presenter',
        'src.models',
        'src.models.bucket_browser_model',
        'src.views',
        'src.views.bucket_browser_view',
        'src.services',
        'src.services.s3_service',
        'src.utils',
        'src.utils.styles',
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtWidgets',
        'PySide6.QtGui',
        'boto3',
        'botocore',
        'python-dotenv',
    ],
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
