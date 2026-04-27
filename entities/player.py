import pygame

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 130, 160)
        self.hp = 100
        self.score = 0
        self.pose = "STANDBY"
        
        # --- Physics Baru (Optimasi Jurang) ---
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = False
        self.gravity = 0.8
        self.jump_speed = -18
        
        # 1. Coyote Time: Memberi toleransi lompat sesaat setelah jatuh dari tepi
        self.coyote_timer = 0
        self.coyote_max = 10 # 10 frame toleransi
        
        # 2. Horizontal Movement Physics
        self.acceleration = 0.8
        self.friction = 0.9
        self.max_speed_ground = 7
        self.max_speed_air = 9 # Speed boost di udara agar bisa melompati jurang lebar
        self.facing_right = True
        
        # --- Inventori & Magic ---
        self.inventory = {'H': 0, 'O': 0, 'H2O': 0}
        self.magic_cooldown = 0
        self.invulnerable_timer = 0

        # Load Sprites
        try:
            img_asli = pygame.image.load("assets/penyihir.png").convert_alpha()
            self.image_right = pygame.transform.scale(img_asli, (130, 160))
            self.image_left = pygame.transform.flip(self.image_right, True, False)
        except:
            self.image_right = pygame.Surface((130, 160))
            self.image_right.fill((0, 255, 0))
            self.image_left = pygame.transform.flip(self.image_right, True, False)

        self.current_image = self.image_right

    def update(self, pose, move_dir=0):
        self.pose = pose
        
        # 1. COYOTE TIME LOGIC
        if self.on_ground:
            self.coyote_timer = self.coyote_max
        else:
            self.coyote_timer -= 1

        # 2. HORIZONTAL MOVEMENT & AIR MOMENTUM
        # Tentukan batas kecepatan berdasarkan posisi (udara vs tanah)
        current_max_speed = self.max_speed_ground if self.on_ground else self.max_speed_air
        
        if move_dir > 0:
            self.velocity_x += self.acceleration
            self.facing_right = True
        elif move_dir < 0:
            self.velocity_x -= self.acceleration
            self.facing_right = False
        else:
            # Friksi lebih rendah di udara (momentum lebih terjaga)
            current_friction = self.friction if self.on_ground else 0.98
            self.velocity_x *= current_friction
            
        # Batasi kecepatan
        if abs(self.velocity_x) > current_max_speed:
            self.velocity_x = (current_max_speed if self.velocity_x > 0 else -current_max_speed)
            
        self.rect.x += int(self.velocity_x)
        self.current_image = self.image_right if self.facing_right else self.image_left

        # 3. OPTIMASI JUMP ARC (Lengkungan Lompat)
        # Deteksi awal lompatan menggunakan Coyote Time
        if self.pose == "LOMPAT" and self.coyote_timer > 0:
            self.velocity_y = self.jump_speed
            self.coyote_timer = 0 # Paksa timer habis agar tidak double jump
            self.on_ground = False
            
        # Variabel Gravity Dinamis: Agar PhysicsEngine mengambil nilai yang tepat
        # Default gravity
        self.gravity = 0.8
        
        # Hang Time: Terasa lebih ringan di puncak lompatan (abs(velocity_y) < 3)
        if not self.on_ground and abs(self.velocity_y) < 3:
            self.gravity = 0.4 # Gravitasi berkurang di puncak
            
        # Short Jump Logic: Jika pose lompat dilepas saat sedang naik, jatuh lebih cepat
        if self.pose != "LOMPAT" and self.velocity_y < 0:
            self.gravity = 2.0 # Jatuh lebih cepat jika tombol dilepas lebih awal

        # 4. Timer System
        if self.magic_cooldown > 0:
            self.magic_cooldown -= 1
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

    def draw(self, surface):
        if self.invulnerable_timer == 0 or (self.invulnerable_timer // 5) % 2 == 0:
            surface.blit(self.current_image, (self.rect.x, self.rect.y))
