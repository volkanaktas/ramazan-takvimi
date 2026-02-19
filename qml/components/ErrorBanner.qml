import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root
    height: visible ? 40 : 0
    visible: appController ? appController.isOffline : false
    color: "#8B1A1A"
    radius: 6

    Behavior on height { NumberAnimation { duration: 200 } }

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
        spacing: 8

        Text {
            text: "\u26A0"
            font.pixelSize: 14
            color: Theme.gold
        }
        Text {
            text: "\u00C7evrimi\u00E7id\u0131\u015F\u0131 mod \u2014 Statik veriler g\u00F6steriliyor"
            font.family: Theme.latinFont
            font.pixelSize: Theme.smallFontSize
            color: "#FFD0D0"
            Layout.fillWidth: true
        }
    }
}
