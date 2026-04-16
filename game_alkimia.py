import pygame
import cv2
import mediapipe as mp
import math
import random
from entities.musuh import Musuh

# --- 1. SETUP & KONFIGURASI ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

pygame.init()
lebar, tinggi = 1000, 700
screen = pygame.display.set_mode((lebar, tinggi))
pygame.display.set_caption("Alchemist Adventure - KTI Final Look")
clock = pygame.time.Clock()
# Font yang lebih estetik
font_utama = pygame.font.SysFont("Verdana", 20, bold=True)
font_skor = pygame.font.SysFont("Impact", 30)

# --- 2. LOAD ASSETS ---
# Load Karakter
try:
    img_asli = pygame.image.load("penyihir.png").convert_alpha()
    img_karakter_kanan = pygame.transform.scale(img_asli, (130, 160))
    img_karakter_kiri = pygame.transform.flip(img_karakter_kanan, True, False)
    img_karakter_current = img_karakter_kanan
except:
    img_karakter_current = pygame.Surface((130, 160))
    img_karakter_current.fill((0, 255, 0))

# Load Background (FITUR BARU)
try:
    img_bg = pygame.image.load("background.png").convert()
    img_bg = pygame.transform.scale(img_bg, (lebar, tinggi))
    pakai_bg = True
except:
    pakai_bg = False # Jika tidak ada gambar, pakai warna polos

# Variabel Game
player_rect = pygame.Rect(400, 500, 130, 160)
objek_kuis = pygame.Rect(800, 480, 70, 80) # Disesuaikan ukuran buku
y_awal = 500
gerak_animasi = 0
pose_aktif = "STANDBY"
skor = 0
sedang_di_tanah = True
pos_x_sebelumnya = player_rect.x
menghadap_kanan = True
partikel_api = [] 

# --- SISTEM PIJAKAN & MUSUH ---
# Daftar pijakan (Lantai dasar + platform melayang)
daftar_pijakan = [
    pygame.Rect(0, 660, lebar, 40), # Tantai dasar
    pygame.Rect(200, 480, 250, 20), # Platform kiri
    pygame.Rect(600, 400, 200, 20)  # Platform kanan
]

# Daftar Musuh
daftar_musuh = [
    Musuh(700, 600), # Musuh di lantai
    Musuh(250, 420)  # Musuh di platform
]

player_velocity_y = 0

# --- FUNGSI BANTUAN ---
def tambah_partikel_api(x, y):
    partikel_api.append([x, y, random.randint(-2, 2), random.randint(-6, -3), random.randint(5, 10), 20])

def gambar_api(surface):
    for p in partikel_api[:]: 
        p[0] += p[2]; p[1] += p[3]; p[4] -= 0.2; p[5] -= 1    
        if p[5] > 10: color = (255, 230, 50) 
        else: color = (255, 80, 20) 
        if p[5] <= 0 or p[4] <= 0: partikel_api.remove(p) 
        else:
            s = pygame.Surface((int(p[4]*2), int(p[4]*2)), pygame.SRCALPHA)
            pygame.draw.circle(s, (*color, 150), (int(p[4]), int(p[4])), int(p[4]))
            surface.blit(s, (p[0] - p[4], p[1] - p[4]))

def gambar_kristal_es(surface, x, y):
    points = [(x, y - 40), (x + 25, y), (x, y + 50), (x - 25, y)]
    pygame.draw.polygon(surface, (200, 240, 255), points)
    pygame.draw.polygon(surface, (0, 200, 255), points, 4)
    pygame.draw.line(surface, (255, 255, 255), (x, y-30), (x, y+40), 2)

# Gambar Buku Kuis (Pengganti Kotak Kuning)
def gambar_buku_kuis(surface, rect):
    # Cover Buku
    pygame.draw.rect(surface, (139, 69, 19), rect, border_radius=5)
    # Halaman Putih (Sisi)
    pygame.draw.rect(surface, (240, 230, 200), (rect.x + 60, rect.y + 5, 10, 70))
    # Judul/Simbol di Buku
    pygame.draw.circle(surface, (255, 215, 0), (rect.centerx - 5, rect.centery), 15, 3)
    # Efek Melayang
    rect.y += math.sin(pygame.time.get_ticks() * 0.005) * 0.5 

def hitung_jarak(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

# --- LOOP UTAMA ---
running = True
while running:
    # 1. RENDER BACKGROUND
    if pakai_bg:
        screen.blit(img_bg, (0, 0))
    else:
        screen.fill((25, 25, 35)) # Warna cadangan jika gambar error
    
    # 2. LOGIKA SENSOR (Sama seperti sebelumnya)
    pos_x_sebelumnya = player_rect.x 
    success, frame = cap.read()
    if not success: break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    pose_aktif = "STANDBY"
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark
            
            # Definisi Jari
            wrist = lm[0]
            jempol_tip, telunjuk_tip = lm[4], lm[8]
            tengah_tip, manis_tip, kelingking_tip = lm[12], lm[16], lm[20]
            telunjuk_pip, tengah_pip = lm[6], lm[10]
            manis_pip, kelingking_pip = lm[14], lm[18]
            
            # Logika Boolean
            is_telunjuk_naik = telunjuk_tip.y < telunjuk_pip.y
            is_tengah_naik = tengah_tip.y < tengah_pip.y
            is_manis_naik = manis_tip.y < manis_pip.y
            is_kelingking_naik = kelingking_tip.y < kelingking_pip.y

            player_rect.x = int(wrist.x * lebar) - 65

            # -- DETEKSI GESTUR --
            if hitung_jarak(jempol_tip, telunjuk_tip) < 0.06:
                pose_aktif = "SIHIR API"
                offset = 50 if menghadap_kanan else -50
                tambah_partikel_api(player_rect.centerx + offset, player_rect.centery)
                tambah_partikel_api(player_rect.centerx + offset + random.randint(-10,10), player_rect.centery + 10)

            elif (is_telunjuk_naik and is_tengah_naik and not is_manis_naik and not is_kelingking_naik):
                pose_aktif = "SIHIR ES"

            elif (not is_telunjuk_naik and not is_tengah_naik and not is_manis_naik and not is_kelingking_naik):
                if sedang_di_tanah:
                    player_velocity_y = -18 # Kecepatan melompat
                    pose_aktif = "LOMPAT"
                    sedang_di_tanah = False
                else: pose_aktif = "LOMPAT (UDARA)"
            else: pose_aktif = "JALAN"

            # Logika Kuis (Menabrak Buku)
            if player_rect.colliderect(objek_kuis) and ("SIHIR" in pose_aktif):
                objek_kuis.x = -200
                skor += 10

    # 3. FISIKA & LOGIKA VISUAL
    # 3. FISIKA PEMAIN & MUSUH
    
    # -- Gravitasi Pemain --
    if not sedang_di_tanah:
        player_velocity_y += 0.8
        player_rect.y += player_velocity_y
    
    # Cek Pijakan Pemain
    sedang_di_tanah = False
    for pijakan in daftar_pijakan:
        if player_rect.colliderect(pijakan):
            if player_velocity_y > 0 and player_rect.bottom <= pijakan.bottom + 10:
                player_rect.bottom = pijakan.top
                player_velocity_y = 0
                sedang_di_tanah = True

    # -- Update Musuh --
    for musuh in daftar_musuh[:]:
        musuh.update(daftar_pijakan, lebar)
        
        # TABRAKAN: PLAYER vs MUSUH (AABB Logic)
        if player_rect.colliderect(musuh.rect):
            # 1. KONDISI MENANG (STOMP): Pemain jatuh dari atas
            if player_velocity_y > 0 and player_rect.bottom < musuh.rect.centery + 10:
                daftar_musuh.remove(musuh)
                player_velocity_y = -12 # Efek memantul
                skor += 20
                print("MUSUH DIKALAHKAN! +20")
            else:
                # 2. KONDISI KALAH (DAMAGE): Kena dari samping atau bawah
                skor -= 10
                # Efek Knockback
                if player_rect.centerx < musuh.rect.centerx: player_rect.x -= 50
                else: player_rect.x += 50
                print("TERKENA DAMAGE! -10")

    kecepatan_x = player_rect.x - pos_x_sebelumnya
    if kecepatan_x > 2: img_karakter_current = img_karakter_kanan; menghadap_kanan = True
    elif kecepatan_x < -2: img_karakter_current = img_karakter_kiri; menghadap_kanan = False
        
    gerak_animasi += 0.2
    movement_bob = math.sin(gerak_animasi * (2 if abs(kecepatan_x) > 2 else 1)) * 6
    
    # 4. DRAWING (GAMBAR ULANG)
    
    # Karakter
    screen.blit(img_karakter_current, (player_rect.x, player_rect.y + movement_bob))

    # Objek Buku Kuis
    if objek_kuis.x > 0:
        gambar_buku_kuis(screen, objek_kuis)

    # Objek Musuh
    for musuh in daftar_musuh:
        musuh.draw(screen)

    # Objek Pijakan (Daftar Pijakan)
    for pijakan in daftar_pijakan:
        pygame.draw.rect(screen, (50, 150, 50), pijakan)

    # Efek Sihir
    gambar_api(screen)
    if pose_aktif == "SIHIR ES":
        offset = 70 if menghadap_kanan else -70
        gambar_kristal_es(screen, player_rect.centerx + offset, player_rect.centery)

    # UI STATUS BAR (Panel Transparan di Kiri Atas)
    ui_bg = pygame.Surface((350, 100))
    ui_bg.set_alpha(150) # Transparan
    ui_bg.fill((0, 0, 0)) # Warna Hitam
    screen.blit(ui_bg, (10, 10))
    
    # Teks di dalam UI
    txt_pose = font_utama.render(f"POSE: {pose_aktif}", True, (0, 255, 255))
    txt_skor = font_skor.render(f"SKOR: {skor}", True, (255, 215, 0))
    screen.blit(txt_pose, (25, 20))
    screen.blit(txt_skor, (25, 60))

    # Kamera Kecil dengan Bingkai
    frame_small = cv2.resize(frame, (200, 150))
    frame_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
    cam_surf = pygame.surfarray.make_surface(frame_small.swapaxes(0, 1))
    screen.blit(cam_surf, (lebar - 220, 20))
    pygame.draw.rect(screen, (255, 255, 255), (lebar - 220, 20, 200, 150), 3) # Bingkai putih

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    clock.tick(60)

cap.release()
pygame.quit()