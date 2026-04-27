import pygame
from entities.items import Atom, AltarReaksi, Obstacle

def get_level_data(level_number):
    if level_number == 1:
        # Transisi Level 1: Pengenalan Ikatan Ion
        # Edukasi: Pemain belajar bagaimana Na (Natrium) melepas elektron dan Cl (Klorin) menerimanya untuk membentuk ikatan ion pada garam dapur (NaCl).
        return {
            "platforms": [
                pygame.Rect(0, 600, 2000, 100),
                pygame.Rect(2300, 500, 2000, 100), # Gap 300
                pygame.Rect(4600, 500, 1500, 100), # Gap 300
                pygame.Rect(6400, 500, 1500, 100), # Gap 300
            ],
            "obstacles": [
                {"type": "KAYU", "x": 1200, "y": 550, "width": 50, "height": 50},
                {"type": "KAYU", "x": 2800, "y": 450, "width": 50, "height": 50},
                {"type": "SUNGAI_BERACUN", "x": 4200, "y": 620, "width": 500, "height": 80},
                {"type": "KAYU", "x": 5800, "y": 450, "width": 50, "height": 50}
            ],
            "items": [
                {"type": "Na", "x": 800, "y": 550, "fact_text": "Atom Na punya 1 elektron luar. Ia tidak sabar untuk 'membuang' 1 elektron agar stabil seperti Gas Mulia!"},
                {"type": "Cl", "x": 3500, "y": 450, "fact_text": "Atom Cl punya 7 elektron luar. Dia sangat agresif 'merampas' 1 elektron dari unsur lain agar stabil seperti Gas Mulia!"},
                {"type": "KUIS", "x": 5500, "y": 450,
                 "question": "Unsur Na (Golongan IA) agar stabil mencapai aturan Oktet, akan cenderung melakukan apa?",
                 "options": ["A. Melepas 1 elektron", "B. Menerima 1 elektron", "C. Membentuk ikatan kovalen"],
                 "correct_idx": 0,
                 "explanation": "Na memiliki elektron valensi 1. Energi ionisasinya rendah sehingga lebih mudah melepas 1 elektron menjadi ion Na+."},
            ],
            "altar": {
                "x": 7200, "y": 450,
                "target_formula": {"Na": 1, "Cl": 1},
                "result_name": "NaCl",
                "result_fact": "Natrium (Na) [2.8.1] melepas 1 elektron karena Energi Ionisasinya rendah (Sifat Periodik Logam Alkali). Klorin (Cl) [2.8.7] menangkap elektron tersebut karena Afinitas Elektronnya tinggi. Gaya elektrostatik menyatukan ion Na+ dan Cl- menjadi Garam Dapur padat."
            },
            "enemies": [
                {"x": 1200, "y": 550, "range": 150},
                {"x": 3200, "y": 450, "range": 200},
                {"x": 5000, "y": 450, "range": 150}
            ]
        }
    elif level_number == 2:
        # Transisi Level 2: Pengenalan Ikatan Kovalen
        # Edukasi: Pemain belajar bagaimana dua atom H berbagi elektron dengan satu atom O untuk membentuk ikatan kovalen pada Air (H2O).
        return {
            "platforms": [
                pygame.Rect(0, 600, 2000, 100),
                pygame.Rect(2300, 500, 1500, 100), # Gap 300
                pygame.Rect(4100, 550, 1500, 100), # Gap 300
                pygame.Rect(5900, 500, 2000, 100)  # Gap 300
            ],
            "obstacles": [
                {"type": "SUNGAI_BERACUN", "x": 1800, "y": 620, "width": 500, "height": 80},
                {"type": "KAYU", "x": 2800, "y": 450, "width": 50, "height": 50},
                {"type": "KAYU", "x": 4500, "y": 500, "width": 50, "height": 50},
                {"type": "SUNGAI_BERACUN", "x": 5500, "y": 670, "width": 400, "height": 80}
            ],
            "items": [
                {"type": "H", "x": 800, "y": 550, "fact_text": "Atom H butuh 1 elektron lagi (Duplet). Walaupun kecil, dia siap 'berbagi' elektron untuk berikatan Kovalen!"},
                {"type": "O", "x": 2800, "y": 400, "fact_text": "Atom O butuh 2 elektron lagi (Oktet). Dia suka 'berbagi' dengan 2 atom H untuk membentuk Air!"},
                {"type": "H", "x": 4800, "y": 500, "fact_text": "Atom H butuh 1 elektron lagi (Duplet). Walaupun kecil, dia siap 'berbagi' elektron untuk berikatan Kovalen!"},
                {"type": "KUIS", "x": 6500, "y": 450,
                 "question": "Oksigen (O) memiliki 6 elektron valensi. Untuk stabil, ia akan...",
                 "options": ["A. Melepas 2 elektron", "B. Menerima 2 e- / Berbagi 2 e-", "C. Membentuk ion positif"],
                 "correct_idx": 1,
                 "explanation": "Oksigen (O) kurang 2 elektron untuk oktet. Ia cenderung menerima 2 elektron atau membentuk 2 ikatan kovalen."},
            ],
            "altar": {
                "x": 7500, "y": 450,
                "target_formula": {"H": 2, "O": 1},
                "result_name": "H2O",
                "result_fact": "Oksigen (O) [2.6] butuh 2 elektron. Hidrogen (H) [1] butuh 1 elektron. Mereka melakukan PENGGUNAAN BERSAMA elektron membentuk Ikatan Kovalen Polar. Adanya 2 Pasangan Elektron Bebas (PEB) pada Oksigen menolak ikatan H, membuat bentuk molekul Air menjadi V-Shape/Bengkok."
            },
            "enemies": [
                {"x": 2500, "y": 450, "range": 150},
                {"x": 4500, "y": 500, "range": 200},
                {"x": 6000, "y": 450, "range": 200}
            ]
        }
    elif level_number == 3:
        # Transisi Level 3: Struktur Atom (Lithium)
        # Edukasi: Pemain belajar bahwa atom Lithium memiliki 3 Proton dan 4 Neutron di intinya.
        return {
            "platforms": [
                pygame.Rect(0, 600, 2000, 100),
                pygame.Rect(2300, 500, 1500, 100), # Gap 300
                pygame.Rect(4100, 550, 1500, 100), # Gap 300
                pygame.Rect(5900, 450, 1500, 100), # Gap 300
                pygame.Rect(7700, 500, 2500, 100)  # Gap 300
            ],
            "obstacles": [
                {"type": "SUNGAI_BERACUN", "x": 1800, "y": 620, "width": 500, "height": 80},
                {"type": "KAYU", "x": 2800, "y": 450, "width": 50, "height": 50},
                {"type": "SUNGAI_BERACUN", "x": 3700, "y": 620, "width": 400, "height": 80},
                {"type": "KAYU", "x": 4800, "y": 500, "width": 50, "height": 50},
                {"type": "SUNGAI_BERACUN", "x": 5500, "y": 620, "width": 400, "height": 80},
                {"type": "KAYU", "x": 6800, "y": 400, "width": 50, "height": 50},
                {"type": "SUNGAI_BERACUN", "x": 7300, "y": 620, "width": 400, "height": 80}
            ],
            "items": [
                {"type": "Proton", "x": 800, "y": 550, "fact_text": "Proton adalah partikel bermuatan positif (+1) yang ada di inti atom!"},
                {"type": "Neutron", "x": 1300, "y": 550, "fact_text": "Neutron adalah partikel netral di inti atom yang menambah massa atom!"},
                {"type": "Proton", "x": 2600, "y": 400, "fact_text": "Jumlah Proton menentukan identitas unsur kimia!"},
                {"type": "Neutron", "x": 3200, "y": 400, "fact_text": "Isotop adalah atom dengan Proton sama tapi jumlah Neutron berbeda."},
                {"type": "Proton", "x": 4500, "y": 500, "fact_text": "Tiga proton artinya ini adalah unsur Lithium (Li)!"},
                {"type": "Neutron", "x": 5200, "y": 450, "fact_text": "Lithium-7 memiliki 3 Proton dan 4 Neutron."},
                {"type": "Neutron", "x": 6500, "y": 350, "fact_text": "Massa atom (A) = jumlah Proton (Z) + jumlah Neutron (N)."},
                {"type": "KUIS", "x": 8000, "y": 450,
                 "question": "Partikel subatomik apakah yang menentukan massa suatu atom?",
                 "options": ["A. Elektron", "B. Proton & Neutron", "C. Foton"],
                 "correct_idx": 1,
                 "explanation": "Sebagian besar massa atom terpusat di inti atom, yang terdiri dari Proton dan Neutron. Elektron massanya sangat kecil sehingga diabaikan."},
            ],
            "altar": {
                "x": 9000, "y": 450,
                "target_formula": {"Proton": 3, "Neutron": 4},
                "result_name": "Lithium",
                "result_fact": "Atom Lithium (Li) terbentuk dari 3 Proton dan 4 Neutron di intinya, menghasilkan nomor massa 7. Lithium adalah logam alkali yang sangat reaktif!"
            },
            "enemies": [
                {"x": 1200, "y": 550, "range": 200},
                {"x": 3500, "y": 500, "range": 150},
                {"x": 6500, "y": 450, "range": 300}
            ]
        }
    else:
        # Default or end of game
        return None

class LevelManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Background
        try:
            self.bg_image = pygame.image.load("assets/backroud.jfif").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))
        except Exception as e:
            self.bg_image = pygame.Surface((self.screen_width, self.screen_height))
            self.bg_image.fill((25, 25, 35))
            print(f"Warning: Could not load background image: {e}")
            
        self.bg_x1 = 0
        self.bg_x2 = self.screen_width
        self.bg_speed = 2
        
        # Level Data
        self.current_level = 1
        self.platforms = []
        self.obstacles = []
        self.enemy_group = pygame.sprite.Group()
        self.platform_speed = 3
        self.base_speed = 3 # Diperlambat dari 5 ke 3
        
    def load_level(self, level_number, item_manager):
        self.current_level = level_number
        data = get_level_data(level_number)
        
        if not data:
            print("Game Selesai atau Level tidak ditemukan!")
            return False
            
        self.platforms = data["platforms"]
        
        self.obstacles = []
        if "obstacles" in data:
            for obs_info in data["obstacles"]:
                self.obstacles.append(Obstacle(obs_info["x"], obs_info["y"], obs_info["width"], obs_info["height"], obs_info["type"]))
                
        item_manager.clear()
        
        from entities.items import Atom, BukuKuis
        for item_info in data["items"]:
            if item_info["type"] == "KUIS":
                quiz_item = BukuKuis(item_info["x"], item_info["y"])
                quiz_item.question = item_info.get("question", "Soal default?")
                quiz_item.options = item_info.get("options", ["A. 1", "B. 2", "C. 3"])
                quiz_item.correct_idx = item_info.get("correct_idx", 0)
                quiz_item.explanation = item_info.get("explanation", "Penjelasan default.")
                item_manager.add_item(quiz_item)
            else:
                fact_text = item_info.get("fact_text", "")
                item_manager.add_item(Atom(item_info["x"], item_info["y"], item_info["type"], fact_text))
            
        altar_info = data["altar"]
        altar = AltarReaksi(altar_info["x"], altar_info["y"], 
                            altar_info["target_formula"], altar_info["result_name"])
        # Simpan fakta senyawa ke dalam object altar secara dinamis
        altar.result_fact = altar_info.get("result_fact", "")
        item_manager.set_altar(altar)
        
        # Load Enemies
        self.enemy_group.empty()
        from entities.enemies import Enemy
        if "enemies" in data:
            for en_info in data["enemies"]:
                enemy = Enemy(en_info["x"], en_info["y"], en_info.get("range", 100))
                self.enemy_group.add(enemy)
                
        self.platform_speed = self.base_speed
        return True

    def update(self):
        # 1. Update Scroll Background
        # Only scroll if platform_speed > 0
        if self.platform_speed > 0:
            self.bg_x1 -= self.bg_speed
            self.bg_x2 -= self.bg_speed
            
            if self.bg_x1 <= -self.screen_width:
                self.bg_x1 = self.screen_width
            if self.bg_x2 <= -self.screen_width:
                self.bg_x2 = self.screen_width
                
        # 2. Update Platforms
        for plat in self.platforms:
            plat.x -= self.platform_speed
            
        # 3. Update Obstacles
        for obs in self.obstacles:
            obs.rect.x -= self.platform_speed
            
        # 4. Update Enemies
        self.enemy_group.update(self.platform_speed, self.platforms)
        
        # Hapus yang sudah lewat layar
        if self.platforms and self.platforms[0].right < 0:
            self.platforms.pop(0)
            
        self.obstacles = [obs for obs in self.obstacles if obs.rect.right > 0]

    def draw(self, surface):
        surface.blit(self.bg_image, (self.bg_x1, 0))
        surface.blit(self.bg_image, (self.bg_x2, 0))
        
        # Gambar platform sebagai blok
        for plat in self.platforms:
            pygame.draw.rect(surface, (139, 69, 19), plat) # Warna Coklat Tanah
            pygame.draw.rect(surface, (34, 139, 34), (plat.x, plat.y, plat.width, 20)) # Warna Hijau Rumput
            
        for obs in self.obstacles:
            obs.draw(surface)
            
        # 4. Draw Enemies
        self.enemy_group.draw(surface)
