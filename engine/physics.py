import pygame

class PhysicsEngine:
    def __init__(self, gravity=0.8, terminal_velocity=15):
        self.gravity = gravity
        self.terminal_velocity = terminal_velocity

    def apply_gravity(self, entity):
        """Menambahkan efek gravitasi pada entitas"""
        entity.velocity_y += self.gravity
        if entity.velocity_y > self.terminal_velocity:
            entity.velocity_y = self.terminal_velocity
        entity.rect.y += entity.velocity_y

    def check_collision(self, entity, platforms):
        """Menangani tabrakan/collision dengan list platform (pygame.Rect)"""
        entity.on_ground = False
        for plat in platforms:
            if entity.rect.colliderect(plat):
                # Hanya mendarat jika sedang jatuh ke bawah dan posisi kaki sekitar atap platform
                if entity.velocity_y > 0 and entity.rect.bottom <= plat.top + 30:
                    entity.rect.bottom = plat.top
                    entity.velocity_y = 0
                    entity.on_ground = True
