import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    color: Theme.cardBg
    radius: Theme.cardRadius
    border.color: Theme.cardBorder
    border.width: 1
    clip: true
    implicitHeight: prayerCol.implicitHeight + Theme.cardPadding * 2

    ColumnLayout {
        id: prayerCol
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: Theme.cardPadding
        spacing: Theme.spacingSmall

        // ── Başlık ────────────────────────────────────────────────────────
        RowLayout {
            Layout.fillWidth: true
            spacing: 6

            Text { text: "\uD83D\uDD4C"; font.pixelSize: 14 }
            Text {
                text: "Namaz Vakitleri"
                font.family: Theme.latinFont; font.pixelSize: Theme.badgeFontSize
                font.bold: true; color: Theme.gold
                Layout.fillWidth: true
            }
            Text {
                text: appController ? appController.locationDisplay : "Mersin / Merkez"
                font.family: Theme.latinFont; font.pixelSize: Theme.smallFontSize - 1
                color: Theme.mutedGray
                elide: Text.ElideRight
                Layout.maximumWidth: 110
            }
        }

        // Tarih
        Text {
            visible: prayerModel && prayerModel.tarih !== ""
            text: prayerModel ? prayerModel.tarih : ""
            font.family: Theme.latinFont; font.pixelSize: Theme.smallFontSize; color: Theme.mutedGray
        }

        Rectangle {
            Layout.fillWidth: true; height: 1; color: Theme.gold; opacity: 0.25
        }

        // ── Vakitler: 3 satır × 2 sütun ────────────────────────────────
        GridLayout {
            Layout.fillWidth: true
            columns: 2
            columnSpacing: 16
            rowSpacing: 7

            PrayerTimeRow { label: "\u0130msak";    value: prayerModel ? prayerModel.imsak  : "--:--"; highlight: false }
            PrayerTimeRow { label: "G\u00FCne\u015F"; value: prayerModel ? prayerModel.gunes  : "--:--"; highlight: false }
            PrayerTimeRow { label: "\u00D6\u011fle";  value: prayerModel ? prayerModel.ogle   : "--:--"; highlight: false }
            PrayerTimeRow { label: "\u0130kindi";   value: prayerModel ? prayerModel.ikindi : "--:--"; highlight: false }
            PrayerTimeRow { label: "\u0130ftar \u2605"; value: prayerModel ? prayerModel.aksam  : "--:--"; highlight: true  }
            PrayerTimeRow { label: "Yats\u0131";   value: prayerModel ? prayerModel.yatsi  : "--:--"; highlight: false }
        }
    }
}
