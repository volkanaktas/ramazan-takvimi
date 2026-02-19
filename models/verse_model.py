from PySide6.QtCore import QObject, Signal, Property


class VerseModel(QObject):
    """Günün ayetini tutan QML'e açık model."""

    changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._arabic = ""
        self._turkish = ""
        self._surah_name = ""
        self._surah_number = 0
        self._verse_number = 0
        self._theme = ""

    # --- arabic ---
    def get_arabic(self):
        return self._arabic

    def set_arabic(self, v):
        if self._arabic != v:
            self._arabic = v
            self.changed.emit()

    arabic = Property(str, get_arabic, set_arabic, notify=changed)

    # --- turkish ---
    def get_turkish(self):
        return self._turkish

    def set_turkish(self, v):
        if self._turkish != v:
            self._turkish = v
            self.changed.emit()

    turkish = Property(str, get_turkish, set_turkish, notify=changed)

    # --- surah_name ---
    def get_surah_name(self):
        return self._surah_name

    def set_surah_name(self, v):
        if self._surah_name != v:
            self._surah_name = v
            self.changed.emit()

    surahName = Property(str, get_surah_name, set_surah_name, notify=changed)

    # --- surah_number ---
    def get_surah_number(self):
        return self._surah_number

    def set_surah_number(self, v):
        if self._surah_number != v:
            self._surah_number = v
            self.changed.emit()

    surahNumber = Property(int, get_surah_number, set_surah_number, notify=changed)

    # --- verse_number ---
    def get_verse_number(self):
        return self._verse_number

    def set_verse_number(self, v):
        if self._verse_number != v:
            self._verse_number = v
            self.changed.emit()

    verseNumber = Property(int, get_verse_number, set_verse_number, notify=changed)

    # --- theme ---
    def get_theme(self):
        return self._theme

    def set_theme(self, v):
        if self._theme != v:
            self._theme = v
            self.changed.emit()

    theme = Property(str, get_theme, set_theme, notify=changed)

    def update(self, data: dict) -> None:
        """Tüm alanları tek seferde günceller, sadece bir kez sinyal gönderir."""
        self._arabic = data.get("arabic", "")
        self._turkish = data.get("turkish", "")
        self._surah_name = data.get("surah_name", "")
        self._surah_number = data.get("surah_number", 0)
        self._verse_number = data.get("verse_number", 0)
        self._theme = data.get("theme", "")
        self.changed.emit()

    def reference(self) -> str:
        return f"{self._surah_name} {self._surah_number}:{self._verse_number}"
