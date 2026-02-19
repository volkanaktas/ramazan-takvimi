"""
Ramazan Takvimi – Uygulama Giriş Noktası
Python 3.12 + PySide6 + QML
"""

import os
import sys

# Yüksek DPI desteği (Windows)
os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")

from PySide6.QtWidgets import QApplication      # QFileDialog için QApplication gerekli
from PySide6.QtGui import QIcon, QFontDatabase
from PySide6.QtQml import QQmlApplicationEngine

from app.settings_manager import SettingsManager
from app.cache_manager import CacheManager
from app.app_controller import AppController
from app.theme_provider import ThemeProvider
from app.music_player import MusicPlayer
from app.location_controller import LocationController
from models.verse_model import VerseModel
from models.hadith_model import HadithModel
from models.prayer_model import PrayerModel
from models.meal_model import MealModel
from models.weather_model import WeatherModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def register_fonts() -> None:
    font_dir = os.path.join(BASE_DIR, "qml", "fonts")
    for font_file in ["Amiri-Regular.ttf", "NotoSans-Regular.ttf"]:
        path = os.path.join(font_dir, font_file)
        if os.path.isfile(path):
            QFontDatabase.addApplicationFont(path)


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Ramazan Takvimi")
    app.setOrganizationName("RamazanApp")
    app.setOrganizationDomain("ramazan.app")

    icon_path = os.path.join(BASE_DIR, "assets", "icon.ico")
    if os.path.isfile(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    register_fonts()

    settings = SettingsManager()
    cache = CacheManager()

    font_scale = settings.get("font_scale", "medium")
    theme = ThemeProvider(scale=font_scale)
    verse_model = VerseModel()
    hadith_model = HadithModel()
    prayer_model = PrayerModel()
    meal_model = MealModel()
    weather_model = WeatherModel()

    controller = AppController(
        verse_model=verse_model,
        hadith_model=hadith_model,
        prayer_model=prayer_model,
        meal_model=meal_model,
        settings=settings,
        cache=cache,
        theme=theme,
        weather_model=weather_model,
    )

    # Müzik çalar
    music_player = MusicPlayer()
    music_player.setFolderPath(settings.get("music_folder", ""))
    music_player.setEnabled(settings.get("music_enabled", False))

    # Konum kontrolcüsü
    location_controller = LocationController(settings=settings, cache=cache)

    engine = QQmlApplicationEngine()

    try:
        import resources_rc  # noqa: F401
    except ImportError:
        pass

    ctx = engine.rootContext()
    ctx.setContextProperty("Theme", theme)
    ctx.setContextProperty("appController", controller)
    ctx.setContextProperty("verseModel", verse_model)
    ctx.setContextProperty("hadithModel", hadith_model)
    ctx.setContextProperty("prayerModel", prayer_model)
    ctx.setContextProperty("mealModel", meal_model)
    ctx.setContextProperty("musicPlayer", music_player)
    ctx.setContextProperty("locationController", location_controller)
    ctx.setContextProperty("weatherModel", weather_model)

    qml_file = os.path.join(BASE_DIR, "qml", "main.qml")
    engine.load(qml_file)

    if not engine.rootObjects():
        print("HATA: QML yüklenemedi.", file=sys.stderr)
        return 1

    ret = app.exec()

    # Çıkışta müzik ve ayar durumunu kaydet
    settings.set("music_folder", music_player.folder)
    settings.set("music_enabled", music_player.isEnabled)
    return ret


if __name__ == "__main__":
    sys.exit(main())
