import pygame

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 130, 160)
        self.hp = 100
        self.score = 0
        self.pose = "STANDBY"
        
        # Physics
        self.velocity_y = 0
        self.on_ground = False
        
        # Chemistry Inventory
        self.inventory = {'H': 0, 'O': 0, 'H2O': 0}

        # Magic System
        self.magic_cooldown = 0
        
        # Damage / I-Frames
        self.invulnerable_timer = 0

        # Load Sprite
        try:
            img_asli = pygame.image.load("assets/penyihir.png").convert_alpha()
            self.image_right = pygame.transform.scale(img_asli, (130, 160))
        except Exception as e:
            self.image_right = pygame.Surface((130, 160))
            self.image_right.fill((0, 255, 0))
            print(f"Warning: Could not load player image: {e}")

        self.current_image = self.image_right

    def update(self, pose):
        self.pose = pose
        
        # Logika Gerakan
        if self.pose == "LOMPAT" and self.on_ground:
            self.velocity_y = -16
            self.on_ground = False
            
        # Cooldown timer
        if self.magic_cooldown > 0:
            self.magic_cooldown -= 1
            
        # Invulnerability timer
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

    def draw(self, surface):
        # Efek kedip (Blink) setiap 5 frame saat sedang kebal
        if self.invulnerable_timer == 0 or (self.invulnerable_timer // 5) % 2 == 0:
            surface.blit(self.current_image, (self.rect.x, self.rect.y))
