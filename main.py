import pygame
import sys
from engine.camera_tracker import CameraTracker
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
    player = Player(400, 500)
    dashboard = Dashboard()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 1. Input Processing (Camera pose)
        frame, pose = camera.update()
        
        # 2. Game Logic / Physics Update
        player.update(pose)
        
        # 3. Rendering
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
