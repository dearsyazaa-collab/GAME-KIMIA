import pygame
import random

class Atom:
    def __init__(self, x, y, atom_type):
        self.rect = pygame.Rect(x, y, 40, 40) # Treat as 40x40 area for collision
        self.atom_type = atom_type # 'H' or 'O'
        
        # Setup font for drawing
        self.font = pygame.font.SysFont("Verdana", 24, bold=True)
        
    def draw(self, surface):
        center = self.rect.center
        if self.atom_type == 'H':
            color = (50, 150, 255) # Blue
            text = 'H'
        else:
            color = (255, 50, 50) # Red
            text = 'O'
            
        pygame.draw.circle(surface, color, center, 20)
        pygame.draw.circle(surface, (255, 255, 255), center, 20, 2) # Border
        
        txt_surf = self.font.render(text, True, (255, 255, 255))
        txt_rect = txt_surf.get_rect(center=center)
        surface.blit(txt_surf, txt_rect)

class ItemManager:
    def __init__(self):
        self.items = []
        self.spawn_timer = 0
        
    def update(self, scroll_speed, screen_width):
        # Move items
        for item in self.items:
            item.rect.x -= scroll_speed
            
        # Remove off-screen items
        self.items = [item for item in self.items if item.rect.right > 0]
        
        # Spawn logic
        self.spawn_timer += 1
        if self.spawn_timer > 100: # Spawn every ~100 frames
            self.spawn_timer = 0
            # spawn on the right, random height above ground
            spawn_x = screen_width + 50
            spawn_y = random.randint(300, 500)
            atom_type = random.choice(['H', 'H', 'O']) # H is more common
            self.items.append(Atom(spawn_x, spawn_y, atom_type))

    def draw(self, surface):
        for item in self.items:
            item.draw(surface)
