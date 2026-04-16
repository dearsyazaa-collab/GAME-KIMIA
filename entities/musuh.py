import pygame

class Musuh:
    def __init__(self, x, y, lebar=60, tinggi=60, kecepatan=2):
        self.rect = pygame.Rect(x, y, lebar, tinggi)
        self.kecepatan_x = -kecepatan  # Default bergerak ke kiri
        self.kecepatan_y = 0
        self.on_ground = False
        self.gravitasi = 0.8

    def update(self, daftar_pijakan, lebar_layar):
        # 1. Terapkan Gravitasi
        if not self.on_ground:
            self.kecepatan_y += self.gravitasi
        else:
            self.kecepatan_y = 0
            
        self.rect.y += self.kecepatan_y
        
        # 2. Collision dengan Pijakan (Deteksi Berpijak)
        self.on_ground = False
        for pijakan in daftar_pijakan:
            if self.rect.colliderect(pijakan):
                # Jika jatuh menimpa pijakan
                if self.kecepatan_y > 0 and self.rect.bottom <= pijakan.bottom:
                    self.rect.bottom = pijakan.top
                    self.on_ground = True
                    self.kecepatan_y = 0

        # 3. Gerakan Horizontal
        self.rect.x += self.kecepatan_x
        
        # 4. AI: Balik arah jika menabrak batas layar
        if self.rect.left <= 0 or self.rect.right >= lebar_layar:
            self.kecepatan_x *= -1
            
        # 5. AI: Balik arah jika di ujung platform (Edge Detection)
        # Cek apakah masih ada pijakan di bawah kaki musuh ke arah gerakannya
        pijakan_di_bawah = False
        # Prediksi posisi di depan musuh (misal 10 pixel di depan bawah)
        cek_x = self.rect.left if self.kecepatan_x < 0 else self.rect.right
        cek_y = self.rect.bottom + 5
        
        for pijakan in daftar_pijakan:
            if pijakan.collidepoint(cek_x, cek_y):
                pijakan_di_bawah = True
                break
        
        # Jika tidak ada pijakan di depan dan musuh sedang di tanah, balik arah
        if not pijakan_di_bawah and self.on_ground:
            self.kecepatan_x *= -1

    def draw(self, surface):
        # Menggunakan warna merah sebagai placeholder
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        # Detail kecil agar terlihat arahnya (mata)
        mata_x = self.rect.x + 10 if self.kecepatan_x < 0 else self.rect.x + self.rect.width - 20
        pygame.draw.rect(surface, (255, 255, 255), (mata_x, self.rect.y + 10, 10, 10))
