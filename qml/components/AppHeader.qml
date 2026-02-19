import QtQuick 2.15
import QtQuick.Layouts 1.15

Item {
    height: 70

    signal settingsClicked()

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: Theme.spacingMedium
        anchors.rightMargin: Theme.spacingMedium
        spacing: Theme.spacingMedium

        // Sol: Başlık + Yıl + Alt başlık
        Column {
            spacing: 2
            Layout.fillWidth: false

            Text {
                text: "\u262A Ramazan Takvimi " + (appController ? appController.currentYear : "2026")
                font.family: Theme.latinFont
                font.pixelSize: Theme.titleFontSize + 2
                font.bold: true
                color: Theme.gold
            }
            Text {
                text: "Mersin Namaz Vakitleri"
                font.family: Theme.latinFont
                font.pixelSize: Theme.smallFontSize
                color: Theme.mutedGray
            }
        }

        // Kurum adı (esnek genişlik, sağdan hizalı)
        Text {
            visible: appController && appController.institutionName !== ""
            text: appController ? appController.institutionName : ""
            font.family: Theme.latinFont
            font.pixelSize: Theme.bodyFontSize
            font.bold: true
            color: Theme.lightGray
            horizontalAlignment: Text.AlignRight
            Layout.fillWidth: true
            elide: Text.ElideLeft
        }

        // Gün rozeti
        Rectangle {
            width: 84
            height: 36
            radius: Theme.badgeRadius
            color: "transparent"
            border.color: Theme.gold
            border.width: 1.5

            Text {
                anchors.centerIn: parent
                text: appController ? appController.currentDay + ". G\u00FCn" : "1. G\u00FCn"
                font.family: Theme.latinFont
                font.pixelSize: Theme.badgeFontSize
                font.bold: true
                color: Theme.gold
            }
        }

        // Ayarlar butonu
        Rectangle {
            width: 36
            height: 36
            radius: 18
            color: settingsArea.containsMouse ? Qt.rgba(1,1,1,0.1) : "transparent"
            border.color: Theme.mutedGray
            border.width: 1

            Text {
                anchors.centerIn: parent
                text: "\u2699"
                font.pixelSize: 18
                color: Theme.mutedGray
            }

            MouseArea {
                id: settingsArea
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: settingsClicked()
            }
        }
    }
}
