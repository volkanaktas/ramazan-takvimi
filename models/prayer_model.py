from PySide6.QtCore import QObject, Signal, Property


class PrayerModel(QObject):
    """Namaz vakitlerini tutan QML'e açık model."""

    changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._imsak = "--:--"
        self._gunes = "--:--"
        self._ogle = "--:--"
        self._ikindi = "--:--"
        self._aksam = "--:--"
        self._yatsi = "--:--"
        self._tarih = ""

    def _make_property(attr):
        def getter(self):
            return getattr(self, attr)

        def setter(self, v):
            if getattr(self, attr) != v:
                setattr(self, attr, v)
                self.changed.emit()

        return getter, setter

    # --- imsak ---
    def get_imsak(self): return self._imsak
    def set_imsak(self, v):
        if self._imsak != v:
            self._imsak = v
            self.changed.emit()
    imsak = Property(str, get_imsak, set_imsak, notify=changed)

    # --- gunes ---
    def get_gunes(self): return self._gunes
    def set_gunes(self, v):
        if self._gunes != v:
            self._gunes = v
            self.changed.emit()
    gunes = Property(str, get_gunes, set_gunes, notify=changed)

    # --- ogle ---
    def get_ogle(self): return self._ogle
    def set_ogle(self, v):
        if self._ogle != v:
            self._ogle = v
            self.changed.emit()
    ogle = Property(str, get_ogle, set_ogle, notify=changed)

    # --- ikindi ---
    def get_ikindi(self): return self._ikindi
    def set_ikindi(self, v):
        if self._ikindi != v:
            self._ikindi = v
            self.changed.emit()
    ikindi = Property(str, get_ikindi, set_ikindi, notify=changed)

    # --- aksam (iftar) ---
    def get_aksam(self): return self._aksam
    def set_aksam(self, v):
        if self._aksam != v:
            self._aksam = v
            self.changed.emit()
    aksam = Property(str, get_aksam, set_aksam, notify=changed)

    # --- yatsi ---
    def get_yatsi(self): return self._yatsi
    def set_yatsi(self, v):
        if self._yatsi != v:
            self._yatsi = v
            self.changed.emit()
    yatsi = Property(str, get_yatsi, set_yatsi, notify=changed)

    # --- tarih ---
    def get_tarih(self): return self._tarih
    def set_tarih(self, v):
        if self._tarih != v:
            self._tarih = v
            self.changed.emit()
    tarih = Property(str, get_tarih, set_tarih, notify=changed)

    def update(self, data: dict) -> None:
        self._imsak = data.get("Imsak", "--:--")
        self._gunes = data.get("Gunes", "--:--")
        self._ogle = data.get("Ogle", "--:--")
        self._ikindi = data.get("Ikindi", "--:--")
        self._aksam = data.get("Aksam", "--:--")
        self._yatsi = data.get("Yatsi", "--:--")
        self._tarih = data.get("tarih", "")
        self.changed.emit()
