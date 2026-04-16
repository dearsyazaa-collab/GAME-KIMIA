import pygame

class Enemy:
    def __init__(self, x, y, enemy_type="Monster Asam"):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.enemy_type = enemy_type
        self.hp = 30
        self.speed = 2
        self.direction = -1 # -1 kiri, 1 kanan

    def update(self):
        """Logika pergerakan musuh"""
        self.rect.x += self.speed * self.direction

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.die()

    def die(self):
        pass

    def draw(self, surface):
        color = (0, 255, 0) if self.enemy_type == "Monster Asam" else (0, 0, 255)
        pygame.draw.rect(surface, color, self.rect)
