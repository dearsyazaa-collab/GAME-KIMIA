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

    def draw(self, surface):
        surface.blit(self.current_image, (self.rect.x, self.rect.y))
