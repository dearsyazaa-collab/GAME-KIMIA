import pygame

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 130, 160)
        self.hp = 100
        self.score = 0
        self.pose = "STANDBY"
        self.facing_right = True
        
        # Physics
        self.velocity_y = 0
        self.on_ground = True
        self.y_awal = y

        # Load Sprite
        try:
            img_asli = pygame.image.load("assets/penyihir.png").convert_alpha()
            self.image_right = pygame.transform.scale(img_asli, (130, 160))
            self.image_left = pygame.transform.flip(self.image_right, True, False)
        except Exception as e:
            self.image_right = pygame.Surface((130, 160))
            self.image_right.fill((0, 255, 0))
            self.image_left = self.image_right
            print(f"Warning: Could not load player image: {e}")

        self.current_image = self.image_right

    def update(self, pose):
        self.pose = pose
        
        # Logika Gerakan Sementara
        if self.pose == "LOMPAT" and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False
            
        # Minimal Physics Simulation 
        if not self.on_ground:
            self.velocity_y += 0.8
            self.rect.y += self.velocity_y
            
        if self.rect.y >= self.y_awal:
            self.rect.y = self.y_awal
            self.on_ground = True
            self.velocity_y = 0

    def draw(self, surface):
        surface.blit(self.current_image, (self.rect.x, self.rect.y))
