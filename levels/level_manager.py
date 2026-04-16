import pygame
import random

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
        
        # Platforms
        self.platforms = []
        self.platform_speed = 5
        self.spawn_x = 0
        self._generate_initial_platforms()
        
    def _generate_initial_platforms(self):
        # Base platform to start safely
        self.platforms.append(pygame.Rect(0, 600, 800, 100))
        self.spawn_x = 800
        self._spawn_platform()
        
    def _spawn_platform(self):
        gap = random.randint(100, 250)
        width = random.randint(300, 600)
        self.platforms.append(pygame.Rect(self.spawn_x + gap, 600, width, 100))
        self.spawn_x = self.spawn_x + gap + width

    def update(self):
        # 1. Update Scroll Background
        self.bg_x1 -= self.bg_speed
        self.bg_x2 -= self.bg_speed
        
        if self.bg_x1 <= -self.screen_width:
            self.bg_x1 = self.screen_width
        if self.bg_x2 <= -self.screen_width:
            self.bg_x2 = self.screen_width
            
        # 2. Update Platforms
        for plat in self.platforms:
            plat.x -= self.platform_speed
        self.spawn_x -= self.platform_speed
        
        # Hapus platform yang sudah lewat layar
        if self.platforms and self.platforms[0].right < 0:
            self.platforms.pop(0)
            
        # Terus buat platform baru jika mendekati layar
        if self.spawn_x < self.screen_width + 400:
            self._spawn_platform()

    def draw(self, surface):
        surface.blit(self.bg_image, (self.bg_x1, 0))
        surface.blit(self.bg_image, (self.bg_x2, 0))
        
        # Gambar platform sebagai blok
        for plat in self.platforms:
            pygame.draw.rect(surface, (139, 69, 19), plat) # Warna Coklat Tanah
            pygame.draw.rect(surface, (34, 139, 34), (plat.x, plat.y, plat.width, 20)) # Warna Hijau Rumput
