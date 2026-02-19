import QtQuick 2.15

Item {
    width: parent ? parent.width : 300
    height: 20

    Rectangle {
        anchors.centerIn: parent
        width: parent.width * 0.85
        height: 1
        color: Theme.gold
        opacity: 0.6
    }

    Rectangle {
        anchors.centerIn: parent
        width: 8
        height: 8
        radius: 4
        color: Theme.gold
        rotation: 45
    }

    Rectangle {
        anchors.verticalCenter: parent.verticalCenter
        x: parent.width * 0.075 + 20
        width: 5
        height: 5
        radius: 2.5
        color: Theme.gold
        opacity: 0.7
        rotation: 45
    }

    Rectangle {
        anchors.verticalCenter: parent.verticalCenter
        x: parent.width * 0.925 - 25
        width: 5
        height: 5
        radius: 2.5
        color: Theme.gold
        opacity: 0.7
        rotation: 45
    }
}
