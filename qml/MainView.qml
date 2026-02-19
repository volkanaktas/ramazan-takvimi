import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "components"

Item {
    id: mainView

    signal settingsRequested()

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: Theme.spacingLarge
        spacing: Theme.spacingSmall

        // Hata / çevrimdışı banner'ı
        ErrorBanner {
            Layout.fillWidth: true
        }

        // Başlık
        AppHeader {
            Layout.fillWidth: true
            onSettingsClicked: mainView.settingsRequested()
        }

        GoldDivider {
            Layout.fillWidth: true
        }

        // Kaydırılabilir içerik
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

            ColumnLayout {
                width: mainView.width - Theme.spacingLarge * 2
                spacing: Theme.spacingMedium

                // Ayet kartı (yükseklik otomatik)
                VerseCard {
                    Layout.fillWidth: true
                }

                // Hadis kartı (yükseklik otomatik)
                HadithCard {
                    Layout.fillWidth: true
                }

                // Alt satır: Yemek + Namaz vakitleri
                RowLayout {
                    Layout.fillWidth: true
                    spacing: Theme.spacingMedium

                    MealCard {
                        Layout.fillWidth: true
                        Layout.preferredWidth: 1
                    }

                    PrayerTimesCard {
                        Layout.fillWidth: true
                        Layout.preferredWidth: 1
                    }
                }

                // Hava durumu
                WeatherCard {
                    Layout.fillWidth: true
                }

                // Müzik çalar mini bar
                MusicBar {
                    Layout.fillWidth: true
                    visible: musicPlayer ? musicPlayer.isEnabled : false
                }

                Item { height: Theme.spacingMedium }
            }
        }

        GoldDivider {
            Layout.fillWidth: true
        }

        DayNavigator {
            Layout.fillWidth: true
        }
    }
}
