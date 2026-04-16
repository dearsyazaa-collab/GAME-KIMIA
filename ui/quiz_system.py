import pygame

class QuizSystem:
    def __init__(self):
        self.is_active = False
        self.font = pygame.font.SysFont("Verdana", 24)
        
    def show_quiz(self, question="Apa simbol kimia air?", options=["A. O2", "B. H2O", "C. CO2"]):
        self.is_active = True
        self.question = question
        self.options = options

    def hide_quiz(self):
        self.is_active = False

    def check_answer(self, pose):
        """Logika untuk memeriksa pose tangan dengan jawaban"""
        if self.is_active and pose == "KUIS":
            # Nanti tambahkan logika validasi lebih detail
            self.hide_quiz()
            return True
        return False

    def draw(self, surface):
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
        
        # Teks Opsi
        for i, opt in enumerate(self.options):
            txt_opt = self.font.render(opt, True, (200, 200, 200))
            surface.blit(txt_opt, (panel_rect.x + 20, panel_rect.y + 80 + (i * 40)))
