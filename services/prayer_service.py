from datetime import date, timedelta
from services.api_client import ApiClient

EZANVAKTI_BASE = "https://ezanvakti.emushaf.net"


class PrayerService:
    """EzanVakti API üzerinden namaz vakitlerini çeker."""

    def __init__(self, district_id: str = "9737"):
        self._ilce_id = district_id
        self._client  = ApiClient(base_url=f"{EZANVAKTI_BASE}/vakitler/{district_id}")

    def fetch_all(self) -> list:
        """Mevcut Ramazan ayı için tüm vakitleri döndürür.

        Raises:
            Exception: Bağlantı veya format hatası.
        """
        data = self._client.get("")
        if not isinstance(data, list):
            raise ValueError(f"Beklenmeyen API yanıt formatı: {type(data)}")
        return data

    def get_for_date(self, prayer_data: list, date_str: str) -> dict:
        """DD.MM.YYYY formatındaki tarihe ait vakti döndürür."""
        for entry in prayer_data:
            if entry.get("MiladiTarihKisa") == date_str:
                return entry
        return {}

    def get_for_ramadan_day(
        self, prayer_data: list, day: int, ramadan_start: date = None
    ) -> dict:
        """Ramazan gün numarasına (1-30) göre namaz vakitlerini döndürür."""
        if ramadan_start is None:
            ramadan_start = date(2026, 2, 18)
        target   = ramadan_start + timedelta(days=day - 1)
        date_str = target.strftime("%d.%m.%Y")
        entry    = self.get_for_date(prayer_data, date_str)
        if entry:
            entry = dict(entry)   # kopya – orijinali bozma
            entry["tarih"] = date_str
        return entry


class LocationService:
    """EzanVakti API üzerinden ülke / şehir / ilçe listelerini çeker."""

    def __init__(self):
        self._client = ApiClient(base_url=EZANVAKTI_BASE)

    def fetch_countries(self) -> list:
        data = self._client.get("ulkeler")
        if not isinstance(data, list):
            return []
        return [
            {"id": str(c.get("UlkeID", c.get("UlkeId", ""))),
             "name": c.get("UlkeAdi", "")}
            for c in data if isinstance(c, dict)
        ]

    def fetch_cities(self, country_id: str) -> list:
        data = self._client.get(f"sehirler/{country_id}")
        if not isinstance(data, list):
            return []
        return [
            {"id": str(c.get("SehirID", c.get("SehirId", ""))),
             "name": c.get("SehirAdi", "")}
            for c in data if isinstance(c, dict)
        ]

    def fetch_districts(self, city_id: str) -> list:
        data = self._client.get(f"ilceler/{city_id}")
        if not isinstance(data, list):
            return []
        return [
            {"id": str(c.get("IlceID", c.get("IlceId", ""))),
             "name": c.get("IlceAdi", "")}
            for c in data if isinstance(c, dict)
        ]
