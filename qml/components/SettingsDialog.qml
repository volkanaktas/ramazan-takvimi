import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Popup {
    id: settingsDialog
    modal: true
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    anchors.centerIn: parent
    width: Math.min(580, parent ? parent.width * 0.92 : 580)
    padding: 0
    height: Math.min(settingsScroll.contentHeight + 48, parent ? parent.height * 0.92 : 700)

    // Konum verileri (JSON.parse ile doldurulur)
    property var countriesList: []
    property var citiesList: []
    property var districtsList: []

    // Seçili indeksler
    property int selCountryIdx: -1
    property int selCityIdx: -1
    property int selDistrictIdx: -1

    // Font ölçeği
    property string selectedFontScale: Theme ? Theme.fontScale : "medium"

    background: Rectangle {
        color: Theme.cardBg
        radius: Theme.cardRadius
        border.color: Theme.gold
        border.width: 1
    }

    // Konum sinyallerini dinle
    Connections {
        target: appController

        function onCountriesLoaded(json) {
            settingsDialog.countriesList = JSON.parse(json)
            // Kaydedilmiş ülkeyi bul
            var savedId = appController ? String(appController.districtId) : ""
            countryCombo.currentIndex = -1
            settingsDialog.selCountryIdx = -1
        }

        function onCitiesLoaded(json) {
            settingsDialog.citiesList = JSON.parse(json)
            cityCombo.currentIndex = -1
            settingsDialog.selCityIdx = -1
            settingsDialog.districtsList = []
            districtCombo.currentIndex = -1
        }

        function onDistrictsLoaded(json) {
            settingsDialog.districtsList = JSON.parse(json)
            districtCombo.currentIndex = -1
            settingsDialog.selDistrictIdx = -1
        }
    }

    onOpened: {
        if (settingsDialog.countriesList.length === 0)
            appController.loadCountries()
    }

    // ------------------------------------------------------------------ //
    ScrollView {
        id: settingsScroll
        anchors.fill: parent
        anchors.margins: 24
        clip: true
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

        ColumnLayout {
            width: settingsScroll.width - 2
            spacing: Theme.spacingMedium

            // Başlık
            RowLayout {
                Layout.fillWidth: true
                Text {
                    text: "\u2699  Ayarlar"
                    font.family: Theme.latinFont
                    font.pixelSize: Theme.titleFontSize
                    font.bold: true
                    color: Theme.gold
                    Layout.fillWidth: true
                }
                Rectangle {
                    width: 28; height: 28; radius: 14
                    color: closeH.containsMouse ? Qt.rgba(1,1,1,0.1) : "transparent"
                    Text { anchors.centerIn: parent; text: "\u2715"; color: Theme.mutedGray; font.pixelSize: 14 }
                    MouseArea { id: closeH; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                        onClicked: settingsDialog.close() }
                }
            }

            Rectangle { Layout.fillWidth: true; height: 1; color: Theme.gold; opacity: 0.3 }

            // ---- Kurum Adı ------------------------------------------ //
            SectionTitle { text: "Kurum Ad\u0131" }

            TextField {
                id: institutionField
                Layout.fillWidth: true
                placeholderText: "Kurumun/caminin ad\u0131..."
                text: appController ? appController.institutionName : ""
                font.family: Theme.latinFont
                font.pixelSize: Theme.bodyFontSize
                color: Theme.lightGray
                background: InputBg { active: institutionField.activeFocus }
                leftPadding: 10; rightPadding: 10
            }

            // ---- Veri Modu ------------------------------------------- //
            SectionTitle { text: "Veri Modu" }

            RowLayout {
                spacing: Theme.spacingMedium

                ModeButton {
                    label: "Statik (\u00C7evrimd\u0131\u015F\u0131)"
                    active: !dynToggle.checked
                    onActivate: dynToggle.checked = false
                }
                ModeButton {
                    label: "Dinamik (API)"
                    active: dynToggle.checked
                    onActivate: dynToggle.checked = true
                }
            }

            Switch { id: dynToggle; visible: false; checked: appController ? appController.isDynamicMode : false }

            // ---- API Token ------------------------------------------- //
            SectionTitle { text: "Diyanet API Token" }

            TextField {
                id: tokenField
                Layout.fillWidth: true
                placeholderText: "Bearer token girin..."
                text: appController ? appController.apiToken : ""
                font.family: Theme.latinFont
                font.pixelSize: Theme.bodyFontSize
                color: Theme.lightGray
                echoMode: TextInput.Password
                background: InputBg { active: tokenField.activeFocus }
                leftPadding: 10; rightPadding: 10
            }

            Text {
                text: "Statik modda token gerekmez."
                font.family: Theme.latinFont; font.pixelSize: Theme.smallFontSize
                color: Theme.mutedGray; Layout.fillWidth: true
            }

            Rectangle { Layout.fillWidth: true; height: 1; color: Theme.cardBorder }

            // ---- Namaz Vakitleri Konumu ------------------------------ //
            SectionTitle { text: "Namaz Vakitleri Konumu" }

            Text {
                text: "\u00dclke"
                font.family: Theme.latinFont; font.pixelSize: Theme.smallFontSize
                color: Theme.mutedGray
            }
            ComboBox {
                id: countryCombo
                Layout.fillWidth: true
                model: settingsDialog.countriesList
                textRole: "name"
                displayText: currentIndex >= 0 ? settingsDialog.countriesList[currentIndex].name : "Y\u00FCkleniyor..."
                font.family: Theme.latinFont
                font.pixelSize: Theme.bodyFontSize
                contentItem: Text {
                    leftPadding: 10
                    text: countryCombo.displayText
                    font: countryCombo.font
                    color: Theme.lightGray
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: "#0A2030"; radius: 6
                    border.color: countryCombo.activeFocus ? Theme.gold : Theme.mutedGray; border.width: 1
                }
                onCurrentIndexChanged: {
                    if (currentIndex >= 0 && settingsDialog.countriesList.length > currentIndex) {
                        settingsDialog.selCountryIdx = currentIndex
                        settingsDialog.citiesList = []
                        settingsDialog.districtsList = []
                        appController.loadCities(settingsDialog.countriesList[currentIndex].id)
                    }
                }
            }

            Text {
                text: "\u015eehir / \u0130l"
                font.family: Theme.latinFont; font.pixelSize: Theme.smallFontSize
                color: Theme.mutedGray
                visible: settingsDialog.citiesList.length > 0
            }
            ComboBox {
                id: cityCombo
                Layout.fillWidth: true
                visible: settingsDialog.citiesList.length > 0
                model: settingsDialog.citiesList
                textRole: "name"
                displayText: currentIndex >= 0 && settingsDialog.citiesList.length > currentIndex
                             ? settingsDialog.citiesList[currentIndex].name : "Se\u00E7iniz..."
                font.family: Theme.latinFont; font.pixelSize: Theme.bodyFontSize
                contentItem: Text {
                    leftPadding: 10; text: cityCombo.displayText
                    font: cityCombo.font; color: Theme.lightGray; verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: "#0A2030"; radius: 6
                    border.color: cityCombo.activeFocus ? Theme.gold : Theme.mutedGray; border.width: 1
                }
                onCurrentIndexChanged: {
                    if (currentIndex >= 0 && settingsDialog.citiesList.length > currentIndex) {
                        settingsDialog.selCityIdx = currentIndex
                        settingsDialog.districtsList = []
                        appController.loadDistricts(settingsDialog.citiesList[currentIndex].id)
                    }
                }
            }

            Text {
                text: "\u0130l\u00E7e"
                font.family: Theme.latinFont; font.pixelSize: Theme.smallFontSize
                color: Theme.mutedGray
                visible: settingsDialog.districtsList.length > 0
            }
            ComboBox {
                id: districtCombo
                Layout.fillWidth: true
                visible: settingsDialog.districtsList.length > 0
                model: settingsDialog.districtsList
                textRole: "name"
                displayText: currentIndex >= 0 && settingsDialog.districtsList.length > currentIndex
                             ? settingsDialog.districtsList[currentIndex].name : "Se\u00E7iniz..."
                font.family: Theme.latinFont; font.pixelSize: Theme.bodyFontSize
                contentItem: Text {
                    leftPadding: 10; text: districtCombo.displayText
                    font: districtCombo.font; color: Theme.lightGray; verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: "#0A2030"; radius: 6
                    border.color: districtCombo.activeFocus ? Theme.gold : Theme.mutedGray; border.width: 1
                }
                onCurrentIndexChanged: {
                    settingsDialog.selDistrictIdx = currentIndex
                }
            }

            Rectangle { Layout.fillWidth: true; height: 1; color: Theme.cardBorder }

            // ---- Font Boyutu ----------------------------------------- //
            SectionTitle { text: "Font Boyutu" }

            RowLayout {
                spacing: Theme.spacingMedium

                ModeButton {
                    id: fontScaleSmall
                    label: "K\u00FC\u00E7\u00FCk"
                    active: settingsDialog.selectedFontScale === "small"
                    onActivate: settingsDialog.selectedFontScale = "small"
                }
                ModeButton {
                    id: fontScaleMedium
                    label: "Orta"
                    active: settingsDialog.selectedFontScale === "medium"
                    onActivate: settingsDialog.selectedFontScale = "medium"
                }
                ModeButton {
                    id: fontScaleLarge
                    label: "B\u00FCy\u00FCk"
                    active: settingsDialog.selectedFontScale === "large"
                    onActivate: settingsDialog.selectedFontScale = "large"
                }
            }

            Rectangle { Layout.fillWidth: true; height: 1; color: Theme.cardBorder }

            // ---- Müzik Çalar ----------------------------------------- //
            SectionTitle { text: "M\u00FCzik \u00C7alar" }

            RowLayout {
                Layout.fillWidth: true
                spacing: Theme.spacingMedium

                ModeButton {
                    label: "Kapal\u0131"
                    active: !musicToggle.checked
                    onActivate: musicToggle.checked = false
                }
                ModeButton {
                    label: "A\u00E7\u0131k"
                    active: musicToggle.checked
                    onActivate: musicToggle.checked = true
                }
            }

            Switch {
                id: musicToggle
                visible: false
                checked: musicPlayer ? musicPlayer.isEnabled : false
            }

            Text {
                text: "M\u00FCzik Klas\u00F6r\u00FC"
                font.family: Theme.latinFont; font.pixelSize: Theme.smallFontSize
                color: Theme.mutedGray
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 8

                TextField {
                    id: musicFolderField
                    Layout.fillWidth: true
                    placeholderText: "Klas\u00F6r yolu se\u00E7iniz..."
                    text: musicPlayer ? musicPlayer.folder : ""
                    font.family: Theme.latinFont; font.pixelSize: Theme.bodyFontSize
                    color: Theme.lightGray; readOnly: true
                    background: InputBg { active: false }
                    leftPadding: 10; rightPadding: 10
                }

                // Gözat butonu
                Rectangle {
                    width: 80; height: 36; radius: 6
                    color: browseH.containsMouse ? Qt.rgba(0.83,0.69,0.22,0.3) : Qt.rgba(0.83,0.69,0.22,0.15)
                    border.color: Theme.gold; border.width: 1
                    Text { anchors.centerIn: parent; text: "G\u00F6zat..."; font.family: Theme.latinFont
                           font.pixelSize: Theme.smallFontSize; color: Theme.gold }
                    MouseArea { id: browseH; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            var folder = musicPlayer.browseFolder()
                            if (folder !== "") musicFolderField.text = folder
                        }
                    }
                }
            }

            Rectangle { Layout.fillWidth: true; height: 1; color: Theme.cardBorder }

            // ---- Kaydet Butonu --------------------------------------- //
            Rectangle {
                Layout.fillWidth: true
                height: 44
                radius: Theme.buttonRadius
                color: saveH.containsMouse ? Theme.gold : Qt.rgba(0.83, 0.69, 0.22, 0.85)
                Text {
                    anchors.centerIn: parent
                    text: "Kaydet ve Uygula"
                    font.family: Theme.latinFont; font.pixelSize: Theme.bodyFontSize; font.bold: true
                    color: Theme.darkNavy
                }
                MouseArea {
                    id: saveH; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        if (appController) {
                            appController.saveSettings(
                                dynToggle.checked,
                                tokenField.text,
                                institutionField.text,
                                settingsDialog.selectedFontScale
                            )
                            // Konum seçimi
                            if (settingsDialog.selDistrictIdx >= 0 &&
                                settingsDialog.districtsList.length > settingsDialog.selDistrictIdx) {
                                var d = settingsDialog.districtsList[settingsDialog.selDistrictIdx]
                                var cId = settingsDialog.selCountryIdx >= 0
                                          ? settingsDialog.countriesList[settingsDialog.selCountryIdx].id : ""
                                var sId = settingsDialog.selCityIdx >= 0
                                          ? settingsDialog.citiesList[settingsDialog.selCityIdx].id : ""
                                var cityName = settingsDialog.selCityIdx >= 0
                                              ? settingsDialog.citiesList[settingsDialog.selCityIdx].name : ""
                                var dispStr = cityName !== "" ? (cityName + " / " + d.name) : d.name
                                appController.saveDistrictSelection(cId, sId, d.id, dispStr)
                            }
                        }
                        // Müzik ayarları
                        if (musicPlayer) {
                            musicPlayer.setFolderPath(musicFolderField.text)
                            musicPlayer.setEnabled(musicToggle.checked)
                        }
                        settingsDialog.close()
                    }
                }
            }

            // Alt boşluk
            Item { height: 4 }
        }
    }
}
