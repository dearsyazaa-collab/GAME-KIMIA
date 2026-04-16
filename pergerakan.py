import cv2
import mediapipe as mp
import math

# 1. Inisialisasi MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

def hitung_jarak(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    status_aksi = "Menjelajah Dunia Archanum..."
    warna_teks = (255, 255, 255)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Ambil landmark penting
            pergelangan = hand_landmarks.landmark[0]
            jempol_tip = hand_landmarks.landmark[4]
            telunjuk_tip = hand_landmarks.landmark[8]
            tengah_tip = hand_landmarks.landmark[12]
            manis_tip = hand_landmarks.landmark[16]
            kelingking_tip = hand_landmarks.landmark[20]
            
            # Titik sendi untuk perbandingan (PIP)
            telunjuk_pip = hand_landmarks.landmark[6]

            # --- LOGIKA GESTUR ---

            # 1. LOMPAT (Menunjuk Jari Telunjuk ke Atas)
            # Logika: Hanya telunjuk yang lurus ke atas
            if telunjuk_tip.y < telunjuk_pip.y and tengah_tip.y > telunjuk_pip.y and kelingking_tip.y > telunjuk_pip.y:
                status_aksi = "LOMPAT!"
                warna_teks = (0, 255, 0) # Hijau

            # 2. INTERAKSI KUIS (Pose I Love You - Gambar yang kamu berikan)
            # Logika: Jempol, Telunjuk, dan Kelingking lurus, sedangkan Tengah dan Manis menekuk
            elif telunjuk_tip.y < telunjuk_pip.y and kelingking_tip.y < telunjuk_pip.y and tengah_tip.y > telunjuk_pip.y and manis_tip.y > telunjuk_pip.y:
                status_aksi = "KUIS: Memilih Jawaban!"
                warna_teks = (255, 105, 180) # Pink

            # 3. SIHIR API (Cubit / Pose OK)
            elif hitung_jarak(jempol_tip, telunjuk_tip) < 0.05:
                status_aksi = "SIHIR API: Eksoterm"
                warna_teks = (0, 0, 255) # Merah

            # 4. SIHIR ES (Mengepal)
            elif hitung_jarak(tengah_tip, pergelangan) < 0.15:
                status_aksi = "SIHIR ES: Presipitasi"
                warna_teks = (255, 255, 0) # Cyan

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # UI Overlay
    cv2.rectangle(frame, (0, 0), (w, 70), (0, 0, 0), -1)
    cv2.putText(frame, status_aksi, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, warna_teks, 2)
    
    cv2.imshow("Alchemist Controller - Kuis Pose Update", frame)

    if cv2.waitKey(1) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()