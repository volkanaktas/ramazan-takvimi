"""
Arka plan thread'inde veri yükleme.
3 kademeli fallback: API → Önbellek → Statik veri
"""

from datetime import date, timedelta

from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from services.quran_service import QuranService
from services.hadith_service import HadithService
from services.prayer_service import PrayerService
from app.cache_manager import CacheManager
from data.static_verses import get_verse_for_day
from data.static_hadiths import get_hadith_for_day
from data.static_meals import get_meal_for_day


class LoaderSignals(QObject):
    """QRunnable için sinyal taşıyıcı (QRunnable QObject'ten türeyemez)."""
    dataLoaded = Signal(dict)
    error = Signal(str)


class DataLoaderRunnable(QRunnable):
    """Belirtilen Ramazan günü için veri yükleyen QRunnable."""

    def __init__(
        self,
        day: int,
        dynamic_mode: bool,
        api_token: str,
        cache_manager: CacheManager,
        district_id: str = "9737",
        ramadan_start: date = None,
    ):
        super().__init__()
        self.day = day
        self.dynamic_mode = dynamic_mode
        self.api_token = api_token
        self.cache = cache_manager
        self.district_id = district_id
        self.ramadan_start = ramadan_start or date(2026, 2, 18)
        self.signals = LoaderSignals()
        self.setAutoDelete(False)

    @Slot()
    def run(self):
        try:
            data = self._load()
            self.signals.dataLoaded.emit(data)
        except Exception as exc:
            self.signals.error.emit(str(exc))

    def _load(self) -> dict:
        verse = self._load_verse()
        hadith = self._load_hadith()
        prayer = self._load_prayer()
        meal = get_meal_for_day(self.day)
        return {
            "verse": verse,
            "hadith": hadith,
            "prayer": prayer,
            "meal": meal,
            "day": self.day,
        }

    # ------------------------------------------------------------------ #
    # Ayet yükleme                                                         #
    # ------------------------------------------------------------------ #
    def _load_verse(self) -> dict:
        if self.dynamic_mode and self.api_token:
            try:
                static = get_verse_for_day(self.day)
                svc = QuranService(token=self.api_token)
                verse = svc.fetch_verse(
                    static["surah_number"], static["verse_number"]
                )
                verse.setdefault("theme", static["theme"])
                verse.setdefault("surah_name", static["surah_name"])
                self.cache.save_verse(self.day, verse)
                return verse
            except Exception:
                pass

        cached = self.cache.get_verse(self.day)
        if cached:
            return cached

        return get_verse_for_day(self.day)

    # ------------------------------------------------------------------ #
    # Hadis yükleme                                                        #
    # ------------------------------------------------------------------ #
    def _load_hadith(self) -> dict:
        if self.dynamic_mode:
            try:
                static = get_hadith_for_day(self.day)
                svc = HadithService()
                hadith = svc.fetch_hadith(static["api_id"])
                hadith.setdefault("theme", static["theme"])
                self.cache.save_hadith(self.day, hadith)
                return hadith
            except Exception:
                pass

        cached = self.cache.get_hadith(self.day)
        if cached:
            return cached

        return get_hadith_for_day(self.day)

    # ------------------------------------------------------------------ #
    # Namaz vakitleri yükleme (ay bazlı önbellekleme)                     #
    # ------------------------------------------------------------------ #
    def _load_prayer(self) -> dict:
        svc = PrayerService(district_id=self.district_id)

        # Hedef tarihin ay ve yılını hesapla
        target_date = self.ramadan_start + timedelta(days=self.day - 1)
        year, month = target_date.year, target_date.month

        # Önce önbellekten dene
        prayer_list = self.cache.get_prayer_times_for_month(year, month)

        if prayer_list is None:
            try:
                prayer_list = svc.fetch_all()
                # Dönen veride hedef ayın verileri varsa kaydet
                if prayer_list:
                    self.cache.save_prayer_times_for_month(year, month, prayer_list)
            except Exception:
                prayer_list = []

        if prayer_list:
            entry = svc.get_for_ramadan_day(prayer_list, self.day, self.ramadan_start)
            if entry:
                return entry

        return {}
