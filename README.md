# ☪️ Ramazan Takvimi 1446 / 2026

Python 3.12 + PySide6 + QML ile geliştirilmiş, Windows için masaüstü Ramazan takvimi uygulaması.

---

## 📸 Özellikler

| Özellik | Açıklama |
|---------|----------|
| 📖 Günün Ayeti | Arapça metin + Türkçe meal, sure/ayet referansı |
| 📜 Günün Hadisi | Hadis metni, ravi ve kaynak bilgisi |
| 🕌 Namaz Vakitleri | Diyanet API veya statik mod; konum seçilebilir |
| 🍽️ İftar Önerisi | Günlük çorba, ana yemek, tatlı önerisi |
| ⛅ Hava Durumu | Open-Meteo (ücretsiz, API anahtarsız) |
| 🎵 Müzik Çalar | MP3 klasörü seçimi, otomatik sıra |
| ⚙️ Ayarlar | Font boyutu, kurum adı, konum, veri modu |
| 📅 Gün Navigasyonu | 1–30. gün arası ileri/geri gezinme |

---

## 🖥️ Ekran Görüntüsü

```
┌─────────────────────────────────────────────────────────┐
│ ☪ Ramazan Takvimi 2026   Kurum Adı       2. Gün  ⚙️    │
│━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│
│  📖 Günün Ayeti                    Bakara 2:185         │
│  ┌─────────────────────────────────────────────────┐    │
│  │  شَهۡرُ رَمَضَانَ ٱلَّذِيٓ أُنزِلَ فِيهِ ...  │    │
│  │  Ramazan ayı, Kur'an'ın indirildiği aydır...    │    │
│  └─────────────────────────────────────────────────┘    │
│  📜 Günün Hadisi   ...                                   │
│  🍽️ İftar Önerisi  |  🕌 Namaz Vakitleri               │
│  ⛅ Hava Durumu – Mersin / Merkez   18°C Parçalı Bulutlu │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Kurulum

### Hazır Kurulum (Windows)

1. [Releases](https://github.com/volkanaktas/ramazan-takvimi/releases) sayfasından `RamazanTakvimi_Kurulum_vX.X.X.exe` dosyasını indirin.
2. Kurulum sihirbazını çalıştırın.
3. Uygulamayı başlatın.

### Kaynak Koddan Çalıştırma

**Gereksinimler:** Python 3.12+

```bash
# Depoyu klonlayın
git clone https://github.com/volkanaktas/ramazan-takvimi.git
cd ramazan-takvimi

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Yapılandırmayı oluşturun
copy config.example.json config.json

# Uygulamayı başlatın
python main.py
```

---

## ⚙️ Yapılandırma

`config.example.json` dosyasını `config.json` olarak kopyalayıp düzenleyin:

```json
{
  "api_token": "BURAYA_DIYANET_API_TOKEN_GIRIN",
  "dynamic_mode": false,
  "ramadan_start": "2026-02-18",
  "ilce_id": "9737",
  "ulke_id": "2",
  "sehir_id": "557",
  "location_display": "Mersin / Merkez",
  "institution_name": "Kurumunuzun Adı",
  "font_scale": "medium",
  "lat": 36.8,
  "lon": 34.64
}
```

| Alan | Açıklama |
|------|----------|
| `api_token` | Diyanet API token (dinamik mod için) |
| `dynamic_mode` | `true` = API'dan çek, `false` = statik veriler |
| `font_scale` | `"small"` / `"medium"` / `"large"` |
| `institution_name` | Başlıkta görünen kurum/cami adı |
| `lat`, `lon` | Hava durumu için koordinat |

---

## 🏗️ Proje Yapısı

```
ramazan-takvimi/
├── main.py                  # Uygulama giriş noktası
├── app/
│   ├── app_controller.py    # QML ↔ Python köprüsü
│   ├── theme_provider.py    # Tema renk ve font sistemi
│   ├── music_player.py      # MP3 çalar
│   ├── settings_manager.py  # config.json okuma/yazma
│   └── cache_manager.py     # API önbelleği
├── models/                  # QML veri modelleri
│   ├── verse_model.py
│   ├── hadith_model.py
│   ├── prayer_model.py
│   ├── meal_model.py
│   └── weather_model.py
├── services/                # Veri servisleri
│   ├── prayer_service.py    # Diyanet namaz vakitleri
│   ├── quran_service.py     # Ayet servisi
│   ├── hadith_service.py    # Hadis servisi
│   ├── weather_service.py   # Open-Meteo hava durumu
│   └── data_loader.py       # Async veri yükleyici
├── data/                    # Statik veriler (çevrimdışı mod)
│   ├── static_verses.py
│   ├── static_hadiths.py
│   └── static_meals.py
├── qml/                     # Kullanıcı arayüzü (QML)
│   ├── main.qml
│   ├── MainView.qml
│   ├── theme/Theme.qml
│   └── components/          # Yeniden kullanılabilir bileşenler
├── assets/
├── build.py                 # PyInstaller build scripti
├── ramazan.spec             # PyInstaller spec dosyası
├── installer.iss            # Inno Setup kurulum scripti
└── requirements.txt
```

---

## 📦 Dağıtım (Build)

**Gereksinimler:** PyInstaller 6+, Inno Setup 6 (Windows)

```bash
# EXE oluştur (dist/RamazanTakvimi/)
python build.py

# Kurulum .exe oluştur
"C:\Users\...\Inno Setup 6\ISCC.exe" installer.iss
# Çıktı: installer_output/RamazanTakvimi_Kurulum_v1.0.0.exe
```

---

## 🌐 Kullanılan API'lar

| Servis | URL | Açıklama |
|--------|-----|----------|
| Diyanet API | `awqatsalah.diyanet.gov.tr` | Namaz vakitleri |
| Open-Meteo | `api.open-meteo.com` | Hava durumu (ücretsiz) |
| Open-Meteo Geocoding | `geocoding-api.open-meteo.com` | Konum koordinatı |

---

## 🛠️ Teknolojiler

- **Python 3.12**
- **PySide6 6.7** – Qt for Python (QML, Multimedia, Network)
- **QtQuick Controls 2** – Arayüz bileşenleri
- **Amiri** – Arapça font
- **Noto Sans** – Latin font
- **PyInstaller 6** – Uygulama paketleme
- **Inno Setup 6** – Windows kurulum oluşturucu

---

## 📄 Lisans

Bu proje eğitim ve kamu yararı amacıyla geliştirilmiştir.
