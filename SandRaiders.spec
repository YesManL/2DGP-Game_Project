# -*- mode: python ; coding: utf-8 -*-
import os
import sys

# SDL2 DLL 경로 찾기
try:
    import sdl2dll
    sdl2_dll_path = sdl2dll.get_dllpath()
except:
    # Python 3.10 경로 기준
    sdl2_dll_path = r'C:\Users\ht515\AppData\Local\Programs\Python\Python310\lib\site-packages\sdl2dll\dll'

block_cipher = None

# SDL2 DLL 파일들 수집
sdl2_binaries = []
if os.path.exists(sdl2_dll_path):
    for file in os.listdir(sdl2_dll_path):
        if file.endswith('.dll'):
            sdl2_binaries.append((os.path.join(sdl2_dll_path, file), '.'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=sdl2_binaries,
    datas=[
        ('01.캐릭터&몬스터&애니메이션', '01.캐릭터&몬스터&애니메이션'),
        ('02.배경&프랍', '02.배경&프랍'),
        ('03.아이템&아이콘', '03.아이템&아이콘'),
        ('04.GUI', '04.GUI'),
        ('05.VFX', '05.VFX'),
        ('99.etc', '99.etc'),
        ('SFX', 'SFX'),
    ],
    hiddenimports=['sdl2', 'sdl2.ext', 'sdl2dll'],
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
    name='SandRaiders',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 콘솔 창 숨기기
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 아이콘 파일이 있으면 경로 지정
)


