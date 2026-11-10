# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:/Projeto_Blog_Comprenolink/Relatorios_Diarios_Anuncios/programas_fontes_python/3_relatorio_acessos_anuncios.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=['6_verificar_anuncios'],
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
    a.binaries,
    a.datas,
    [],
    name='1_relatorio_acessos_anuncios',
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
)
