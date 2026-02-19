import json
import os
from typing import Any, Optional


class CacheManager:
    """cache/ dizinindeki JSON önbellek dosyalarını yönetir."""

    def __init__(self, cache_dir: str = None):
        if cache_dir is None:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cache_dir = os.path.join(base, "cache")
        self._cache_dir = cache_dir
        os.makedirs(self._cache_dir, exist_ok=True)

    def _path(self, filename: str) -> str:
        return os.path.join(self._cache_dir, filename)

    def load(self, filename: str) -> Optional[Any]:
        path = self._path(filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save(self, filename: str, data: Any) -> bool:
        path = self._path(filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except OSError:
            return False

    def exists(self, filename: str) -> bool:
        return os.path.isfile(self._path(filename))

    def get_verse(self, day: int) -> Optional[dict]:
        data = self.load("verse_cache.json") or {}
        return data.get(str(day))

    def save_verse(self, day: int, verse_data: dict) -> None:
        data = self.load("verse_cache.json") or {}
        data[str(day)] = verse_data
        self.save("verse_cache.json", data)

    def get_hadith(self, day: int) -> Optional[dict]:
        data = self.load("hadith_cache.json") or {}
        return data.get(str(day))

    def save_hadith(self, day: int, hadith_data: dict) -> None:
        data = self.load("hadith_cache.json") or {}
        data[str(day)] = hadith_data
        self.save("hadith_cache.json", data)

    # Namaz vakitleri: ay bazlı önbellekleme
    def get_prayer_times_for_month(self, year: int, month: int) -> Optional[list]:
        return self.load(f"prayer_{year}_{month:02d}.json")

    def save_prayer_times_for_month(self, year: int, month: int, data: list) -> None:
        self.save(f"prayer_{year}_{month:02d}.json", data)

    # Eski API: geriye uyumluluk
    def get_prayer_times(self) -> Optional[list]:
        from datetime import date
        today = date.today()
        return self.get_prayer_times_for_month(today.year, today.month)

    def save_prayer_times(self, data: list) -> None:
        from datetime import date
        today = date.today()
        self.save_prayer_times_for_month(today.year, today.month, data)

    def clear_prayer_cache(self) -> None:
        """Tüm namaz vakitleri önbellek dosyalarını siler."""
        for fname in os.listdir(self._cache_dir):
            if fname.startswith("prayer_") and fname.endswith(".json"):
                try:
                    os.remove(os.path.join(self._cache_dir, fname))
                except OSError:
                    pass

    def get_location_cache(self, kind: str) -> Optional[list]:
        """Ülke/şehir/ilçe listesi önbellekten yükle."""
        return self.load(f"location_{kind}.json")

    def save_location_cache(self, kind: str, data: list) -> None:
        self.save(f"location_{kind}.json", data)
