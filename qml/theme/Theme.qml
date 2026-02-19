pragma Singleton
import QtQuick 2.15

QtObject {
    // ---- Renkler ----
    readonly property color gold:        "#D4AF37"
    readonly property color goldLight:   "#F0D060"
    readonly property color darkNavy:    "#0D1B2A"
    readonly property color deepTeal:    "#0A3D4A"
    readonly property color cardBg:      "#12283A"
    readonly property color cardBorder:  "#1E3A50"
    readonly property color lightGray:   "#C8D0D8"
    readonly property color mutedGray:   "#7A8A9A"
    readonly property color white:       "#FFFFFF"
    readonly property color errorRed:    "#C0392B"
    readonly property color successGreen:"#27AE60"
    readonly property color overlayBg:   "#CC0D1B2A"

    // ---- Fontlar ----
    readonly property string arabicFont: "Amiri"
    readonly property string latinFont:  "Noto Sans"
    readonly property string fallbackFont: "Segoe UI"

    // ---- Punto Boyutları ----
    readonly property int arabicFontSize:   22
    readonly property int bodyFontSize:     14
    readonly property int smallFontSize:    12
    readonly property int titleFontSize:    18
    readonly property int badgeFontSize:    13

    // ---- Köşe Yarıçapları ----
    readonly property int cardRadius:    12
    readonly property int buttonRadius:   8
    readonly property int badgeRadius:   20

    // ---- Boşluklar ----
    readonly property int spacingSmall:   6
    readonly property int spacingMedium: 12
    readonly property int spacingLarge:  20
    readonly property int cardPadding:   16
}
