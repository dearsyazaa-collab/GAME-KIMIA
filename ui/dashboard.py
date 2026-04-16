import pygame
import cv2

class Dashboard:
    def __init__(self):
        self.font_utama = pygame.font.SysFont("Verdana", 20, bold=True)
        self.font_skor = pygame.font.SysFont("Impact", 30)

    def draw(self, screen, player, camera_frame):
        # UI STATUS BAR
        ui_bg = pygame.Surface((350, 100))
        ui_bg.set_alpha(150)
        ui_bg.fill((0, 0, 0))
        screen.blit(ui_bg, (10, 10))
        
        txt_pose = self.font_utama.render(f"POSE: {player.pose}", True, (0, 255, 255))
        txt_skor = self.font_skor.render(f"SKOR: {player.score}", True, (255, 215, 0))
        txt_hp = self.font_utama.render(f"HP: {player.hp}", True, (255, 50, 50))
        
        screen.blit(txt_pose, (25, 20))
        screen.blit(txt_skor, (25, 60))
        screen.blit(txt_hp, (200, 60))

        # Kamera Kecil (Picture-in-Picture)
        if camera_frame is not None:
            lebar = screen.get_width()
            frame_small = cv2.resize(camera_frame, (200, 150))
            frame_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
            cam_surf = pygame.surfarray.make_surface(frame_small.swapaxes(0, 1))
            screen.blit(cam_surf, (lebar - 220, 20))
            pygame.draw.rect(screen, (255, 255, 255), (lebar - 220, 20, 200, 150), 3)
