import pygame

class QuizSystem:
    def __init__(self):
        self.is_active = False
        self.font = pygame.font.SysFont("Verdana", 24)
        self.font_q = pygame.font.SysFont("Verdana", 22, bold=True)
        self.font_instruksi = pygame.font.SysFont("Verdana", 20, bold=True)
        self.correct_idx = 1 # Indeks jawaban yang benar
        self.explanation = ""
        
    def show_quiz(self, question="Apa simbol kimia air?", options=["A. O2", "B. H2O", "C. CO2"], correct_idx=1, explanation="Air terbentuk dari 2 atom H dan 1 atom O."):
        self.is_active = True
        self.question = question
        self.options = options
        self.correct_idx = correct_idx
        self.explanation = explanation

    def hide_quiz(self):
        self.is_active = False

    def draw(self, surface):
        if not self.is_active:
            return
            
        screen_width, screen_height = surface.get_size()
        panel_rect = pygame.Rect(screen_width//2 - 350, screen_height//2 - 200, 700, 400)
        
        # Gambar Panel
        pygame.draw.rect(surface, (50, 50, 100), panel_rect, border_radius=15)
        pygame.draw.rect(surface, (255, 255, 255), panel_rect, width=4, border_radius=15)
        
        # Teks Pertanyaan (dengan word wrap sederhana)
        words = self.question.split()
        lines = []
        current_line = []
        current_length = 0
        for word in words:
            if current_length + len(word) > 55:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
            else:
                current_line.append(word)
                current_length += len(word) + 1
        if current_line:
            lines.append(" ".join(current_line))
            
        y_q = panel_rect.y + 20
        for line in lines:
            txt_q = self.font_q.render(line, True, (255, 255, 255))
            surface.blit(txt_q, (panel_rect.x + 20, y_q))
            y_q += 30
        
        # Menggambar opsi
        y_opt = y_q + 20
        for i, opt in enumerate(self.options):
            txt_opt = self.font.render(opt, True, (255, 255, 255))
            surface.blit(txt_opt, (panel_rect.x + 40, y_opt + (i * 45)))

        # Teks Instruksi
        instruksi = "Pose Jawab: Jempol(A), Peace(B), Tiga Jari(C)"
        txt_instruksi = self.font_instruksi.render(instruksi, True, (255, 255, 0))
        surface.blit(txt_instruksi, (panel_rect.x + 20, panel_rect.bottom - 40))
