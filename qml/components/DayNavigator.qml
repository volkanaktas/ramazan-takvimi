import QtQuick 2.15
import QtQuick.Layouts 1.15

Item {
    height: 56

    RowLayout {
        anchors.centerIn: parent
        spacing: Theme.spacingLarge

        // Önceki Gün
        Rectangle {
            width: 110
            height: 40
            radius: Theme.buttonRadius
            color: prevArea.containsMouse && !prevArea.isDisabled
                   ? Qt.rgba(0.83, 0.69, 0.22, 0.2) : "transparent"
            border.color: prevArea.isDisabled ? Theme.mutedGray : Theme.gold
            border.width: 1.5
            opacity: prevArea.isDisabled ? 0.35 : 1.0

            RowLayout {
                anchors.centerIn: parent
                spacing: 4
                Text { text: "\u25C4"; font.pixelSize: 11; color: Theme.gold }
                Text {
                    text: "\u00D6nceki"
                    font.family: Theme.latinFont
                    font.pixelSize: Theme.bodyFontSize
                    color: Theme.gold
                }
            }

            MouseArea {
                id: prevArea
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: isDisabled ? Qt.ArrowCursor : Qt.PointingHandCursor
                property bool isDisabled: appController ? appController.currentDay <= 1 : false
                onClicked: if (!isDisabled && appController) appController.previousDay()
            }
        }

        // Gün göstergesi
        Text {
            text: appController ? appController.currentDay + " / 30" : "1 / 30"
            font.family: Theme.latinFont
            font.pixelSize: Theme.titleFontSize
            font.bold: true
            color: Theme.lightGray
            horizontalAlignment: Text.AlignHCenter
        }

        // Sonraki Gün
        Rectangle {
            width: 110
            height: 40
            radius: Theme.buttonRadius
            color: nextArea.containsMouse && !nextArea.isDisabled
                   ? Qt.rgba(0.83, 0.69, 0.22, 0.2) : "transparent"
            border.color: nextArea.isDisabled ? Theme.mutedGray : Theme.gold
            border.width: 1.5
            opacity: nextArea.isDisabled ? 0.35 : 1.0

            RowLayout {
                anchors.centerIn: parent
                spacing: 4
                Text {
                    text: "Sonraki"
                    font.family: Theme.latinFont
                    font.pixelSize: Theme.bodyFontSize
                    color: Theme.gold
                }
                Text { text: "\u25BA"; font.pixelSize: 11; color: Theme.gold }
            }

            MouseArea {
                id: nextArea
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: isDisabled ? Qt.ArrowCursor : Qt.PointingHandCursor
                property bool isDisabled: appController ? appController.currentDay >= 30 : false
                onClicked: if (!isDisabled && appController) appController.nextDay()
            }
        }
    }
}
