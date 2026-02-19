import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    color: Theme.cardBg
    radius: Theme.cardRadius
    border.color: Theme.cardBorder
    border.width: 1
    clip: true
    implicitHeight: weatherCol.implicitHeight + Theme.cardPadding * 2

    visible: weatherModel && weatherModel.temperature !== ""

    ColumnLayout {
        id: weatherCol
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: Theme.cardPadding
        spacing: Theme.spacingSmall

        // ── Başlık ────────────────────────────────────────────────────────
        RowLayout {
            Layout.fillWidth: true
            spacing: 6

            Text {
                text: "Hava Durumu"
                font.family: Theme.latinFont
                font.pixelSize: Theme.badgeFontSize
                font.bold: true
                color: Theme.gold
                Layout.fillWidth: true
            }
            Text {
                text: weatherModel ? weatherModel.locationName : ""
                font.family: Theme.latinFont
                font.pixelSize: Theme.smallFontSize
                color: Theme.mutedGray
                elide: Text.ElideRight
                Layout.maximumWidth: 150
                visible: weatherModel && weatherModel.locationName !== ""
            }
        }

        Rectangle {
            Layout.fillWidth: true; height: 1; color: Theme.gold; opacity: 0.25
        }

        // ── İkon + Sıcaklık ──────────────────────────────────────────────
        RowLayout {
            Layout.fillWidth: true
            spacing: Theme.spacingMedium

            Text {
                text: weatherModel ? weatherModel.icon : ""
                font.pixelSize: 36
            }

            ColumnLayout {
                spacing: 2

                Text {
                    text: weatherModel ? weatherModel.description : ""
                    font.family: Theme.latinFont
                    font.pixelSize: Theme.bodyFontSize
                    color: Theme.lightGray
                }

                RowLayout {
                    spacing: Theme.spacingMedium

                    Text {
                        text: weatherModel ? weatherModel.temperature : ""
                        font.family: Theme.latinFont
                        font.pixelSize: Theme.titleFontSize
                        font.bold: true
                        color: Theme.white
                    }

                    Text {
                        text: weatherModel ? "Hissedilen: " + weatherModel.feelsLike : ""
                        font.family: Theme.latinFont
                        font.pixelSize: Theme.smallFontSize
                        color: Theme.mutedGray
                        visible: weatherModel && weatherModel.feelsLike !== ""
                    }
                }
            }

            Item { Layout.fillWidth: true }

            // Nem + Rüzgar
            ColumnLayout {
                spacing: 4

                RowLayout {
                    spacing: 6
                    Text { text: "\uD83D\uDCA7"; font.pixelSize: 14 }
                    Text {
                        text: weatherModel ? weatherModel.humidity : ""
                        font.family: Theme.latinFont
                        font.pixelSize: Theme.smallFontSize
                        color: Theme.lightGray
                    }
                }
                RowLayout {
                    spacing: 6
                    Text { text: "\uD83D\uDCA8"; font.pixelSize: 14 }
                    Text {
                        text: weatherModel ? weatherModel.windSpeed : ""
                        font.family: Theme.latinFont
                        font.pixelSize: Theme.smallFontSize
                        color: Theme.lightGray
                    }
                }
            }
        }
    }
}
