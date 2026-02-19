import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: hadithCard
    color: Theme.cardBg
    radius: Theme.cardRadius
    border.color: Theme.cardBorder
    border.width: 1
    clip: true
    implicitHeight: hadithCol.implicitHeight + Theme.cardPadding * 2

    // Sol altın çizgi
    Rectangle {
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        width: 3
        color: Theme.gold
        opacity: 0.7
    }

    ColumnLayout {
        id: hadithCol
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: Theme.cardPadding
        anchors.leftMargin: Theme.cardPadding + 8
        spacing: Theme.spacingMedium

        // Başlık
        RowLayout {
            Layout.fillWidth: true
            spacing: 8
            Text { text: "\u2726"; font.pixelSize: 14; color: Theme.gold }
            Text {
                text: "G\u00FCn\u00FCn Hadisi"
                font.family: Theme.latinFont
                font.pixelSize: Theme.badgeFontSize
                font.bold: true
                color: Theme.gold
            }
            Item { Layout.fillWidth: true }
            Text {
                visible: hadithModel && hadithModel.theme !== ""
                text: hadithModel ? hadithModel.theme : ""
                font.family: Theme.latinFont
                font.pixelSize: Theme.smallFontSize
                font.italic: true
                color: Theme.goldLight
                opacity: 0.8
                horizontalAlignment: Text.AlignRight
            }
        }

        // Hadis metni
        Text {
            Layout.fillWidth: true
            text: hadithModel
                  ? (hadithModel.text !== "" ? "\u201C" + hadithModel.text + "\u201D" : "Y\u00FCkleniyor...")
                  : "Y\u00FCkleniyor..."
            font.family: Theme.latinFont
            font.pixelSize: Theme.bodyFontSize
            color: Theme.lightGray
            wrapMode: Text.WordWrap
            lineHeight: 1.5
            font.italic: true
        }

        // Ravi ve kaynak
        RowLayout {
            Layout.fillWidth: true
            spacing: Theme.spacingSmall

            Text {
                visible: hadithModel && hadithModel.narrator !== ""
                text: hadithModel ? hadithModel.narrator : ""
                font.family: Theme.latinFont
                font.pixelSize: Theme.smallFontSize
                color: Theme.mutedGray
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
            }

            Text {
                visible: hadithModel && hadithModel.source !== ""
                text: hadithModel ? "\u2014 " + hadithModel.source : ""
                font.family: Theme.latinFont
                font.pixelSize: Theme.smallFontSize
                font.bold: true
                color: Theme.gold
                opacity: 0.9
                horizontalAlignment: Text.AlignRight
            }
        }
    }
}
