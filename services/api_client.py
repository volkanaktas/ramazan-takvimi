import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Any


class ApiClient:
    """Retry desteğiyle temel HTTP istemcisi."""

    DEFAULT_TIMEOUT = 10  # saniye

    def __init__(self, base_url: str = "", token: str = ""):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._session = self._build_session()

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def _headers(self) -> dict:
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def get(self, path: str, params: Optional[dict] = None) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        response = self._session.get(
            url,
            headers=self._headers(),
            params=params,
            timeout=self.DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        self._session.close()
