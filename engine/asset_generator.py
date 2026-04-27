import pygame
import os

def generate_enemy_sprites():
    # Inisialisasi Pygame khusus untuk pembuatan aset
    pygame.init()
    
    # Pastikan folder assets ada
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # Ukuran sprite diperbesar (80x80)
    size = (80, 80)
    
    # 1. GENERATE ENEMY IDLE (Slime Kimia Ungu Transparan Besar)
    surface_idle = pygame.Surface(size, pygame.SRCALPHA)
    
    # Body Slime
    pygame.draw.ellipse(surface_idle, (128, 0, 128, 180), (10, 15, 60, 55)) 
    pygame.draw.ellipse(surface_idle, (180, 50, 180, 200), (20, 25, 40, 35)) # Highlight
    
    # Eyes (Proporsional dengan ukuran 80)
    pygame.draw.circle(surface_idle, (255, 255, 255), (28, 40), 8) # White
    pygame.draw.circle(surface_idle, (255, 255, 255), (52, 40), 8) # White
    pygame.draw.circle(surface_idle, (0, 0, 0), (28, 40), 3) # Pupil
    pygame.draw.circle(surface_idle, (0, 0, 0), (52, 40), 3) # Pupil
    
    pygame.image.save(surface_idle, "assets/enemy.png")
    print("Aset assets/enemy.png (UKURAN BESAR) berhasil dibuat!")

    # 2. GENERATE ENEMY FROZEN (Biru Kristal Besar)
    surface_frozen = pygame.Surface(size, pygame.SRCALPHA)
    
    # Body
    pygame.draw.ellipse(surface_frozen, (0, 255, 255, 200), (10, 15, 60, 55)) 
    pygame.draw.ellipse(surface_frozen, (200, 255, 255, 220), (20, 25, 40, 35)) 
    
    # Kristal Detail (X X Eyes)
    white = (255, 255, 255)
    pygame.draw.line(surface_frozen, white, (25, 35), (35, 45), 3)
    pygame.draw.line(surface_frozen, white, (35, 35), (25, 45), 3)
    pygame.draw.line(surface_frozen, white, (45, 35), (55, 45), 3)
    pygame.draw.line(surface_frozen, white, (55, 35), (45, 45), 3)

    pygame.image.save(surface_frozen, "assets/enemy_frozen.png")
    print("Aset assets/enemy_frozen.png (UKURAN BESAR) berhasil dibuat!")
    
    pygame.quit()

if __name__ == "__main__":
    generate_enemy_sprites()
