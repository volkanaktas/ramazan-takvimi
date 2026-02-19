import QtQuick 2.15

Rectangle {
    id: root
    visible: appController ? appController.isLoading : false
    color: "#CC0D1B2A"

    Rectangle {
        id: spinner
        anchors.centerIn: parent
        width: 48
        height: 48
        radius: 24
        color: "transparent"
        border.color: Theme.gold
        border.width: 3

        Rectangle {
            x: parent.width / 2 - 3
            y: 2
            width: 6
            height: 6
            radius: 3
            color: Theme.gold
        }

        RotationAnimator {
            target: spinner
            from: 0
            to: 360
            duration: 900
            loops: Animation.Infinite
            running: root.visible
        }
    }

    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: spinner.bottom
        anchors.topMargin: 12
        text: "Y\u00FCkleniyor..."
        font.family: Theme.latinFont
        font.pixelSize: Theme.bodyFontSize
        color: Theme.lightGray
    }
}
