import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    color: Theme.cardBg
    radius: Theme.cardRadius
    border.color: Theme.cardBorder
    border.width: 1
    implicitHeight: mealCol.implicitHeight + Theme.cardPadding * 2

    ColumnLayout {
        id: mealCol
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: Theme.cardPadding
        spacing: Theme.spacingSmall

        // Başlık
        RowLayout {
            Layout.fillWidth: true
            spacing: 8
            Text { text: "\uD83C\uDF7D"; font.pixelSize: 15 }
            Text {
                text: "\u0130ftar \u00D6nerisi"
                font.family: Theme.latinFont
                font.pixelSize: Theme.badgeFontSize
                font.bold: true
                color: Theme.gold
            }
        }

        // Özel not
        Text {
            visible: mealModel && mealModel.note !== ""
            text: mealModel ? mealModel.note : ""
            font.family: Theme.latinFont
            font.pixelSize: Theme.smallFontSize
            font.bold: true
            color: Theme.goldLight
            font.italic: true
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
        }

        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: Theme.gold
            opacity: 0.25
        }

        // Çorba
        MealRow {
            Layout.fillWidth: true
            icon: "\uD83E\uDD63"
            label: "\u00C7orba"
            value: mealModel ? mealModel.soup : ""
        }

        // Ana Yemek
        MealRow {
            Layout.fillWidth: true
            icon: "\uD83C\uDF56"
            label: "Ana Yemek"
            value: mealModel ? mealModel.mainCourse : ""
        }

        // Tatlı
        MealRow {
            Layout.fillWidth: true
            icon: "\uD83C\uDF6E"
            label: "Tatl\u0131"
            value: mealModel ? mealModel.dessert : ""
        }
    }
}
