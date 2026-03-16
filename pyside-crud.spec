# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_all

# PyInstaller runs the spec file with the working directory set to the spec location
# so we can use the current directory as the project root
block_cipher = None

# Collect all files from src package
datas = []
binaries = []
hiddenimports = []

# Collect all src modules
tmp_datas, tmp_binaries, tmp_hiddenimports = collect_all('src')
datas.extend(tmp_datas)
binaries.extend(tmp_binaries)
hiddenimports.extend(tmp_hiddenimports)

# Collect external dependencies
tmp_datas, tmp_binaries, tmp_hiddenimports = collect_all('PySide6')
datas.extend(tmp_datas)
binaries.extend(tmp_binaries)
hiddenimports.extend(tmp_hiddenimports)

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
    hiddenimports=[
        # Package __init__ files
        'src',
        'src.config',
        'src.presenters',
        'src.models',
        'src.views',
        'src.services',
        'src.utils',
        'src.mvp',
        
        # Config modules
        'src.config.config_manager',
        
        # Presenter modules
        'src.presenters.config_presenter',
        'src.presenters.bucket_browser_presenter',
        
        # Model modules
        'src.models.bucket_browser_model',
        'src.models.bucket_object',
        
        # View modules
        'src.views.bucket_browser_view',
        'src.views.setup_wizard_view',
        'src.views.settings_panel_view',
        'src.views.folder_first_sort_proxy_model',
        
        # Service modules
        'src.services.s3_service',
        'src.services.s3_errors',
        
        # Utility modules
        'src.utils.styles',
        'src.utils.file_icons',
        
        # MVP modules
        'src.mvp.base_model',
        'src.mvp.base_view',
        'src.mvp.base_presenter',
        'src.mvp.contracts',
        
        # Other modules
        'src.main_window',
        
        # External dependencies
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtWidgets',
        'PySide6.QtGui',
        'boto3',
        'botocore',
        'dotenv',
        'jmespath',
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
