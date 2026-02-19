import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    color: Theme.cardBg
    radius: Theme.cardRadius
    border.color: Theme.cardBorder
    border.width: 1
    clip: true
    implicitHeight: verseCol.implicitHeight + Theme.cardPadding * 2 + 8

    // Üst altın vurgu
    Rectangle {
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: 3
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0.0; color: "transparent" }
            GradientStop { position: 0.5; color: Theme.gold }
            GradientStop { position: 1.0; color: "transparent" }
        }
    }

    ColumnLayout {
        id: verseCol
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: Theme.cardPadding
        anchors.topMargin: Theme.cardPadding + 4
        spacing: Theme.spacingSmall

        // ── Başlık + referans ────────────────────────────────────────────
        RowLayout {
            Layout.fillWidth: true
            spacing: 8

            Text { text: "\uD83D\uDCD6"; font.pixelSize: 15 }
            Text {
                text: "G\u00FCn\u00FCn Ayeti"
                font.family: Theme.latinFont; font.pixelSize: Theme.badgeFontSize
                font.bold: true; color: Theme.gold
                Layout.fillWidth: true
            }
            Text {
                text: verseModel
                      ? verseModel.surahName + " " + verseModel.surahNumber + ":" + verseModel.verseNumber
                      : ""
                font.family: Theme.latinFont; font.pixelSize: Theme.smallFontSize; color: Theme.mutedGray
            }
        }

        // Tema etiketi
        Text {
            visible: verseModel && verseModel.theme !== ""
            text: verseModel ? verseModel.theme : ""
            font.family: Theme.latinFont; font.pixelSize: Theme.smallFontSize
            font.italic: true; color: Theme.goldLight; opacity: 0.9
        }

        // ── Arapça metin ─────────────────────────────────────────────────
        Text {
            Layout.fillWidth: true
            text: verseModel ? verseModel.arabic : ""
            font.family: Theme.arabicFont
            font.pixelSize: Theme.arabicFontSize
            color: Theme.white
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignRight
            lineHeight: 1.7
            visible: text !== ""
        }

        // Ayırıcı
        Rectangle {
            Layout.fillWidth: true; height: 1; color: Theme.gold; opacity: 0.3
            visible: verseModel && verseModel.arabic !== ""
        }

        // ── Türkçe meal ──────────────────────────────────────────────────
        Text {
            Layout.fillWidth: true
            text: verseModel
                  ? (verseModel.turkish !== "" ? verseModel.turkish : "Y\u00FCkleniyor...")
                  : "Y\u00FCkleniyor..."
            font.family: Theme.latinFont; font.pixelSize: Theme.bodyFontSize
            color: Theme.lightGray; wrapMode: Text.WordWrap
            lineHeight: 1.5; font.italic: true
        }
    }
}
