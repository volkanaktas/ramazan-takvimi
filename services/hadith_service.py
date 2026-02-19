from services.api_client import ApiClient

HADITH_API_BASE = "https://hadeethenc.com/api/v1"


class HadithService:
    """HadeethEnc API üzerinden hadis çeker."""

    def __init__(self):
        self._client = ApiClient(base_url=HADITH_API_BASE)

    def fetch_hadith(self, hadith_id: int) -> dict:
        """Belirtilen ID için Türkçe hadis verisini döndürür.

        Returns:
            dict: text, source, narrator, theme anahtarlarını içerir.
        Raises:
            Exception: API hatası.
        """
        data = self._client.get(
            "hadeeths/one/",
            params={"language": "tr", "id": hadith_id},
        )
        return self._normalize(data)

    def _normalize(self, data: dict) -> dict:
        text = data.get("content") or data.get("text") or ""
        source = data.get("reference") or data.get("attribution") or ""
        narrator = data.get("hadeeth_intro") or ""
        return {
            "text": text,
            "source": source,
            "narrator": narrator,
            "theme": "",
        }
