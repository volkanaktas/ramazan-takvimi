"""
Hava durumu verisini QML'e aktaran model.
"""

from PySide6.QtCore import QObject, Property, Signal


class WeatherModel(QObject):
    weatherChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._temperature = ""
        self._feelsLike = ""
        self._humidity = ""
        self._windSpeed = ""
        self._description = ""
        self._icon = ""
        self._locationName = ""

    def update(self, data: dict) -> None:
        self._temperature = data.get("temperature", "")
        self._feelsLike = data.get("feelsLike", "")
        self._humidity = data.get("humidity", "")
        self._windSpeed = data.get("windSpeed", "")
        self._description = data.get("description", "")
        self._icon = data.get("icon", "")
        self._locationName = data.get("locationName", "")
        self.weatherChanged.emit()

    def _get_temperature(self): return self._temperature
    temperature = Property(str, _get_temperature, notify=weatherChanged)

    def _get_feelsLike(self): return self._feelsLike
    feelsLike = Property(str, _get_feelsLike, notify=weatherChanged)

    def _get_humidity(self): return self._humidity
    humidity = Property(str, _get_humidity, notify=weatherChanged)

    def _get_windSpeed(self): return self._windSpeed
    windSpeed = Property(str, _get_windSpeed, notify=weatherChanged)

    def _get_description(self): return self._description
    description = Property(str, _get_description, notify=weatherChanged)

    def _get_icon(self): return self._icon
    icon = Property(str, _get_icon, notify=weatherChanged)

    def _get_locationName(self): return self._locationName
    locationName = Property(str, _get_locationName, notify=weatherChanged)
