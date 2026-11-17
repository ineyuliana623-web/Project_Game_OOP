# Project UTS OOP - Game Pertarungan Karakter

Game pertarungan bergiliran sederhana menggunakan Python, Pygame, gambar kartun, dan konsep OOP.

NAMA: INE YULIANA
NIM: 14012500134
## Fitur
- Ksatria melawan Naga secara bergiliran.
- Tombol Serang, Bertahan, Item (+20 HP), dan Main Lagi.
- Bar HP dan pesan menang/kalah.
- Class `Karakter`, `Tombol`, dan `Game`.

## Materi OOP
- **Class:** `Karakter`, `Tombol`, dan `Game`.
- **Object:** `self.pemain` dan `self.musuh` adalah object dari class `Karakter`.
- **Constructor:** method `__init__()` mengatur data awal object.
- **Attribute:** `nama`, `hp`, `serangan`, `gambar`, dan lainnya.
- **Method:** `serang()`, `bertahan_diri()`, `gunakan_item()`, `gambar()`, dan `jalankan()`.

## Cara menjalankan di VS Code
1. Install Python di komputer.
2. Buka folder `Project_Game_OOP` di VS Code.
3. Buka Terminal > New Terminal.
4. Jalankan: `python -m pip install pygame`
5. Jalankan: `python game.py`

Jika perintah `python` tidak dikenali di Windows, coba `py -m pip install pygame` dan `py game.py`.

Pastikan file `game.py` dan folder `assets` berada di dalam folder project yang sama.
