import QtQuick 2.15
import QtQuick.Layouts 1.15

RowLayout {
    property string label: ""
    property string value: "--:--"
    property bool highlight: false

    spacing: 8

    Text {
        text: label
        font.family: Theme.latinFont
        font.pixelSize: Theme.smallFontSize
        color: highlight ? Theme.gold : Theme.mutedGray
        font.bold: highlight
        Layout.preferredWidth: 65
    }

    Text {
        text: value
        font.family: Theme.latinFont
        font.pixelSize: highlight ? Theme.bodyFontSize + 1 : Theme.bodyFontSize
        color: highlight ? Theme.gold : Theme.lightGray
        font.bold: highlight
    }
}
