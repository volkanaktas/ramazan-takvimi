"""
Open-Meteo hava durumu servisi.
API anahtarı gerektirmez.
"""

import json
import urllib.parse
import urllib.request

WMO_CODES = {
    0:  ("Açık",                "☀️"),
    1:  ("Az Bulutlu",          "🌤️"),
    2:  ("Parçalı Bulutlu",     "⛅"),
    3:  ("Kapalı",              "☁️"),
    45: ("Sisli",               "🌫️"),
    48: ("Buzlu Sis",           "🌫️"),
    51: ("Hafif Çisenti",       "🌦️"),
    53: ("Orta Çisenti",        "🌦️"),
    55: ("Yoğun Çisenti",       "🌧️"),
    61: ("Hafif Yağmur",        "🌧️"),
    63: ("Orta Yağmur",         "🌧️"),
    65: ("Şiddetli Yağmur",     "🌧️"),
    71: ("Hafif Kar",           "🌨️"),
    73: ("Orta Kar",            "❄️"),
    75: ("Yoğun Kar",           "❄️"),
    77: ("Kar Taneleri",        "🌨️"),
    80: ("Hafif Sağanak",       "🌦️"),
    81: ("Orta Sağanak",        "🌧️"),
    82: ("Şiddetli Sağanak",    "⛈️"),
    85: ("Hafif Kar Sağanağı",  "🌨️"),
    86: ("Yoğun Kar Sağanağı",  "❄️"),
    95: ("Gök Gürültülü Fırtına", "⛈️"),
    96: ("Dolu ile Fırtına",    "⛈️"),
    99: ("Yoğun Dolu Fırtınası","⛈️"),
}


def _http_get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "RamazanApp/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def geocode(city: str, district: str = "") -> dict:
    """Şehir/ilçe adından koordinat döndürür."""
    query = f"{city} {district}".strip()
    url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={urllib.parse.quote(query)}&count=3&language=tr&countryCode=TR"
    )
    data = _http_get(url)
    results = data.get("results", [])
    if not results:
        raise ValueError(f"Konum bulunamadı: {query}")
    r = results[0]
    return {"lat": r["latitude"], "lon": r["longitude"]}


def fetch_weather(lat: float, lon: float) -> dict:
    """Koordinattan güncel hava durumu verisi döndürür."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,weather_code,"
        "wind_speed_10m,apparent_temperature"
        "&timezone=Europe%2FIstanbul"
    )
    data = _http_get(url)
    current = data.get("current", {})
    code = current.get("weather_code", 0)
    desc, icon = WMO_CODES.get(code, ("Bilinmiyor", "🌡️"))
    return {
        "temperature":  str(round(current.get("temperature_2m", 0))) + "°C",
        "feelsLike":    str(round(current.get("apparent_temperature", 0))) + "°C",
        "humidity":     str(current.get("relative_humidity_2m", 0)) + "%",
        "windSpeed":    str(round(current.get("wind_speed_10m", 0))) + " km/s",
        "description":  desc,
        "icon":         icon,
        "locationName": "",
    }
