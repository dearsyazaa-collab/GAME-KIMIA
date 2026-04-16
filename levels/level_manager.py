import pygame

class LevelManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scroll_x = 0
        try:
            self.bg_image = pygame.image.load("assets/background.png").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))
        except Exception as e:
            self.bg_image = pygame.Surface((self.screen_width, self.screen_height))
            self.bg_image.fill((25, 25, 35))
            print(f"Warning: Could not load background image: {e}")

    def update_scroll(self, amount):
        self.scroll_x -= amount

    def draw(self, surface):
        surface.blit(self.bg_image, (0, 0))
        # Nanti ditambahkan logic untuk menggambar tilemap/platform
        pygame.draw.rect(surface, (50, 150, 50), (0, 660, self.screen_width, 40)) # Lantai dasar
