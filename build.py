"""
Ramazan Takvimi – Build Scripti
Kullanım: python build.py
Çıktı:    dist/RamazanTakvimi/RamazanTakvimi.exe
"""

import os
import sys
import shutil
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))


def run(cmd: list) -> None:
    print(f"\n>>> {' '.join(cmd)}\n")
    result = subprocess.run(cmd, cwd=BASE)
    if result.returncode != 0:
        print(f"\nHATA: Komut başarısız oldu (kod {result.returncode})")
        sys.exit(result.returncode)


def clean() -> None:
    for folder in ("build", os.path.join("dist", "RamazanTakvimi")):
        full = os.path.join(BASE, folder)
        if os.path.exists(full):
            shutil.rmtree(full)
            print(f"Temizlendi: {folder}")


def copy_runtime_files() -> None:
    """Build sonrası dist klasörüne çalışma zamanı dosyalarını kopyala."""
    dist = os.path.join(BASE, "dist", "RamazanTakvimi")

    # cache klasörü (uygulama ilk çalışmada oluşturur, boş olarak ekle)
    cache_dir = os.path.join(dist, "cache")
    os.makedirs(cache_dir, exist_ok=True)

    print("Çalışma zamanı dosyaları kopyalandı.")


def main() -> None:
    print("=" * 60)
    print("  Ramazan Takvimi – PyInstaller Build")
    print("=" * 60)

    clean()

    run([sys.executable, "-m", "PyInstaller", "ramazan.spec", "--clean"])

    copy_runtime_files()

    dist_path = os.path.join(BASE, "dist", "RamazanTakvimi")
    exe_path  = os.path.join(dist_path, "RamazanTakvimi.exe")

    print("\n" + "=" * 60)
    if os.path.isfile(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"  BUILD BAŞARILI")
        print(f"  Konum : {dist_path}")
        print(f"  EXE   : RamazanTakvimi.exe  ({size_mb:.1f} MB)")
        print(f"\n  Kurulum için: python build_installer.py")
    else:
        print("  BUILD BAŞARISIZ – EXE bulunamadı.")
    print("=" * 60)


if __name__ == "__main__":
    main()
