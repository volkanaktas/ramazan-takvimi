; Ramazan Takvimi – Inno Setup Kurulum Scripti
; Gereksinim: Inno Setup 6 (https://jrsoftware.org/isinfo.php)
; Kullanım  : İscc.exe installer.iss  veya  Inno Setup IDE ile aç
; Ön koşul  : Önce "python build.py" çalıştırın.

#define AppName      "Ramazan Takvimi"
#define AppVersion   "1.0.0"
#define AppPublisher "Ramazan Takvimi"
#define AppExeName   "RamazanTakvimi.exe"
#define SourceDir    "dist\RamazanTakvimi"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL=https://ramazan.app
AppSupportURL=https://ramazan.app
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputDir=installer_output
OutputBaseFilename=RamazanTakvimi_Kurulum_v{#AppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ShowLanguageDialog=no
; UninstallDisplayIcon={app}\{#AppExeName}
; SetupIconFile=assets\icon.ico   ; .ico dosyası eklenirse etkinleştirin

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "Masaüstüne kısayol oluştur"; GroupDescription: "Ek görevler:"; Flags: unchecked
Name: "startmenuicon"; Description: "Başlat menüsüne ekle"; GroupDescription: "Ek görevler:"

[Files]
; Tüm uygulama dosyaları
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}";         Filename: "{app}\{#AppExeName}"
Name: "{group}\Kaldır";             Filename: "{uninstallexe}"
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; \
    Description: "Uygulamayı şimdi başlat"; \
    Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Uygulama tarafından oluşturulan cache ve config dosyalarını kaldır
Type: filesandordirs; Name: "{app}\cache"
Type: files;          Name: "{app}\config.json"
