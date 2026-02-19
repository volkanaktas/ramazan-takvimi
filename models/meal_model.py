from PySide6.QtCore import QObject, Signal, Property


class MealModel(QObject):
    """İftar yemeği önerisini tutan QML'e açık model."""

    changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._soup = ""
        self._main_course = ""
        self._dessert = ""
        self._note = ""

    # --- soup ---
    def get_soup(self): return self._soup
    def set_soup(self, v):
        if self._soup != v:
            self._soup = v
            self.changed.emit()
    soup = Property(str, get_soup, set_soup, notify=changed)

    # --- main_course ---
    def get_main_course(self): return self._main_course
    def set_main_course(self, v):
        if self._main_course != v:
            self._main_course = v
            self.changed.emit()
    mainCourse = Property(str, get_main_course, set_main_course, notify=changed)

    # --- dessert ---
    def get_dessert(self): return self._dessert
    def set_dessert(self, v):
        if self._dessert != v:
            self._dessert = v
            self.changed.emit()
    dessert = Property(str, get_dessert, set_dessert, notify=changed)

    # --- note ---
    def get_note(self): return self._note
    def set_note(self, v):
        if self._note != v:
            self._note = v
            self.changed.emit()
    note = Property(str, get_note, set_note, notify=changed)

    def update(self, data: dict) -> None:
        self._soup = data.get("soup", "")
        self._main_course = data.get("main_course", "")
        self._dessert = data.get("dessert", "")
        self._note = data.get("note", "")
        self.changed.emit()
