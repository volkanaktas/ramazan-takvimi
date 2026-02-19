import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    property string label: ""
    property bool active: false
    signal activate()

    implicitWidth: 170
    implicitHeight: 40
    radius: 8
    color: active ? Qt.rgba(0.83, 0.69, 0.22, 0.2) : "transparent"
    border.color: active ? Theme.gold : Theme.mutedGray
    border.width: active ? 2 : 1

    RowLayout {
        anchors.centerIn: parent
        spacing: 8
        Text {
            text: active ? "\u25C9" : "\u25CB"
            color: Theme.gold
            font.pixelSize: 14
        }
        Text {
            text: label
            font.family: Theme.latinFont
            font.pixelSize: Theme.smallFontSize
            color: active ? Theme.gold : Theme.mutedGray
        }
    }

    MouseArea {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: parent.activate()
    }
}
