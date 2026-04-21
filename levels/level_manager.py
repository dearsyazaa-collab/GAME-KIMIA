import pygame
from entities.items import Atom, AltarReaksi, Obstacle

def get_level_data(level_number):
    if level_number == 1:
        # Transisi Level 1: Pengenalan Ikatan Ion
        # Edukasi: Pemain belajar bagaimana Na (Natrium) melepas elektron dan Cl (Klorin) menerimanya untuk membentuk ikatan ion pada garam dapur (NaCl).
        return {
            "platforms": [
                pygame.Rect(0, 600, 800, 100),    # Platform 1 - Start Area (Aman minimal 800px)
                pygame.Rect(900, 500, 300, 100),  # Platform 2 - Tengah
                pygame.Rect(1300, 550, 400, 100), # Platform 3 - End Area
            ],
            "obstacles": [
                {"type": "KAYU", "x": 900, "y": 450, "width": 50, "height": 50} # Menghalangi jalan ke platform berikutnya
            ],
            "items": [
                {"type": "Na", "x": 400, "y": 550},
                {"type": "Cl", "x": 1400, "y": 500},
            ],
            "altar": {
                "x": 1600, "y": 450,
                "target_formula": {"Na": 1, "Cl": 1},
                "result_name": "NaCl"
            }
        }
    elif level_number == 2:
        # Transisi Level 2: Pengenalan Ikatan Kovalen
        # Edukasi: Pemain belajar bagaimana dua atom H berbagi elektron dengan satu atom O untuk membentuk ikatan kovalen pada Air (H2O).
        return {
            "platforms": [
                pygame.Rect(0, 600, 800, 100),    # Area Aman awal
                pygame.Rect(1300, 500, 400, 100),
                pygame.Rect(1800, 550, 300, 100),
            ],
            "obstacles": [
                {"type": "SUNGAI_BERACUN", "x": 800, "y": 620, "width": 500, "height": 80} # Harus dibekukan
            ],
            "items": [
                {"type": "H", "x": 400, "y": 550},
                {"type": "O", "x": 1400, "y": 400}, # Butuh lompatan tinggi
                {"type": "H", "x": 1900, "y": 500},
            ],
            "altar": {
                "x": 2100, "y": 450,
                "target_formula": {"H": 2, "O": 1},
                "result_name": "H2O"
            }
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
            self.bg_image = pygame.image.load("assets/background.png").convert()
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
        self.platform_speed = 5
        self.base_speed = 5 # Store the base speed to restore it when unpaused
        
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
        
        from entities.items import Atom, QuestionBlock
        for item_info in data["items"]:
            if item_info["type"] == "KUIS":
                item_manager.add_item(QuestionBlock(item_info["x"], item_info["y"]))
            else:
                item_manager.add_item(Atom(item_info["x"], item_info["y"], item_info["type"]))
            
        altar_info = data["altar"]
        altar = AltarReaksi(altar_info["x"], altar_info["y"], 
                            altar_info["target_formula"], altar_info["result_name"])
        item_manager.set_altar(altar)
        
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
