import QtQuick 2.15
import QtQuick.Layouts 1.15

RowLayout {
    property string icon: ""
    property string label: ""
    property string value: ""

    spacing: 8

    Text {
        text: icon
        font.pixelSize: 14
    }

    Text {
        text: label + ":"
        font.family: Theme.latinFont
        font.pixelSize: Theme.smallFontSize
        color: Theme.mutedGray
        Layout.preferredWidth: 72
    }

    Text {
        text: value !== "" ? value : "\u2014"
        font.family: Theme.latinFont
        font.pixelSize: Theme.bodyFontSize
        color: Theme.lightGray
        font.bold: value !== ""
        Layout.fillWidth: true
        wrapMode: Text.WordWrap
    }
}
