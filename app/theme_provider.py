"""
Tema sabitlerini QML'e context property olarak aktaran Python QObject.
Tüm QML dosyalarında 'Theme.gold' gibi doğrudan erişilebilir.
"""

from PySide6.QtCore import QObject, Property, Signal, Slot


_SCALES = {
    "small":  {"body": 13, "small": 11, "title": 16, "badge": 12, "arabic": 20},
    "medium": {"body": 16, "small": 13, "title": 19, "badge": 14, "arabic": 24},
    "large":  {"body": 19, "small": 15, "title": 22, "badge": 17, "arabic": 28},
}


class ThemeProvider(QObject):
    """Koyu İslami temanın tüm sabit değerlerini tutar."""

    fontScaleChanged = Signal()

    def __init__(self, scale: str = "medium", parent=None):
        super().__init__(parent)
        self._scale = scale if scale in _SCALES else "medium"
        sizes = _SCALES[self._scale]
        self._bodyFontSize = sizes["body"]
        self._smallFontSize = sizes["small"]
        self._titleFontSize = sizes["title"]
        self._badgeFontSize = sizes["badge"]
        self._arabicFontSize = sizes["arabic"]

    @Slot(str)
    def set_scale(self, scale: str) -> None:
        if scale not in _SCALES:
            return
        if self._scale == scale:
            return
        self._scale = scale
        sizes = _SCALES[scale]
        self._bodyFontSize = sizes["body"]
        self._smallFontSize = sizes["small"]
        self._titleFontSize = sizes["title"]
        self._badgeFontSize = sizes["badge"]
        self._arabicFontSize = sizes["arabic"]
        self.fontScaleChanged.emit()

    # --- Renkler ---
    @Property(str, constant=True)
    def gold(self): return "#D4AF37"

    @Property(str, constant=True)
    def goldLight(self): return "#F0D060"

    @Property(str, constant=True)
    def darkNavy(self): return "#0D1B2A"

    @Property(str, constant=True)
    def deepTeal(self): return "#0A3D4A"

    @Property(str, constant=True)
    def cardBg(self): return "#12283A"

    @Property(str, constant=True)
    def cardBorder(self): return "#1E3A50"

    @Property(str, constant=True)
    def lightGray(self): return "#C8D0D8"

    @Property(str, constant=True)
    def mutedGray(self): return "#7A8A9A"

    @Property(str, constant=True)
    def white(self): return "#FFFFFF"

    @Property(str, constant=True)
    def errorRed(self): return "#C0392B"

    @Property(str, constant=True)
    def overlayBg(self): return "#CC0D1B2A"

    # --- Fontlar ---
    @Property(str, constant=True)
    def arabicFont(self): return "Amiri"

    @Property(str, constant=True)
    def latinFont(self): return "Noto Sans"

    # --- Punto Boyutları ---
    def _get_arabicFontSize(self): return self._arabicFontSize
    arabicFontSize = Property(int, _get_arabicFontSize, notify=fontScaleChanged)

    def _get_bodyFontSize(self): return self._bodyFontSize
    bodyFontSize = Property(int, _get_bodyFontSize, notify=fontScaleChanged)

    def _get_smallFontSize(self): return self._smallFontSize
    smallFontSize = Property(int, _get_smallFontSize, notify=fontScaleChanged)

    def _get_titleFontSize(self): return self._titleFontSize
    titleFontSize = Property(int, _get_titleFontSize, notify=fontScaleChanged)

    def _get_badgeFontSize(self): return self._badgeFontSize
    badgeFontSize = Property(int, _get_badgeFontSize, notify=fontScaleChanged)

    # --- Font Ölçeği ---
    def _get_fontScale(self): return self._scale
    fontScale = Property(str, _get_fontScale, notify=fontScaleChanged)

    # --- Köşe Yarıçapları ---
    @Property(int, constant=True)
    def cardRadius(self): return 12

    @Property(int, constant=True)
    def buttonRadius(self): return 8

    @Property(int, constant=True)
    def badgeRadius(self): return 20

    # --- Boşluklar ---
    @Property(int, constant=True)
    def spacingSmall(self): return 6

    @Property(int, constant=True)
    def spacingMedium(self): return 12

    @Property(int, constant=True)
    def spacingLarge(self): return 20

    @Property(int, constant=True)
    def cardPadding(self): return 16
