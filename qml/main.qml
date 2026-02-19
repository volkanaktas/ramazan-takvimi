import QtQuick 2.15
import QtQuick.Controls 2.15
import "components"

ApplicationWindow {
    id: root
    title: "Ramazan Takvimi " + (appController ? appController.currentYear : "2026")
    width: 900
    height: 700
    minimumWidth: 720
    minimumHeight: 560
    visible: true

    // Koyu İslami arka plan gradyanı
    background: Rectangle {
        gradient: Gradient {
            GradientStop { position: 0.0; color: Theme.darkNavy }
            GradientStop { position: 1.0; color: Theme.deepTeal }
        }
    }

    // Cami silueti – dekoratif, altta
    Image {
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        source: "qrc:/assets/mosque_silhouette.svg"
        width: parent.width * 0.7
        fillMode: Image.PreserveAspectFit
        opacity: 0.08
        smooth: true
    }

    // Ana görünüm
    MainView {
        id: mainView
        anchors.fill: parent
        onSettingsRequested: settingsDialog.open()
    }

    // Yükleme animasyonu (en üstte)
    LoadingOverlay {
        anchors.fill: parent
        z: 100
    }

    // Ayarlar diyaloğu
    SettingsDialog {
        id: settingsDialog
    }
}
