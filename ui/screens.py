import pygame
import cv2

class Screens:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        pygame.font.init()
        self.title_font = pygame.font.SysFont('Arial', 64, bold=True)
        self.subtitle_font = pygame.font.SysFont('Arial', 32)
        self.text_font = pygame.font.SysFont('Arial', 24)

    def draw_main_menu(self, screen, frame):
        screen.fill((30, 30, 40))  # Dark background
        
        # Title
        title_surf = self.title_font.render("Alchemist Adventure", True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(title_surf, title_rect)
        
        # Instruction
        inst_surf = self.subtitle_font.render("Tekan SPACE untuk Mulai", True, (255, 255, 255))
        inst_rect = inst_surf.get_rect(center=(self.width // 2, self.height // 2 + 50))
        screen.blit(inst_surf, inst_rect)
        
        # Camera Feed
        if frame is not None:
            # Resize frame for PIP (Picture-in-Picture)
            pip_width, pip_height = 160, 120
            resized_frame = cv2.resize(frame, (pip_width, pip_height))
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            # Rotate and flip to match Pygame surface (cv2 is (H,W,C), Pygame is (W,H))
            frame_surface = pygame.surfarray.make_surface(rgb_frame.swapaxes(0, 1))
            
            # Draw frame in bottom right corner
            pip_rect = pygame.Rect(self.width - pip_width - 20, self.height - pip_height - 20, pip_width, pip_height)
            pygame.draw.rect(screen, (255, 255, 255), pip_rect.inflate(4, 4)) # Border
            screen.blit(frame_surface, pip_rect)
            
            cam_text = self.text_font.render("Kamera Aktif", True, (200, 200, 200))
            screen.blit(cam_text, (self.width - pip_width - 20, self.height - pip_height - 50))

    def draw_game_over(self, screen, score):
        screen.fill((50, 10, 10))  # Dark red background
        
        # Game Over text
        title_surf = self.title_font.render("GAME OVER", True, (255, 50, 50))
        title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(title_surf, title_rect)
        
        # Score
        score_surf = self.subtitle_font.render(f"Skor Akhir: {score}", True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(self.width // 2, self.height // 2 + 20))
        screen.blit(score_surf, score_rect)
        
        # Instruction
        inst_surf = self.text_font.render("Tekan R untuk Ulangi", True, (200, 200, 200))
        inst_rect = inst_surf.get_rect(center=(self.width // 2, self.height // 2 + 80))
        screen.blit(inst_surf, inst_rect)

    def draw_level_complete(self, screen, score):
        screen.fill((10, 50, 10))  # Dark green background
        
        # Title
        title_surf = self.title_font.render("LEVEL SELESAI!", True, (50, 255, 50))
        title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(title_surf, title_rect)
        
        # Subtitle
        sub_surf = self.subtitle_font.render("Senyawa Terbentuk!", True, (255, 215, 0))
        sub_rect = sub_surf.get_rect(center=(self.width // 2, self.height // 2 + 10))
        screen.blit(sub_surf, sub_rect)
        
        # Score
        score_surf = self.text_font.render(f"Skor Saat Ini: {score}", True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(self.width // 2, self.height // 2 + 60))
        screen.blit(score_surf, score_rect)
        
        # Instruction
        inst_surf = self.text_font.render("Tekan SPACE untuk Lanjut", True, (200, 200, 200))
        inst_rect = inst_surf.get_rect(center=(self.width // 2, self.height // 2 + 110))
        screen.blit(inst_surf, inst_rect)

    def draw_level_summary(self, screen, compound_name, compound_fact, can_continue):
        screen.fill((20, 20, 40))  # Dark blue background
        
        # Title
        title_surf = self.title_font.render("REAKSI BERHASIL!", True, (50, 255, 50))
        title_rect = title_surf.get_rect(center=(self.width // 2, 100))
        screen.blit(title_surf, title_rect)
        
        # Senyawa Terbentuk
        sub_surf = self.subtitle_font.render(f"Senyawa Terbentuk: {compound_name}", True, (255, 215, 0))
        sub_rect = sub_surf.get_rect(center=(self.width // 2, 200))
        screen.blit(sub_surf, sub_rect)
        
        # Visual/Kotak Fakta
        fact_rect = pygame.Rect(self.width // 8, 280, self.width * 3 // 4, 250)
        pygame.draw.rect(screen, (50, 50, 70), fact_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), fact_rect, 2, border_radius=10)
        
        # Override compound_fact based on compound_name for casual language
        if compound_name == "NaCl":
            compound_fact = "Na itu murah hati, dia kasih 1 elektronnya ke Cl yang butuh. Hasilnya? Ikatan Ion yang kuat kayak cinta mereka!"
        elif compound_name == "H2O":
            compound_fact = "H dan O itu tim solid. Mereka patungan (sharing) elektron biar sama-sama stabil. Itulah Ikatan Kovalen!"
        elif compound_name == "Lithium":
            compound_fact = "Di pusat atom ada 'geng' Proton dan Neutron. Mereka yang nentuin massa atom. Makin banyak mereka, makin berat atomnya!"
            
        # Teks Edukasi (Fakta Senyawa) - Simple word wrap
        words = compound_fact.split(' ')
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if self.text_font.size(test_line)[0] > fact_rect.width - 40:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
            
        y_offset = 310
        for line in lines:
            line_surf = self.text_font.render(line, True, (255, 255, 255))
            line_rect = line_surf.get_rect(center=(self.width // 2, y_offset))
            screen.blit(line_surf, line_rect)
            y_offset += 35
            
        # Instruction
        if can_continue:
            # Berkedip
            if pygame.time.get_ticks() % 1000 < 500:
                inst_surf = self.subtitle_font.render("Tekan SPACE untuk Lanjut", True, (200, 255, 200))
                inst_rect = inst_surf.get_rect(center=(self.width // 2, self.height - 100))
                screen.blit(inst_surf, inst_rect)
        else:
            inst_surf = self.text_font.render("Membaca informasi...", True, (150, 150, 150))
            inst_rect = inst_surf.get_rect(center=(self.width // 2, self.height - 100))
            screen.blit(inst_surf, inst_rect)

