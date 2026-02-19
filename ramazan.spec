# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec dosyası – Ramazan Takvimi
# pyinstaller ramazan.spec ile çalıştırın.

import os

BASE = os.path.abspath('.')

a = Analysis(
    ['main.py'],
    pathex=[BASE],
    binaries=[],
    datas=[
        ('qml',        'qml'),
        ('assets',     'assets'),
        ('config.json', '.'),
    ],
    hiddenimports=[
        # PySide6 modülleri
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'PySide6.QtQml',
        'PySide6.QtQuick',
        'PySide6.QtQuickControls2',
        'PySide6.QtMultimedia',
        'PySide6.QtNetwork',
        # Uygulama modülleri
        'app.app_controller',
        'app.cache_manager',
        'app.location_controller',
        'app.music_player',
        'app.settings_manager',
        'app.theme_provider',
        'models.hadith_model',
        'models.meal_model',
        'models.prayer_model',
        'models.verse_model',
        'models.weather_model',
        'services.api_client',
        'services.data_loader',
        'services.hadith_service',
        'services.location_service',
        'services.prayer_service',
        'services.quran_service',
        'services.weather_service',
        'data.static_hadiths',
        'data.static_meals',
        'data.static_verses',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter', 'matplotlib', 'numpy', 'scipy',
        'cv2', 'PIL', 'selenium', 'dlib',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RamazanTakvimi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,           # Konsol penceresi gösterme
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='assets/icon.ico',  # .ico eklenirse bu satırı etkinleştirin
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RamazanTakvimi',
)
