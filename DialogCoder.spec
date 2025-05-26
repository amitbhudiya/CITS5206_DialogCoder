# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['launch.py'],
    pathex=[
        'src', 
        '.',  
    ],
    binaries=[],
    datas=[
        ('app', 'app'), 
        ('src', 'src'),  
        ('requirements.txt', '.'), 
    ],
    hiddenimports=[
        'streamlit',
        'pandas',
        'matplotlib',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'streamlit.runtime.scriptrunner.script_runner',
        'streamlit.runtime.stats',
        'streamlit.runtime.caching',
        'streamlit.runtime.legacy_caching',
        'file_processor', 
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
    name='DialogCoder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app/assets/icon.ico' if os.path.exists('app/assets/icon.ico') else None,
) 