# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_all

# Add the current directory to Python path so PyInstaller can find src
sys.path.insert(0, os.getcwd())

block_cipher = None

# Collect external dependencies
datas = []
binaries = []
hiddenimports = []

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
    pathex=[os.getcwd(), os.path.join(os.getcwd(), 'src')],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        # Explicitly list all src modules
        'src',
        'src.config',
        'src.config.config_manager',
        'src.presenters',
        'src.presenters.config_presenter',
        'src.presenters.bucket_browser_presenter',
        'src.models',
        'src.models.bucket_browser_model',
        'src.models.bucket_object',
        'src.views',
        'src.views.bucket_browser_view',
        'src.views.setup_wizard_view',
        'src.views.settings_panel_view',
        'src.views.folder_first_sort_proxy_model',
        'src.services',
        'src.services.s3_service',
        'src.services.s3_errors',
        'src.utils',
        'src.utils.styles',
        'src.utils.file_icons',
        'src.mvp',
        'src.mvp.base_model',
        'src.mvp.base_view',
        'src.mvp.base_presenter',
        'src.mvp.contracts',
        'src.main_window',
        # External deps
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
    console=True,  # Changed to True temporarily to see errors
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onefile=True,
)
