# -*- mode: python ; coding: utf-8 -*-

import configparser


# load app info
with open('app/app_info.py') as f:
    file_content = '[dummy_section]\n' + f.read()

config = configparser.ConfigParser()
config.read_string(file_content)

section = config['dummy_section']

app_name = section['AppName'].replace('"', '')
icon_file = str(section['AppIconPath'] + '/' + section['AppIconName']).replace('"', '')


a = Analysis(
    ['app/main.py'],
    pathex=['./app'],
    binaries=[
        ('.venv/Scripts/AutoHotkey.exe', '.')
    ],
    datas=[
        ('app/resources', 'resources'),
        ('app/plugins/*.zip', 'plugins'),
        ('app/plugins/devices/*.zip', 'plugins/devices'),
    ],
    hiddenimports=[
        'pygame',
        'pynput',
        'ahk',
        'numpy',
        'sounddevice',
        'qtpy.QtWebSockets',
        'qtpy.shiboken',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)

pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=None
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    icon=icon_file,
    console=False 
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name=app_name
)
