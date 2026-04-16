import pygame
import sys
from engine.camera_tracker import CameraTracker
from engine.physics import PhysicsEngine
from levels.level_manager import LevelManager
from entities.player import Player
from entities.items import ItemManager
from ui.dashboard import Dashboard

def main():
    pygame.init()
    screen_width, screen_height = 1000, 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Alchemist Adventure")
    clock = pygame.time.Clock()

    # Initialize modules
    camera = CameraTracker(device_index=0)
    level_manager = LevelManager(screen_width, screen_height)
    physics_engine = PhysicsEngine(gravity=0.8, terminal_velocity=18)
    item_manager = ItemManager()
    player = Player(200, 400) # Starting safe position
    dashboard = Dashboard()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 1. Input Processing
        frame, pose = camera.update()
        
        # 2. Game Logic / Level Update
        player.update(pose)
        level_manager.update()
        
        # Scroll item manager at the exact speed of ground
        item_manager.update(level_manager.platform_speed, screen_width)
        
        # Collectible Collision Logic
        for item in item_manager.items[:]:
            if player.rect.colliderect(item.rect):
                print(f"Got {item.atom_type}!")
                player.inventory[item.atom_type] += 1
                item_manager.items.remove(item)
                
        # Chemistry Reaction Logic (H2O)
        if player.inventory['H'] >= 2 and player.inventory['O'] >= 1:
            player.inventory['H'] -= 2
            player.inventory['O'] -= 1
            player.inventory['H2O'] += 1
            player.score += 100
            print("Reaction Success: H2O Formed!")
        
        # 3. Physics Updates
        physics_engine.apply_gravity(player)
        physics_engine.check_collision(player, level_manager.platforms)
        
        # 4. Game Over / Out of bounds logic
        if player.rect.top > screen_height:
            print("GAME OVER - Player fell out of bounds!")
            # Reset player
            player.rect.y = 100
            player.velocity_y = 0
            # Auto reposition safe
            if level_manager.platforms:
                player.rect.x = level_manager.platforms[0].x + 50
            player.hp -= 10
            
        # 5. Rendering
        # Draw background and ground
        level_manager.draw(screen)
        
        # Draw items
        item_manager.draw(screen)
        
        # Draw player
        player.draw(screen)
        
        # Draw UI
        if frame is not None:
            dashboard.draw(screen, player, frame)

        pygame.display.flip()
        clock.tick(60)

    camera.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
