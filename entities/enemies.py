import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_range=200):
        super().__init__()
        
        # Load Assets
        try:
            img_slime = pygame.image.load("assets/slime.png").convert_alpha()
            self.idle_image = pygame.transform.scale(img_slime, (80, 80))
            self.frozen_image = pygame.image.load("assets/enemy_frozen.png").convert_alpha()
            self.frozen_image = pygame.transform.scale(self.frozen_image, (80, 80))
        except:
            self.idle_image = pygame.Surface((80, 80))
            self.idle_image.fill((128, 0, 128))
            self.frozen_image = pygame.Surface((80, 80))
            self.frozen_image.fill((0, 191, 255))

        self.image = self.idle_image
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Attributes
        self.hp = 100
        self.speed = 2
        self.direction = 1 # 1: Kanan, -1: Kiri
        self.state = "ALIVE" # ALIVE, FROZEN, DEAD
        
        # Patrol Logic
        self.start_x = x
        self.patrol_range = patrol_range
        
        # Timer & Physics
        self.frozen_timer = 0
        self.death_scale = 1.0
        self.velocity_y = 0

    def update(self, scroll_speed, platforms):
        """
        scroll_speed: Kecepatan scroll layar
        platforms: List of pygame.Rect platform untuk deteksi tepi
        """
        # Selalu ikuti scroll kamera
        self.rect.x -= scroll_speed
        self.start_x -= scroll_speed
        
        if self.state == "ALIVE":
            self.image = self.idle_image
            
            # 1. Gerak Horizontal
            self.rect.x += self.speed * self.direction
            
            # 2. Deteksi Batas Patroli
            if abs(self.rect.x - self.start_x) >= self.patrol_range:
                self.direction *= -1
            
            # 3. Deteksi Tepi Platform (Edge Detection)
            # Kita cek 20 pixel di depan bawah kaki musuh
            check_x = self.rect.centerx + (self.direction * 30)
            check_y = self.rect.bottom + 5
            
            on_edge = True
            for plat in platforms:
                if plat.collidepoint(check_x, check_y):
                    on_edge = False
                    break
            
            if on_edge:
                self.direction *= -1 # Berbalik arah jika di ujung platform
                
        elif self.state == "FROZEN":
            self.image = self.frozen_image
            self.frozen_timer -= 1
            if self.frozen_timer <= 0:
                self.state = "ALIVE"
                
        elif self.state == "DEAD":
            # Animasi mengecil
            self.death_scale -= 0.05
            if self.death_scale <= 0.1:
                self.kill()
            else:
                new_size = (int(80 * self.death_scale), int(80 * self.death_scale))
                self.image = pygame.transform.scale(self.idle_image, new_size)
                center = self.rect.center
                self.rect = self.image.get_rect(center=center)

    def freeze(self, duration=300):
        self.state = "FROZEN"
        self.frozen_timer = duration

    def die(self):
        self.state = "DEAD"
