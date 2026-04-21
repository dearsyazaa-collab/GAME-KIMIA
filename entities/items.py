import pygame
import random

class Atom:
    def __init__(self, x, y, atom_type):
        self.rect = pygame.Rect(x, y, 40, 40) # Treat as 40x40 area for collision
        self.atom_type = atom_type 
        
        # Setup font for drawing
        self.font = pygame.font.SysFont("Verdana", 24, bold=True)
        
    def draw(self, surface):
        center = self.rect.center
        
        # Pewarnaan berdasar jenis atom
        if self.atom_type == 'H':
            color = (50, 150, 255) # Biru
        elif self.atom_type == 'O':
            color = (255, 50, 50) # Merah
        elif self.atom_type == 'Na':
            color = (255, 165, 0) # Orange
        elif self.atom_type == 'Cl':
            color = (0, 255, 0) # Hijau
        else:
            color = (150, 150, 150) # Abu-abu default
            
        pygame.draw.circle(surface, color, center, 20)
        pygame.draw.circle(surface, (255, 255, 255), center, 20, 2) # Border
        
        txt_surf = self.font.render(self.atom_type, True, (255, 255, 255))
        txt_rect = txt_surf.get_rect(center=center)
        surface.blit(txt_surf, txt_rect)

class AltarReaksi:
    def __init__(self, x, y, target_formula, result_name):
        self.rect = pygame.Rect(x, y, 120, 150) # Dimensi altar
        self.target_formula = target_formula    # Contoh: {"Na": 1, "Cl": 1}
        self.result_name = result_name          # Contoh: "NaCl"
        self.font = pygame.font.SysFont("Verdana", 16, bold=True)

    def draw(self, surface):
        # Menggambar dasar altar
        pygame.draw.rect(surface, (100, 100, 100), self.rect)
        pygame.draw.rect(surface, (255, 215, 0), self.rect, 3) # Border emas
        
        # Teks target reaksi
        y_offset = self.rect.y + 10
        txt_title = self.font.render("Altar Reaksi", True, (255, 255, 255))
        surface.blit(txt_title, (self.rect.x + 10, y_offset))
        
        y_offset += 25
        for atom, count in self.target_formula.items():
            txt_req = self.font.render(f"{atom}: {count}", True, (200, 255, 200))
            surface.blit(txt_req, (self.rect.x + 10, y_offset))
            y_offset += 20
            
        txt_res = self.font.render(f"-> {self.result_name}", True, (255, 215, 0))
        surface.blit(txt_res, (self.rect.x + 10, y_offset + 10))


class ItemManager:
    def __init__(self):
        self.items = []
        self.altar = None
        
    def add_item(self, item):
        self.items.append(item)
        
    def set_altar(self, altar):
        self.altar = altar
        
    def clear(self):
        self.items.clear()
        self.altar = None

    def update(self, scroll_speed, screen_width):
        # Pindahkan item sesuai kecepatan platform
        for item in self.items:
            item.rect.x -= scroll_speed
            
        # Pindahkan altar jika ada
        if self.altar:
            self.altar.rect.x -= scroll_speed
            
        # Hapus item yang sudah keluar layar di sebelah kiri
        self.items = [item for item in self.items if item.rect.right > 0]

    def draw(self, surface):
        for item in self.items:
            item.draw(surface)
            
        if self.altar:
            self.altar.draw(surface)

class QuestionBlock:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.atom_type = "KUIS" # Menggunakan 'atom_type' agar bisa kompatibel dengan sistem collision saat ini
        self.font = pygame.font.SysFont("Verdana", 28, bold=True)
        
    def draw(self, surface):
        # Kotak berwarna ungu dengan tanda tanya
        pygame.draw.rect(surface, (150, 50, 200), self.rect, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=8)
        
        txt_surf = self.font.render("?", True, (255, 255, 255))
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

class Obstacle:
    def __init__(self, x, y, width, height, obs_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.obs_type = obs_type
        self.is_destroying = False
        self.destroy_timer = 0
        
    def draw(self, surface):
        if self.obs_type == "KAYU":
            if self.is_destroying:
                # Berkedip merah/oranye saat hancur
                if self.destroy_timer % 4 < 2:
                    color = (255, 69, 0) # Merah/Oranye
                    border = (255, 0, 0)
                else:
                    color = (139, 69, 19) # Coklat
                    border = (101, 67, 33)
            else:
                color = (139, 69, 19)
                border = (101, 67, 33)
                
            pygame.draw.rect(surface, color, self.rect)
            pygame.draw.rect(surface, border, self.rect, 3)
            # Tekstur simpel
            pygame.draw.line(surface, border, (self.rect.x + 10, self.rect.y), (self.rect.x + 10, self.rect.bottom), 2)
            pygame.draw.line(surface, border, (self.rect.x + 30, self.rect.y), (self.rect.x + 30, self.rect.bottom), 2)
            
        elif self.obs_type == "SUNGAI_BERACUN":
            # Hijau transparan untuk sungai beracun
            s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            s.fill((50, 205, 50, 150))
            surface.blit(s, (0, 0)) # S is drawn at rect coordinates in the blit
            # Gelombang kecil
            pygame.draw.arc(s, (34, 139, 34), (10, 10, 40, 20), 0, 3.14, 2)
            if self.rect.width > 50:
                pygame.draw.arc(s, (34, 139, 34), (60, 20, 40, 20), 0, 3.14, 2)
            surface.blit(s, (self.rect.x, self.rect.y))
            
        elif self.obs_type == "PIJAKAN_ES":
            # Biru es
            pygame.draw.rect(surface, (173, 216, 230), self.rect)
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
            # Refleksi es
            pygame.draw.line(surface, (255, 255, 255), (self.rect.x + 10, self.rect.y + 10), (self.rect.x + 30, self.rect.y + 30), 2)

