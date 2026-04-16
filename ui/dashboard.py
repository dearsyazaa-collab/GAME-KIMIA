import pygame
import cv2

class Dashboard:
    def __init__(self):
        self.font_utama = pygame.font.SysFont("Verdana", 20, bold=True)
        self.font_inv = pygame.font.SysFont("Verdana", 18, bold=True)
        self.font_skor = pygame.font.SysFont("Impact", 30)

    def draw(self, screen, player, camera_frame):
        # UI Kiri Atas (Inventory, Score, HP, Pose)
        ui_bg = pygame.Surface((550, 120))
        ui_bg.set_alpha(150)
        ui_bg.fill((0, 0, 0))
        screen.blit(ui_bg, (10, 10))
        
        # Score & HP & Pose
        txt_skor = self.font_skor.render(f"SCORE: {player.score}", True, (255, 215, 0))
        txt_hp = self.font_utama.render(f"HP: {player.hp}", True, (255, 50, 50))
        txt_pose = self.font_utama.render(f"POSE: {player.pose}", True, (0, 255, 255))
        
        screen.blit(txt_skor, (25, 20))
        screen.blit(txt_hp, (200, 25))
        screen.blit(txt_pose, (320, 25))
        
        # Inventory Text: SCORE: [score] | H: [count] | O: [count] | H2O: [count]
        inv_text = f"INVENTORY | H: {player.inventory['H']} | O: {player.inventory['O']} | H2O: {player.inventory['H2O']}"
        txt_inv = self.font_inv.render(inv_text, True, (255, 255, 255))
        screen.blit(txt_inv, (25, 75))

        # Kamera Kecil (Picture-in-Picture) di Kanan Atas
        if camera_frame is not None:
            lebar = screen.get_width()
            frame_small = cv2.resize(camera_frame, (200, 150))
            frame_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
            cam_surf = pygame.surfarray.make_surface(frame_small.swapaxes(0, 1))
            screen.blit(cam_surf, (lebar - 220, 20))
            pygame.draw.rect(screen, (255, 255, 255), (lebar - 220, 20, 200, 150), 3)
