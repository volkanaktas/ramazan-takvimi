from PySide6.QtCore import QObject, Signal, Property


class HadithModel(QObject):
    """Günün hadisini tutan QML'e açık model."""

    changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = ""
        self._source = ""
        self._narrator = ""
        self._theme = ""

    # --- text ---
    def get_text(self):
        return self._text

    def set_text(self, v):
        if self._text != v:
            self._text = v
            self.changed.emit()

    text = Property(str, get_text, set_text, notify=changed)

    # --- source ---
    def get_source(self):
        return self._source

    def set_source(self, v):
        if self._source != v:
            self._source = v
            self.changed.emit()

    source = Property(str, get_source, set_source, notify=changed)

    # --- narrator ---
    def get_narrator(self):
        return self._narrator

    def set_narrator(self, v):
        if self._narrator != v:
            self._narrator = v
            self.changed.emit()

    narrator = Property(str, get_narrator, set_narrator, notify=changed)

    # --- theme ---
    def get_theme(self):
        return self._theme

    def set_theme(self, v):
        if self._theme != v:
            self._theme = v
            self.changed.emit()

    theme = Property(str, get_theme, set_theme, notify=changed)

    def update(self, data: dict) -> None:
        self._text = data.get("text", "")
        self._source = data.get("source", "")
        self._narrator = data.get("narrator", "")
        self._theme = data.get("theme", "")
        self.changed.emit()
