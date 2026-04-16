import pygame
import cv2
import mediapipe as mp
import math

# --- 1. SETUP MEDIAPIPE ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# --- 2. SETUP PYGAME ---
pygame.init()
W, H = 1000, 700
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Eksperimen Pose Alkimia")

# INI BARIS YANG TADI KURANG:
clock = pygame.time.Clock() 

font_besar = pygame.font.SysFont("Arial", 40, bold=True)
font_kecil = pygame.font.SysFont("Arial", 20)

cap = cv2.VideoCapture(0)

def hitung_jarak(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

# Variabel status
pose_aktif = "TIDAK ADA"
warna_bg = (30, 30, 35)

running = True
while running:
    success, frame = cap.read()
    if not success: break
    
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    pose_aktif = "STANDBY"
    warna_elemen = (200, 200, 200)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark
            
            # Koordinat titik penting
            wrist = lm[0]
            thumb_tip, index_tip = lm[4], lm[8]
            middle_tip, ring_tip, pinky_tip = lm[12], lm[16], lm[20]
            index_pip = lm[6]

            # --- LOGIKA DETEKSI POSE ---
            
            # 1. LOMPAT (Telunjuk saja)
            if index_tip.y < index_pip.y and middle_tip.y > index_pip.y and pinky_tip.y > index_pip.y:
                pose_aktif = "LOMPAT (ANGIN)"
                warna_elemen = (100, 255, 100)

            # 2. SIHIR API (Cubit/OK)
            elif hitung_jarak(thumb_tip, index_tip) < 0.05:
                pose_aktif = "SIHIR API (EKSOTERM)"
                warna_elemen = (255, 50, 50)

            # 3. SIHIR ES (Mengepal)
            elif hitung_jarak(middle_tip, wrist) < 0.15:
                pose_aktif = "SIHIR ES (PRESIPITASI)"
                warna_elemen = (50, 150, 255)

            # 4. KUIS (Pose I Love You)
            elif index_tip.y < index_pip.y and pinky_tip.y < index_pip.y and middle_tip.y > index_pip.y:
                pose_aktif = "KUIS (I LOVE YOU)"
                warna_elemen = (255, 100, 200)

    # --- RENDER ---
    screen.fill(warna_bg)

    # Preview Kamera
    frame_small = cv2.resize(frame, (320, 240))
    frame_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
    cam_surf = pygame.surfarray.make_surface(frame_small.swapaxes(0, 1))
    screen.blit(cam_surf, (W//2 - 160, 50))
    pygame.draw.rect(screen, (255, 255, 255), (W//2 - 160, 50, 320, 240), 2)

    # Status Pose
    teks_pose = font_besar.render(pose_aktif, True, warna_elemen)
    rect_teks = teks_pose.get_rect(center=(W//2, H//2 + 100))
    screen.blit(teks_pose, rect_teks)

    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    
    # Memanggil clock agar loop berjalan stabil di 30 FPS
    clock.tick(30) 

cap.release()
pygame.quit()
# Tambahkan ini di dalam loop utama, di bawah deteksi pose
if pose_aktif == "SIHIR API (EKSOTERM)":
    # Gambar lingkaran merah di tangan karakter sebagai efek api
    pygame.draw.circle(screen, (255, 100, 0), (player_rect.centerx + 30, player_rect.centery), 20)
    # Tambahkan partikel kecil
    for i in range(5):
        pygame.draw.circle(screen, (255, 0, 0), (player_rect.centerx + 40, player_rect.centery - i*5), 5)

elif pose_aktif == "SIHIR ES (PRESIPITASI)":
    # Gambar kotak biru muda sebagai kristal es
    pygame.draw.rect(screen, (150, 200, 255), (player_rect.centerx + 20, player_rect.centery - 10, 30, 30))