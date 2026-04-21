import pygame
import cv2

class Dashboard:
    def __init__(self):
        self.font_utama = pygame.font.SysFont("Verdana", 20, bold=True)
        self.font_inv = pygame.font.SysFont("Verdana", 18, bold=True)
        self.font_skor = pygame.font.SysFont("Impact", 30)

    def draw_hud(self, screen, player, camera_frame=None, current_level=1):
        # UI Kiri Atas (Inventory, Score, HP, Pose, Magic, Mission)
        ui_bg = pygame.Surface((550, 175))
        ui_bg.set_alpha(150)
        ui_bg.fill((0, 0, 0))
        screen.blit(ui_bg, (10, 10))
        
        # Score & HP & Pose
        txt_skor = self.font_skor.render(f"SCORE: {player.score}", True, (255, 215, 0))
        txt_hp = self.font_utama.render(f"HP: {int(player.hp)}", True, (255, 50, 50))
        txt_pose = self.font_utama.render(f"POSE: {player.pose}", True, (0, 255, 255))
        
        screen.blit(txt_skor, (25, 20))
        screen.blit(txt_hp, (200, 25))
        screen.blit(txt_pose, (320, 25))
        
        # Magic Status Indicator
        if hasattr(player, 'magic_cooldown') and player.magic_cooldown > 0:
            magic_text = f"Sihir: Cooldown... ({player.magic_cooldown // 60}s)"
            color_magic = (255, 100, 100)
        else:
            magic_text = "Sihir Siap!"
            color_magic = (100, 255, 100)
            
        txt_magic = self.font_utama.render(magic_text, True, color_magic)
        screen.blit(txt_magic, (25, 65))
        
        # Inventory Text (Dynamic)
        inv_items = [f"{k}: {v}" for k, v in player.inventory.items() if v > 0]
        if not inv_items:
            inv_text = "Tas: Kosong"
        else:
            inv_text = "Tas: " + " | ".join(inv_items)
            
        txt_inv = self.font_inv.render(inv_text, True, (255, 255, 255))
        screen.blit(txt_inv, (25, 105))
        
        # Misi / Objective (Dynamic based on Level)
        if current_level == 1:
            misi_text = "Misi: Membuat Garam Dapur (NaCl) - Ikatan Ion"
        elif current_level == 2:
            misi_text = "Misi: Membuat Air (H2O) - Ikatan Kovalen"
        else:
            misi_text = "Misi: Eksplorasi Dunia Kimia"
            
        txt_misi = self.font_inv.render(misi_text, True, (255, 255, 0))
        screen.blit(txt_misi, (25, 145))

        # Kamera Kecil (Picture-in-Picture) di Kanan Atas
        if camera_frame is not None:
            lebar = screen.get_width()
            frame_small = cv2.resize(camera_frame, (200, 150))
            frame_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
            cam_surf = pygame.surfarray.make_surface(frame_small.swapaxes(0, 1))
            screen.blit(cam_surf, (lebar - 220, 20))
            pygame.draw.rect(screen, (255, 255, 255), (lebar - 220, 20, 200, 150), 3)
