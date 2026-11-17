import pygame
import sys
import math

# ==================================================
# PROJECT UTS OOP: FANTASY BATTLE
# Nama : Ine Yuliana
# NIM  : 14012500134
# ==================================================

pygame.init()

LEBAR, TINGGI = 1000, 600
LAYAR = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Fantasy Battle - Pink Princess Edition")
JAM = pygame.time.Clock()

# Warna tema pink dan ungu
PUTIH = (255, 255, 255)
PINK = (245, 125, 180)
PINK_MUDA = (255, 190, 220)
PINK_TUA = (190, 75, 140)
LAVENDER = (205, 175, 235)
UNGU = (145, 105, 185)
UNGU_TUA = (65, 40, 95)
UNGU_GELAP = (40, 25, 65)
BIRU = (105, 145, 220)
HIJAU = (100, 185, 140)
KUNING = (255, 225, 150)

# Font
font_judul = pygame.font.SysFont("georgia", 36, bold=True)
font_besar = pygame.font.SysFont("georgia", 27, bold=True)
font_sedang = pygame.font.SysFont("arial", 20, bold=True)
font_kecil = pygame.font.SysFont("arial", 15)

# Memuat gambar dari folder assets (ditambahkan .convert_alpha() agar background transparan)
LATAR = pygame.image.load(
    "assets/background.jpeg"
).convert()

LATAR = pygame.transform.smoothscale(
    LATAR, (LEBAR, TINGGI)
)

GAMBAR_HERO = pygame.image.load(
    "assets/hero.png"
).convert_alpha()

GAMBAR_NAGA = pygame.image.load(
    "assets/dragon.png"
).convert_alpha()

GAMBAR_HERO = pygame.transform.smoothscale(
    GAMBAR_HERO, (200, 230)
)

GAMBAR_NAGA = pygame.transform.smoothscale(
    GAMBAR_NAGA, (230, 230)
)


def tulis(teks, font, warna, posisi):
    gambar = font.render(teks, True, warna)
    kotak = gambar.get_rect(center=posisi)
    LAYAR.blit(gambar, kotak)


def gambar_panel(kotak, warna, radius=18):
    pygame.draw.rect(
        LAYAR, UNGU_GELAP, kotak, border_radius=radius
    )
    pygame.draw.rect(
        LAYAR, PINK_MUDA, kotak, 2, border_radius=radius
    )


class Karakter:
    """Class untuk membuat karakter dalam permainan."""

    def __init__(self, nama, hp, serangan, gambar):
        self.nama = nama
        self.hp = hp
        self.hp_maks = hp
        self.serangan = serangan
        self.gambar = gambar
        self.bertahan = False

    def serang(self, lawan):
        damage = self.serangan

        if lawan.bertahan:
            damage = max(1, damage // 2)
            lawan.bertahan = False
            pesan = f"{lawan.nama} berhasil bertahan!"
        else:
            pesan = f"{self.nama} menyerang {lawan.nama}!"

        lawan.hp = max(0, lawan.hp - damage)

        return f"{pesan} Damage: {damage}"

    def bertahan_diri(self):
        self.bertahan = True
        return f"{self.nama} bersiap untuk bertahan!"

    def gunakan_item(self):
        hp_sebelum = self.hp
        self.hp = min(self.hp_maks, self.hp + 20)
        pulih = self.hp - hp_sebelum

        return f"{self.nama} memulihkan {pulih} HP!"


class Tombol:
    """Class untuk membuat tombol permainan."""

    def __init__(self, teks, x, y, lebar, tinggi, warna):
        self.teks = teks
        self.rect = pygame.Rect(x, y, lebar, tinggi)
        self.warna = warna

    def gambar(self, posisi_mouse):
        warna = self.warna

        # Efek ketika mouse diarahkan ke tombol
        if self.rect.collidepoint(posisi_mouse):
            warna = tuple(
                min(255, nilai + 30) for nilai in warna
            )

        pygame.draw.rect(
            LAYAR, UNGU_GELAP, self.rect.move(0, 4),
            border_radius=16
        )

        pygame.draw.rect(
            LAYAR, warna, self.rect,
            border_radius=16
        )

        pygame.draw.rect(
            LAYAR, PUTIH, self.rect, 2,
            border_radius=16
        )

        tulis(
            self.teks,
            font_sedang,
            PUTIH,
            self.rect.center
        )

    def diklik(self, posisi_mouse):
        return self.rect.collidepoint(posisi_mouse)


class Game:
    """Class utama untuk mengatur permainan."""

    def __init__(self):
        self.pemain = Karakter(
            "Ksatria", 100, 22, GAMBAR_HERO
        )

        self.musuh = Karakter(
            "Naga", 110, 17, GAMBAR_NAGA
        )

        self.hero_x = 85
        self.hero_y = 175

        self.giliran_pemain = True
        self.game_selesai = False
        self.waktu_pesan = 0

        self.pesan = "Selamat datang, Ksatria! Siap bertarung?"

        self.waktu_efek = 0
        self.target_efek = ""

        # Membuat tombol permainan
        self.tombol_serang = Tombol(
            "SERANG", 55, 515, 195, 60, PINK_TUA
        )

        self.tombol_bertahan = Tombol(
            "BERTAHAN", 275, 515, 195, 60, BIRU
        )

        self.tombol_item = Tombol(
            "ITEM +20 HP", 495, 515, 195, 60, HIJAU
        )

        self.tombol_reset = Tombol(
            "MAIN LAGI", 715, 515, 230, 60, UNGU
        )

    # Menggerakkan Ksatria dengan tombol panah
    def gerakkan_pemain(self, tombol):
        if self.game_selesai:
            return

        kecepatan = 15

        if tombol == pygame.K_LEFT:
            self.hero_x -= kecepatan
        elif tombol == pygame.K_RIGHT:
            self.hero_x += kecepatan
        elif tombol == pygame.K_UP:
            self.hero_y -= kecepatan
        elif tombol == pygame.K_DOWN:
            self.hero_y += kecepatan

        self.hero_x = max(0, min(self.hero_x, 400))
        self.hero_y = max(145, min(self.hero_y, 230))

    # Mengatur aksi pemain
    def aksi_pemain(self, aksi):
        if self.game_selesai or not self.giliran_pemain:
            return

        if aksi == "serang":
            self.pesan = self.pemain.serang(self.musuh)
            self.target_efek = "naga"
            self.waktu_efek = pygame.time.get_ticks() + 400

        elif aksi == "bertahan":
            self.pesan = self.pemain.bertahan_diri()

        elif aksi == "item":
            self.pesan = self.pemain.gunakan_item()

        if self.musuh.hp <= 0:
            self.pesan = "Hebat! Kamu berhasil mengalahkan Naga!"
            self.game_selesai = True
        else:
            self.giliran_pemain = False
            self.waktu_pesan = pygame.time.get_ticks() + 700

    # Mengatur giliran Naga
    def giliran_musuh(self):
        if self.game_selesai or self.giliran_pemain:
            return

        if pygame.time.get_ticks() >= self.waktu_pesan:
            self.pesan = self.musuh.serang(self.pemain)

            self.target_efek = "ksatria"
            self.waktu_efek = pygame.time.get_ticks() + 400

            if self.pemain.hp <= 0:
                self.pesan = "Ksatria kalah! Coba main lagi!"
                self.game_selesai = True
            else:
                self.giliran_pemain = True
                self.pesan += " Giliranmu!"

    # Menggambar HP karakter
    def gambar_hp(self, x, y, karakter, warna):
        pygame.draw.rect(
            LAYAR, UNGU_GELAP,
            (x, y, 300, 23),
            border_radius=12
        )

        panjang = int(
            294 * karakter.hp / karakter.hp_maks
        )

        if panjang > 0:
            pygame.draw.rect(
                LAYAR, warna,
                (x + 3, y + 3, panjang, 17),
                border_radius=10
            )

        tulis(
            f"{karakter.nama}  {karakter.hp}/{karakter.hp_maks} HP",
            font_kecil,
            PUTIH,
            (x + 150, y - 12)
        )

    # Menggambar efek serangan
    def gambar_efek(self):
        sisa = self.waktu_efek - pygame.time.get_ticks()

        if sisa > 0:
            if self.target_efek == "naga":
                posisi = (760, 290)
            else:
                posisi = (180, 290)

            ukuran = 25 + int((400 - sisa) / 8)

            efek = pygame.Surface(
                (LEBAR, TINGGI), pygame.SRCALPHA
            )

            pygame.draw.circle(
                efek,
                (255, 190, 220, 160),
                posisi,
                ukuran,
                5
            )

            LAYAR.blit(efek, (0, 0))

    # Menggambar bintang dekorasi
    def gambar_dekorasi(self):
        titik = [
            (45, 205), (180, 95), (350, 155),
            (510, 180), (830, 195), (950, 260),
            (70, 390), (920, 390)
        ]

        for x, y in titik:
            pygame.draw.circle(
                LAYAR, PINK_MUDA, (x, y), 3
            )

    # Menggambar tampilan permainan
    def gambar(self):
        LAYAR.blit(LATAR, (0, 0))

        # Lapisan warna ungu transparan
        lapisan = pygame.Surface(
            (LEBAR, TINGGI), pygame.SRCALPHA
        )
        lapisan.fill((55, 25, 75, 65))
        LAYAR.blit(lapisan, (0, 0))

        self.gambar_dekorasi()

        # Judul permainan
        gambar_panel(
            (240, 10, 520, 65),
            UNGU_GELAP
        )

        tulis(
            "FANTASY BATTLE",
            font_judul,
            PINK_MUDA,
            (500, 43)
        )

        tulis(
            "KSATRIA  VS  NAGA",
            font_sedang,
            KUNING,
            (500, 88)
        )

        # Panel HP pemain
        gambar_panel(
            (25, 95, 420, 70),
            UNGU_TUA
        )

        self.gambar_hp(
            85, 132, self.pemain, PINK
        )

        # Panel HP musuh
        gambar_panel(
            (555, 95, 420, 70),
            UNGU_TUA
        )

        self.gambar_hp(
            615, 132, self.musuh, HIJAU
        )

        # Gambar karakter
        LAYAR.blit(
            self.pemain.gambar,
            (self.hero_x, self.hero_y)
        )

        LAYAR.blit(
            self.musuh.gambar,
            (650, 175)
        )

        # Nama karakter
        tulis(
            "KSATRIA",
            font_besar,
            PUTIH,
            (185, 405)
        )

        tulis(
            "NAGA",
            font_besar,
            PUTIH,
            (765, 405)
        )

        # Panel pesan
        gambar_panel(
            (130, 425, 740, 55),
            UNGU_GELAP
        )

        tulisan_pesan = font_sedang.render(
            self.pesan, True, KUNING
        )

        if tulisan_pesan.get_width() > 700:
            tulisan_pesan = pygame.transform.smoothscale(
                tulisan_pesan,
                (700, tulisan_pesan.get_height())
            )

        LAYAR.blit(
            tulisan_pesan,
            tulisan_pesan.get_rect(center=(500, 452))
        )

        # Petunjuk keyboard
        tulis(
            "Gunakan tombol PANAH untuk menggerakkan Ksatria",
            font_kecil,
            PUTIH,
            (500, 493)
        )

        # Efek serangan
        self.gambar_efek()

        # Tampilan menang atau kalah
        if self.game_selesai:
            penutup = pygame.Surface(
                (LEBAR, TINGGI), pygame.SRCALPHA
            )

            penutup.fill((35, 20, 55, 190))
            LAYAR.blit(penutup, (0, 0))

            gambar_panel(
                (250, 190, 500, 200),
                UNGU_GELAP
            )

            if self.musuh.hp <= 0:
                judul = "KAMU MENANG!"
                keterangan = "Naga berhasil dikalahkan!"
            else:
                judul = "KAMU KALAH!"
                keterangan = "Jangan menyerah, coba lagi!"

            tulis(
                judul,
                font_judul,
                KUNING,
                (500, 250)
            )

            tulis(
                keterangan,
                font_sedang,
                PUTIH,
                (500, 300)
            )

            tulis(
                "Klik MAIN LAGI untuk mengulang",
                font_kecil,
                PINK_MUDA,
                (500, 345)
            )

        # Tombol tetap terlihat
        posisi_mouse = pygame.mouse.get_pos()

        if not self.game_selesai:
            self.tombol_serang.gambar(posisi_mouse)
            self.tombol_bertahan.gambar(posisi_mouse)
            self.tombol_item.gambar(posisi_mouse)

        self.tombol_reset.gambar(posisi_mouse)

    # Mengulang permainan
    def reset(self):
        self.__init__()

    # Menjalankan permainan
    def jalankan(self):
        berjalan = True

        while berjalan:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    berjalan = False

                # Kontrol keyboard
                if event.type == pygame.KEYDOWN:
                    self.gerakkan_pemain(event.key)

                # Kontrol mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        posisi = event.pos

                        if self.tombol_reset.diklik(posisi):
                            self.reset()

                        elif self.giliran_pemain and not self.game_selesai:

                            if self.tombol_serang.diklik(posisi):
                                self.aksi_pemain("serang")

                            elif self.tombol_bertahan.diklik(posisi):
                                self.aksi_pemain("bertahan")

                            elif self.tombol_item.diklik(posisi):
                                self.aksi_pemain("item")

            self.giliran_musuh()
            self.gambar()

            pygame.display.flip()
            JAM.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.jalankan()