"""
Merkezi QObject köprüsü – QML ile Python arasındaki tüm iletişimi yönetir.
"""

import json
import threading
from datetime import date

from PySide6.QtCore import QObject, Signal, Slot, Property, QThreadPool

from app.settings_manager import SettingsManager
from app.cache_manager import CacheManager
from app.theme_provider import ThemeProvider
from models.verse_model import VerseModel
from models.hadith_model import HadithModel
from models.prayer_model import PrayerModel
from models.meal_model import MealModel
from services.data_loader import DataLoaderRunnable

# Ramazan 1447 (2026) başlangıç tarihi
RAMADAN_START_DEFAULT = date(2026, 2, 18)


class AppController(QObject):
    """QML'e açık sinyaller, property'ler ve slotlar."""

    loadingChanged = Signal(bool)
    errorOccurred = Signal(str)
    dayChanged = Signal(int)
    offlineModeChanged = Signal(bool)
    institutionNameChanged = Signal(str)
    locationDisplayChanged = Signal(str)

    # Konum yükleme sinyalleri
    countriesLoaded = Signal(str)   # JSON string: [{"id":..., "name":...}, ...]
    citiesLoaded = Signal(str)
    districtsLoaded = Signal(str)

    def __init__(
        self,
        verse_model: VerseModel,
        hadith_model: HadithModel,
        prayer_model: PrayerModel,
        meal_model: MealModel,
        settings: SettingsManager,
        cache: CacheManager,
        theme: ThemeProvider = None,
        weather_model=None,
        parent=None,
    ):
        super().__init__(parent)
        self._verse_model = verse_model
        self._hadith_model = hadith_model
        self._prayer_model = prayer_model
        self._meal_model = meal_model
        self._settings = settings
        self._cache = cache
        self._theme = theme
        self._weather_model = weather_model

        # Ramazan başlangıcı (config'den veya varsayılan)
        ramadan_str = self._settings.get("ramadan_start", "2026-02-18")
        try:
            self._ramadan_start = date.fromisoformat(ramadan_str)
        except (ValueError, TypeError):
            self._ramadan_start = RAMADAN_START_DEFAULT

        self._current_day: int = self._compute_current_ramadan_day()
        self._is_loading: bool = False
        self._is_offline: bool = False
        self._dynamic_mode: bool = self._settings.get("dynamic_mode", False)
        self._api_token: str = self._settings.get("api_token", "")
        self._institution_name: str = self._settings.get("institution_name", "")
        self._district_id: str = str(self._settings.get("ilce_id", "9737"))
        self._location_display: str = self._settings.get("location_display", "Mersin / Merkez")
        self._lat: float = float(self._settings.get("lat", 36.8))
        self._lon: float = float(self._settings.get("lon", 34.64))
        self._active_runnable = None

        # İlk yükleme
        self._load_day(self._current_day)
        self._load_weather()

    # ------------------------------------------------------------------ #
    # Yardımcı                                                             #
    # ------------------------------------------------------------------ #
    def _compute_current_ramadan_day(self) -> int:
        today = date.today()
        delta = (today - self._ramadan_start).days + 1
        return max(1, min(30, delta))

    # ------------------------------------------------------------------ #
    # Properties                                                           #
    # ------------------------------------------------------------------ #
    def _get_current_day(self) -> int:
        return self._current_day

    def _set_current_day(self, v: int) -> None:
        if self._current_day != v:
            self._current_day = v
            self.dayChanged.emit(v)

    currentDay = Property(int, _get_current_day, _set_current_day, notify=dayChanged)

    # ---
    def _get_is_loading(self) -> bool:
        return self._is_loading

    def _set_is_loading(self, v: bool) -> None:
        if self._is_loading != v:
            self._is_loading = v
            self.loadingChanged.emit(v)

    isLoading = Property(bool, _get_is_loading, _set_is_loading, notify=loadingChanged)

    # ---
    def _get_dynamic_mode(self) -> bool:
        return self._dynamic_mode

    def _set_dynamic_mode(self, v: bool) -> None:
        self._dynamic_mode = v

    isDynamicMode = Property(bool, _get_dynamic_mode, _set_dynamic_mode)

    # ---
    def _get_api_token(self) -> str:
        return self._api_token

    def _set_api_token(self, v: str) -> None:
        self._api_token = v

    apiToken = Property(str, _get_api_token, _set_api_token)

    # ---
    def _get_is_offline(self) -> bool:
        return self._is_offline

    isOffline = Property(bool, _get_is_offline, notify=offlineModeChanged)

    # ---
    def _get_institution_name(self) -> str:
        return self._institution_name

    def _set_institution_name(self, v: str) -> None:
        if self._institution_name != v:
            self._institution_name = v
            self.institutionNameChanged.emit(v)

    institutionName = Property(
        str, _get_institution_name, _set_institution_name,
        notify=institutionNameChanged
    )

    # ---
    @Property(int, constant=True)
    def currentYear(self) -> int:
        return date.today().year

    # ---
    def _get_district_id(self) -> str:
        return self._district_id

    districtId = Property(str, _get_district_id)

    # ---
    def _get_location_display(self) -> str:
        return self._location_display

    def _set_location_display(self, v: str) -> None:
        if self._location_display != v:
            self._location_display = v
            self.locationDisplayChanged.emit(v)

    locationDisplay = Property(
        str, _get_location_display, _set_location_display,
        notify=locationDisplayChanged
    )

    # ------------------------------------------------------------------ #
    # Navigasyon Slotları                                                  #
    # ------------------------------------------------------------------ #
    @Slot()
    def nextDay(self) -> None:
        if self._current_day < 30:
            self._current_day += 1
            self.dayChanged.emit(self._current_day)
            self._load_day(self._current_day)

    @Slot()
    def previousDay(self) -> None:
        if self._current_day > 1:
            self._current_day -= 1
            self.dayChanged.emit(self._current_day)
            self._load_day(self._current_day)

    @Slot(int)
    def goToDay(self, day: int) -> None:
        if 1 <= day <= 30:
            self._current_day = day
            self.dayChanged.emit(day)
            self._load_day(day)

    # ------------------------------------------------------------------ #
    # Ayarlar Slotları                                                     #
    # ------------------------------------------------------------------ #
    @Slot(bool, str, str, str)
    def saveSettings(
        self,
        dynamic_mode: bool,
        api_token: str,
        institution_name: str,
        font_scale: str = "medium",
    ) -> None:
        self._dynamic_mode = dynamic_mode
        self._api_token = api_token
        self._set_institution_name(institution_name)

        self._settings.set("dynamic_mode", dynamic_mode)
        self._settings.set("api_token", api_token)
        self._settings.set("institution_name", institution_name)

        if self._theme:
            self._theme.set_scale(font_scale)
        self._settings.set("font_scale", font_scale)

        self._load_day(self._current_day)

    @Slot(str, str, str, str)
    def saveDistrictSelection(
        self,
        country_id: str,
        city_id: str,
        district_id: str,
        location_display: str = "",
    ) -> None:
        """Seçilen konumu kaydet ve namaz vakitlerini yeniden yükle."""
        if district_id and district_id != self._district_id:
            self._district_id = district_id
            self._settings.set("ulke_id", country_id)
            self._settings.set("sehir_id", city_id)
            self._settings.set("ilce_id", district_id)
            if location_display:
                self._set_location_display(location_display)
                self._settings.set("location_display", location_display)
            # Namaz vakitleri önbelleğini sıfırla (yeni konum için)
            self._cache.clear_prayer_cache()
            self._load_day(self._current_day)
            self._load_weather()

    # ------------------------------------------------------------------ #
    # Konum Yükleme Slotları                                               #
    # ------------------------------------------------------------------ #
    @Slot()
    def loadCountries(self) -> None:
        """Arka planda ülkeleri yükler, countriesLoaded sinyalini emit eder."""
        threading.Thread(
            target=self._fetch_location, args=("countries", "", ""), daemon=True
        ).start()

    @Slot(str)
    def loadCities(self, country_id: str) -> None:
        threading.Thread(
            target=self._fetch_location, args=("cities", country_id, ""), daemon=True
        ).start()

    @Slot(str)
    def loadDistricts(self, city_id: str) -> None:
        threading.Thread(
            target=self._fetch_location, args=("districts", "", city_id), daemon=True
        ).start()

    def _fetch_location(self, kind: str, country_id: str, city_id: str) -> None:
        from services.prayer_service import LocationService
        try:
            svc = LocationService()
            if kind == "countries":
                data = svc.fetch_countries()
                self._cache.save_location_cache("countries", data)
            elif kind == "cities":
                data = svc.fetch_cities(country_id)
                self._cache.save_location_cache(f"cities_{country_id}", data)
            elif kind == "districts":
                data = svc.fetch_districts(city_id)
                self._cache.save_location_cache(f"districts_{city_id}", data)
            else:
                data = []
        except Exception:
            # Önbellekten dene
            key = kind if kind == "countries" else (
                f"cities_{country_id}" if kind == "cities" else f"districts_{city_id}"
            )
            data = self._cache.get_location_cache(key) or []

        json_str = json.dumps(data, ensure_ascii=False)
        if kind == "countries":
            self.countriesLoaded.emit(json_str)
        elif kind == "cities":
            self.citiesLoaded.emit(json_str)
        elif kind == "districts":
            self.districtsLoaded.emit(json_str)

    # ------------------------------------------------------------------ #
    # İç yükleme mekanizması                                              #
    # ------------------------------------------------------------------ #
    def _load_day(self, day: int) -> None:
        self._set_is_loading(True)
        runnable = DataLoaderRunnable(
            day=day,
            dynamic_mode=self._dynamic_mode,
            api_token=self._api_token,
            cache_manager=self._cache,
            district_id=self._district_id,
            ramadan_start=self._ramadan_start,
        )
        self._active_runnable = runnable
        runnable.signals.dataLoaded.connect(self._on_data_loaded)
        runnable.signals.error.connect(self._on_error)
        QThreadPool.globalInstance().start(runnable)

    def _on_data_loaded(self, data: dict) -> None:
        self._verse_model.update(data.get("verse", {}))
        self._hadith_model.update(data.get("hadith", {}))
        self._prayer_model.update(data.get("prayer", {}))
        self._meal_model.update(data.get("meal", {}))
        self._set_is_loading(False)
        if self._is_offline:
            self._is_offline = False
            self.offlineModeChanged.emit(False)

    def _on_error(self, msg: str) -> None:
        self.errorOccurred.emit(msg)
        self._set_is_loading(False)
        if not self._is_offline:
            self._is_offline = True
            self.offlineModeChanged.emit(True)

    # ------------------------------------------------------------------ #
    # Hava Durumu                                                          #
    # ------------------------------------------------------------------ #
    def _load_weather(self) -> None:
        if self._weather_model is None:
            return
        lat = self._lat
        lon = self._lon
        location = self._location_display
        weather_model = self._weather_model
        threading.Thread(
            target=self._fetch_weather,
            args=(lat, lon, location, weather_model),
            daemon=True,
        ).start()

    @staticmethod
    def _fetch_weather(lat: float, lon: float, location: str, weather_model) -> None:
        try:
            from services.weather_service import fetch_weather
            data = fetch_weather(lat, lon)
            data["locationName"] = location
            weather_model.update(data)
        except Exception:
            pass
