"""EzanVakti API üzerinden ülke / şehir / ilçe listelerini çeker."""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE = "https://ezanvakti.emushaf.net"
TIMEOUT = 10


def _session() -> requests.Session:
    s = requests.Session()
    retry = Retry(total=2, backoff_factor=0.3)
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s


def fetch_countries() -> list:
    """[{"UlkeID": "2", "UlkeAdi": "TÜRKİYE"}, ...] döndürür."""
    with _session() as s:
        r = s.get(f"{BASE}/ulkeler", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()


def fetch_cities(ulke_id: str) -> list:
    """[{"SehirID": "557", "SehirAdi": "MERSİN"}, ...] döndürür."""
    with _session() as s:
        r = s.get(f"{BASE}/sehirler/{ulke_id}", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()


def fetch_districts(sehir_id: str) -> list:
    """[{"IlceID": "9737", "IlceAdi": "MERKEZ"}, ...] döndürür."""
    with _session() as s:
        r = s.get(f"{BASE}/ilceler/{sehir_id}", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
