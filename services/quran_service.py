from services.api_client import ApiClient

QURAN_API_BASE = "https://acikkaynakkuran-dev.diyanet.gov.tr/api/v1"


class QuranService:
    """Diyanet Kur'an API üzerinden ayet çeker."""

    def __init__(self, token: str = ""):
        self._client = ApiClient(base_url=QURAN_API_BASE, token=token)

    def set_token(self, token: str) -> None:
        self._client.token = token

    def fetch_verse(self, surah: int, verse: int) -> dict:
        """Belirtilen sure ve ayet numarası için ayet verisini döndürür.

        Returns:
            dict: arabic, turkish, surah_name, surah_number, verse_number anahtarlarını içerir.
        Raises:
            Exception: API hatası veya yetersiz token.
        """
        path = f"verses/{surah}/{verse}"
        data = self._client.get(path)
        return self._normalize(data, surah, verse)

    def _normalize(self, data: dict, surah: int, verse: int) -> dict:
        """API yanıtını standart formata çevirir."""
        # Diyanet API yanıt formatı değişkenlik gösterebilir
        arabic = (
            data.get("arabic")
            or data.get("verse_text")
            or data.get("text")
            or ""
        )
        turkish = (
            data.get("turkish")
            or data.get("translation")
            or data.get("meali")
            or ""
        )
        surah_name = (
            data.get("surah_name")
            or data.get("sure_adi")
            or ""
        )
        return {
            "arabic": arabic,
            "turkish": turkish,
            "surah_name": surah_name,
            "surah_number": surah,
            "verse_number": verse,
            "theme": "",
        }
