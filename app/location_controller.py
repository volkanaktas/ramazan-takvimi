"""
Ülke / Şehir / İlçe seçimi için QML ↔ Python köprüsü.
QRunnable ile arka planda EzanVakti API çağrısı yapar.
"""

from PySide6.QtCore import QObject, QRunnable, Signal, Slot, Property, QThreadPool

from app.settings_manager import SettingsManager
from app.cache_manager import CacheManager
import services.location_service as loc_svc


# ── Sinyal taşıyıcı ───────────────────────────────────────────────────────────
class _Signals(QObject):
    done  = Signal(list)
    error = Signal(str)


class _LocRunnable(QRunnable):
    def __init__(self, fn, *args):
        super().__init__()
        self.fn      = fn
        self.args    = args
        self.signals = _Signals()
        self.setAutoDelete(False)

    def run(self):
        try:
            self.signals.done.emit(self.fn(*self.args))
        except Exception as exc:
            self.signals.error.emit(str(exc))


# ── Ana kontrolcü ─────────────────────────────────────────────────────────────
class LocationController(QObject):

    countriesChanged = Signal()
    citiesChanged    = Signal()
    districtsChanged = Signal()
    loadingChanged   = Signal(bool)
    locationSaved    = Signal(str)   # ilce_id

    def __init__(self, settings: SettingsManager, cache: CacheManager, parent=None):
        super().__init__(parent)
        self._settings  = settings
        self._cache     = cache
        self._countries : list = []   # [{"UlkeID": .., "UlkeAdi": ..}, ...]
        self._cities    : list = []   # [{"SehirID": .., "SehirAdi": ..}, ...]
        self._districts : list = []   # [{"IlceID": .., "IlceAdi": ..}, ...]
        self._loading   : bool = False
        self._runnable  = None        # GC koruma

    # ── display listeleri ─────────────────────────────────────────────────────
    def _cnames(self): return [c.get("UlkeAdi", "") for c in self._countries]
    def _snames(self): return [s.get("SehirAdi", "") for s in self._cities]
    def _inames(self): return [i.get("IlceAdi", "") for i in self._districts]

    countryNames  = Property(list, _cnames, notify=countriesChanged)
    cityNames     = Property(list, _snames, notify=citiesChanged)
    districtNames = Property(list, _inames, notify=districtsChanged)

    def _get_loading(self): return self._loading
    isLoading = Property(bool, _get_loading, notify=loadingChanged)

    def _get_display(self):
        return self._settings.get("location_display", "Mersin / Merkez")
    locationDisplay = Property(str, _get_display, notify=locationSaved)

    def _get_ilce_id(self):
        return self._settings.get("ilce_id", "9737")
    currentIlceId = Property(str, _get_ilce_id, notify=locationSaved)

    # ── seçili indeksler ──────────────────────────────────────────────────────
    def _country_idx(self):
        uid = self._settings.get("ulke_id", "")
        for i, c in enumerate(self._countries):
            if str(c.get("UlkeID", "")) == uid:
                return i
        return 0 if self._countries else -1

    def _city_idx(self):
        sid = self._settings.get("sehir_id", "")
        for i, s in enumerate(self._cities):
            if str(s.get("SehirID", "")) == sid:
                return i
        return 0 if self._cities else -1

    def _district_idx(self):
        iid = self._settings.get("ilce_id", "")
        for i, d in enumerate(self._districts):
            if str(d.get("IlceID", "")) == iid:
                return i
        return 0 if self._districts else -1

    currentCountryIndex  = Property(int, _country_idx,  notify=countriesChanged)
    currentCityIndex     = Property(int, _city_idx,     notify=citiesChanged)
    currentDistrictIndex = Property(int, _district_idx, notify=districtsChanged)

    # ── Slotlar ───────────────────────────────────────────────────────────────
    @Slot()
    def loadCountries(self):
        self._run(loc_svc.fetch_countries, self._on_countries)

    @Slot(int)
    def selectCountry(self, index: int):
        if 0 <= index < len(self._countries):
            uid = str(self._countries[index].get("UlkeID", ""))
            self._settings.set("ulke_id", uid)
            self._run(loc_svc.fetch_cities, self._on_cities, uid)

    @Slot(int)
    def selectCity(self, index: int):
        if 0 <= index < len(self._cities):
            sid = str(self._cities[index].get("SehirID", ""))
            self._settings.set("sehir_id", sid)
            self._run(loc_svc.fetch_districts, self._on_districts, sid)

    @Slot(int)
    def selectDistrict(self, index: int):
        if 0 <= index < len(self._districts):
            d   = self._districts[index]
            ci  = self._city_idx()
            s   = self._cities[ci] if ci >= 0 else {}
            display = f"{s.get('SehirAdi', '')} / {d.get('IlceAdi', '')}"
            self._settings.set("ilce_id",          str(d.get("IlceID", "")))
            self._settings.set("ilce_adi",         d.get("IlceAdi", ""))
            self._settings.set("sehir_id",         str(s.get("SehirID", "")))
            self._settings.set("sehir_adi",        s.get("SehirAdi", ""))
            self._settings.set("location_display", display)
            # Namaz vakitleri önbelleğini temizle
            self._cache.clear_prayer_cache()
            self.locationSaved.emit(str(d.get("IlceID", "")))

    # ── İç yardımcılar ───────────────────────────────────────────────────────
    def _run(self, fn, callback, *args):
        self._loading = True
        self.loadingChanged.emit(True)
        r = _LocRunnable(fn, *args)
        r.signals.done.connect(callback)
        r.signals.error.connect(self._on_error)
        self._runnable = r
        QThreadPool.globalInstance().start(r)

    def _on_countries(self, data: list):
        self._countries = data
        self._cities    = []
        self._districts = []
        self.countriesChanged.emit()
        self.citiesChanged.emit()
        self.districtsChanged.emit()
        self._loading = False
        self.loadingChanged.emit(False)
        # Kayıtlı ülke varsa şehirleri otomatik yükle
        uid = self._settings.get("ulke_id", "")
        if uid:
            self._run(loc_svc.fetch_cities, self._on_cities, uid)

    def _on_cities(self, data: list):
        self._cities    = data
        self._districts = []
        self.citiesChanged.emit()
        self.districtsChanged.emit()
        self._loading = False
        self.loadingChanged.emit(False)
        # Kayıtlı şehir varsa ilçeleri otomatik yükle
        sid = self._settings.get("sehir_id", "")
        if sid:
            self._run(loc_svc.fetch_districts, self._on_districts, sid)

    def _on_districts(self, data: list):
        self._districts = data
        self.districtsChanged.emit()
        self._loading = False
        self.loadingChanged.emit(False)

    def _on_error(self, msg: str):
        self._loading = False
        self.loadingChanged.emit(False)
