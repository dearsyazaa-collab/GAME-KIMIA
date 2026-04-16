import pygame

class PhysicsEngine:
    def __init__(self, gravity=0.8, terminal_velocity=15):
        self.gravity = gravity
        self.terminal_velocity = terminal_velocity

    def apply_gravity(self, entity):
        """Menambahkan efek gravitasi pada entitas"""
        if not entity.on_ground:
            entity.velocity_y += self.gravity
            if entity.velocity_y > self.terminal_velocity:
                entity.velocity_y = self.terminal_velocity
        entity.rect.y += entity.velocity_y

    def check_collision(self, entity, platforms):
        """Menangani tabrakan/collision dengan platform"""
        entity.on_ground = False
        for platform in platforms:
            if entity.rect.colliderect(platform.rect):
                if entity.velocity_y > 0 and entity.rect.bottom <= platform.rect.bottom:
                    entity.rect.bottom = platform.rect.top
                    entity.velocity_y = 0
                    entity.on_ground = True
