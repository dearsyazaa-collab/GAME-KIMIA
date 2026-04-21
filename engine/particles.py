import pygame
import random

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def add_particles(self, x, y, color, count=10, speed=2, size_range=(2, 5), lifetime_range=(10, 30), style="explosion"):
        for _ in range(count):
            if style == "explosion":
                vx = random.uniform(-speed, speed)
                vy = random.uniform(-speed, speed)
            elif style == "fountain":
                vx = random.uniform(-speed/2, speed/2)
                vy = random.uniform(-speed, -1)
                
            p = {
                'x': x,
                'y': y,
                'vx': vx,
                'vy': vy,
                'color': color,
                'timer': random.randint(*lifetime_range),
                'size': random.randint(*size_range)
            }
            self.particles.append(p)
            
    def update(self, scroll_speed=0):
        for p in self.particles[:]:
            p['x'] += p['vx'] - scroll_speed
            p['y'] += p['vy']
            p['timer'] -= 1
            if p['timer'] <= 0:
                self.particles.remove(p)
                
    def draw(self, surface):
        for p in self.particles:
            pygame.draw.circle(surface, p['color'], (int(p['x']), int(p['y'])), p['size'])
