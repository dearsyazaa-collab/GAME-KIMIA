import pygame

class Item:
    def __init__(self, x, y, item_type="Koin"):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.item_type = item_type
        self.active = True

    def draw(self, surface):
        if not self.active: return
        if self.item_type == "Koin":
            pygame.draw.circle(surface, (255, 215, 0), self.rect.center, 15)
        elif self.item_type == "QuestionBlock":
            pygame.draw.rect(surface, (139, 69, 19), self.rect)
            # Gambar tanda tanya
            font = pygame.font.SysFont("Arial", 20, bold=True)
            txt = font.render("?", True, (255, 255, 255))
            surface.blit(txt, (self.rect.x + 8, self.rect.y + 3))

class QuestionBlock(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "QuestionBlock")
        self.rect = pygame.Rect(x, y, 40, 40)
