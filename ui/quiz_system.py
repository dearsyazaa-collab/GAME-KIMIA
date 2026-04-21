import pygame

class QuizSystem:
    def __init__(self):
        self.is_active = False
        self.font = pygame.font.SysFont("Verdana", 24)
        self.hovered_option_idx = -1
        self.option_rects = []
        self.correct_idx = 1 # Indeks jawaban yang benar
        
    def show_quiz(self, question="Apa simbol kimia air?", options=["A. O2", "B. H2O", "C. CO2"], correct_idx=1):
        self.is_active = True
        self.question = question
        self.options = options
        self.correct_idx = correct_idx
        self.hovered_option_idx = -1
        
        # Inisialisasi area persegi (Rect) untuk deteksi hover kursor
        screen_width, screen_height = 1000, 700
        panel_x = screen_width//2 - 200
        panel_y = screen_height//2 - 150
        
        self.option_rects = []
        for i in range(len(options)):
            # Area yang bisa di-klik untuk masing-masing opsi
            rect = pygame.Rect(panel_x + 20, panel_y + 80 + (i * 45), 360, 40)
            self.option_rects.append(rect)

    def hide_quiz(self):
        self.is_active = False

    def check_answer(self, finger_pos, pose):
        """Logika untuk memeriksa pose tangan dan kursor jari dengan jawaban"""
        if not self.is_active:
            return None
            
        self.hovered_option_idx = -1
        
        # Logika Hover & Select
        if finger_pos:
            finger_x, finger_y = finger_pos
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(finger_x, finger_y):
                    self.hovered_option_idx = i # Highlight opsi ini
                    
                    # Jika gestur KUIS dilakukan saat meng-hover opsi ini, proses jawabannya
                    if pose == "KUIS":
                        is_correct = (i == self.correct_idx)
                        self.hide_quiz()
                        return is_correct
                        
        return None

    def draw(self, surface, finger_pos=None):
        if not self.is_active:
            return
            
        screen_width, screen_height = surface.get_size()
        panel_rect = pygame.Rect(screen_width//2 - 200, screen_height//2 - 150, 400, 300)
        
        # Gambar Panel
        pygame.draw.rect(surface, (50, 50, 100), panel_rect, border_radius=15)
        pygame.draw.rect(surface, (255, 255, 255), panel_rect, width=4, border_radius=15)
        
        # Teks Pertanyaan
        txt_q = self.font.render(self.question, True, (255, 255, 255))
        surface.blit(txt_q, (panel_rect.x + 20, panel_rect.y + 20))
        
        # Menggambar opsi dan highlight
        for i, opt in enumerate(self.options):
            rect = self.option_rects[i]
            
            # Jika di-hover, beri warna highlight
            if i == self.hovered_option_idx:
                pygame.draw.rect(surface, (100, 200, 100), rect, border_radius=5) # Hijau
                pygame.draw.rect(surface, (255, 255, 255), rect, width=2, border_radius=5)
            else:
                pygame.draw.rect(surface, (70, 70, 120), rect, border_radius=5)
                
            txt_opt = self.font.render(opt, True, (255, 255, 255))
            # Menempatkan teks di tengah secara vertikal pada rect
            txt_rect = txt_opt.get_rect(midleft=(rect.x + 10, rect.centery))
            surface.blit(txt_opt, txt_rect)

        # Draw kursor jari
        if finger_pos:
            pygame.draw.circle(surface, (255, 50, 50), finger_pos, 10)
            pygame.draw.circle(surface, (255, 255, 255), finger_pos, 10, width=2)
