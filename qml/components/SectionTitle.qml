import QtQuick 2.15

Text {
    property alias text: label.text
    id: label
    font.family: Theme.latinFont
    font.pixelSize: Theme.bodyFontSize
    font.bold: true
    color: Theme.lightGray
}
