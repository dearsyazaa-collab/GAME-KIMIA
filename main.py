import pygame
import sys
from engine.camera_tracker import CameraTracker
from engine.physics import PhysicsEngine
from levels.level_manager import LevelManager
from entities.player import Player
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
        level_manager.draw(screen)
        player.draw(screen)
        
        if frame is not None:
            dashboard.draw(screen, player, frame)

        pygame.display.flip()
        clock.tick(60)

    camera.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
