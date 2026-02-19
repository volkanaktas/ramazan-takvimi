import QtQuick 2.15

Rectangle {
    property bool active: false
    color: "#0A2030"
    radius: 6
    border.color: active ? Theme.gold : Theme.mutedGray
    border.width: 1
}
