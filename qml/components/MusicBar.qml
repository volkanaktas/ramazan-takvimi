import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    color: Theme.cardBg
    radius: 8
    border.color: Theme.cardBorder
    border.width: 1
    implicitHeight: 42

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 12
        spacing: 10

        Text { text: "\uD83C\uDFB5"; font.pixelSize: 14 }

        // Önceki
        Rectangle {
            width: 28; height: 28; radius: 14
            color: prevM.containsMouse ? Qt.rgba(1,1,1,0.1) : "transparent"
            Text { anchors.centerIn: parent; text: "\u23EE"; font.pixelSize: 13; color: Theme.mutedGray }
            MouseArea { id: prevM; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                onClicked: if (musicPlayer) musicPlayer.previousTrack() }
        }

        // Oynat / Duraklat
        Rectangle {
            width: 30; height: 30; radius: 15
            color: playM.containsMouse ? Qt.rgba(0.83,0.69,0.22,0.3) : Qt.rgba(0.83,0.69,0.22,0.15)
            border.color: Theme.gold; border.width: 1
            Text {
                anchors.centerIn: parent
                text: musicPlayer && musicPlayer.isPlaying ? "\u23F8" : "\u25B6"
                font.pixelSize: 13; color: Theme.gold
            }
            MouseArea { id: playM; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                onClicked: {
                    if (!musicPlayer) return
                    if (musicPlayer.isPlaying) musicPlayer.pause()
                    else musicPlayer.play()
                }
            }
        }

        // Sonraki
        Rectangle {
            width: 28; height: 28; radius: 14
            color: nextM.containsMouse ? Qt.rgba(1,1,1,0.1) : "transparent"
            Text { anchors.centerIn: parent; text: "\u23ED"; font.pixelSize: 13; color: Theme.mutedGray }
            MouseArea { id: nextM; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                onClicked: if (musicPlayer) musicPlayer.nextTrack() }
        }

        // Parça adı
        Text {
            Layout.fillWidth: true
            text: musicPlayer ? (musicPlayer.currentTrack !== "" ? musicPlayer.currentTrack : "—") : "—"
            font.family: Theme.latinFont
            font.pixelSize: Theme.smallFontSize
            color: Theme.mutedGray
            elide: Text.ElideRight
        }

        // Parça sayısı
        Text {
            text: musicPlayer ? musicPlayer.trackCount + " par\u00E7a" : ""
            font.family: Theme.latinFont
            font.pixelSize: Theme.smallFontSize
            color: Theme.mutedGray
            visible: musicPlayer && musicPlayer.trackCount > 0
        }
    }
}
