import pygame
import sys
import random
import json
import os

# === MANAJEMEN AKUN PENGGUNA (DINAMIS - DISIMPAN KE FILE) ===
# Path file JSON tempat semua akun pengguna disimpan secara permanen
FILE_AKUN = "data_akun.json"

# === SISTEM PELACAKAN SKOR PER PEMAIN ===
# Path file JSON khusus untuk menyimpan riwayat skor setiap pemain
FILE_SKOR = "data_skor.json"

# Dictionary sementara untuk menyimpan data pemain dalam satu sesi bermain
# Format: { 'nama_pemain': { 'skor_kuis': 0, 'soal_benar': 0, 'total_soal': 0 } }
data_pemain = {}

def muat_data_akun():
    """Membaca semua data akun dari file JSON. Mengembalikan dict kosong jika file belum ada."""
    # Periksa apakah file akun sudah ada di sistem
    if os.path.exists(FILE_AKUN):
        # Buka dan baca isi file JSON, kembalikan sebagai dictionary Python
        with open(FILE_AKUN, "r") as f:
            return json.load(f)
    # Jika file belum ada, kembalikan dictionary kosong (belum ada akun)
    return {}

def simpan_data_akun(data_akun):
    """Menyimpan semua data akun ke file JSON agar tidak hilang saat game ditutup."""
    # Tulis dictionary ke file JSON dengan format yang rapi (indent=4)
    with open(FILE_AKUN, "w") as f:
        json.dump(data_akun, f, indent=4)

def muat_data_skor():
    """Membaca riwayat skor semua pemain dari file JSON."""
    # Cek apakah file skor sudah ada
    if os.path.exists(FILE_SKOR):
        with open(FILE_SKOR, "r") as f:
            return json.load(f)
    # Jika belum ada, kembalikan dictionary kosong
    return {}

def simpan_skor_pemain(nama_pemain, skor_kuis, soal_benar, total_soal):
    """
    Menyimpan hasil skor kuis pemain ke file JSON secara permanen.
    Jika pemain sudah punya riwayat, skor terbaik (high score) akan diperbarui.
    """
    # Muat semua data skor yang sudah ada dari file
    semua_skor = muat_data_skor()

    # Cek apakah pemain ini sudah pernah menyimpan skor sebelumnya
    if nama_pemain in semua_skor:
        # Jika skor baru lebih tinggi, timpa dengan skor terbaru (high score)
        if skor_kuis > semua_skor[nama_pemain].get("skor_terbaik", 0):
            semua_skor[nama_pemain]["skor_terbaik"] = skor_kuis
        # Selalu simpan data sesi terbaru
        semua_skor[nama_pemain]["skor_terakhir"] = skor_kuis
        semua_skor[nama_pemain]["soal_benar_terakhir"] = soal_benar
        semua_skor[nama_pemain]["total_soal_terakhir"] = total_soal
    else:
        # Pemain baru, buat entri pertama untuk pemain ini di dictionary
        semua_skor[nama_pemain] = {
            "skor_terbaik": skor_kuis,
            "skor_terakhir": skor_kuis,
            "soal_benar_terakhir": soal_benar,
            "total_soal_terakhir": total_soal
        }

    # Tulis kembali seluruh data skor ke file JSON agar tersimpan permanen
    with open(FILE_SKOR, "w") as f:
        json.dump(semua_skor, f, indent=4)

    # Cetak hasil pencapaian ke konsol sebagai log (berguna untuk debugging KTI)
    print(f"\n{'='*50}")
    print(f"HASIL AKHIR PEMAIN: {nama_pemain}")
    print(f"Skor Kuis   : {skor_kuis} poin")
    print(f"Soal Benar  : {soal_benar}/{total_soal}")
    print(f"{'='*50}\n")

def proses_login_atau_daftar(username, password):
    """
    Fungsi utama otentikasi. Menjalankan dua logika sekaligus:
    1. Jika username BARU -> daftar otomatis dan izinkan masuk
    2. Jika username LAMA -> validasi password sebelum mengizinkan masuk
    Mengembalikan tuple (berhasil: bool, pesan: str)
    """
    # Validasi: username dan password tidak boleh kosong
    if not username or not password:
        return False, "Username dan Password tidak boleh kosong!"

    # Muat data akun yang sudah ada dari file JSON
    data_akun = muat_data_akun()

    # Cek apakah username ini sudah pernah terdaftar sebelumnya
    if username in data_akun:
        # Username SUDAH ADA -> cek apakah passwordnya cocok
        if data_akun[username] == password:
            # Password cocok, izinkan login
            return True, f"Login berhasil! Selamat datang, {username}!"
        else:
            # Password salah, tolak login
            return False, "Password salah! Silakan coba lagi."
    else:
        # Username BELUM ADA -> daftarkan sebagai akun baru
        data_akun[username] = password
        # Simpan akun baru ke file JSON agar tersimpan permanen
        simpan_data_akun(data_akun)
        return True, f"Akun baru '{username}' berhasil dibuat! Selamat bermain!"
# ================================================================

from engine.camera_tracker import CameraTracker
from engine.physics import PhysicsEngine
from levels.level_manager import LevelManager
from entities.player import Player
from entities.items import ItemManager
from ui.dashboard import Dashboard
from ui.quiz_system import QuizSystem
from ui.screens import Screens
from engine.particles import ParticleSystem

def main():
    pygame.init()
    screen_width, screen_height = 1000, 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Alchemist Adventure")
    clock = pygame.time.Clock()

    # Initialize Mixer & Music
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("assets/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Warning: Gagal memutar musik: {e}")

    # Initialize modules
    camera = CameraTracker(device_index=0)
    camera.start()
    level_manager = LevelManager(screen_width, screen_height)
    physics_engine = PhysicsEngine(gravity=0.8, terminal_velocity=15)
    item_manager = ItemManager()
    player = Player(200, 400) # Starting safe position
    dashboard = Dashboard()
    quiz_system = QuizSystem()
    screens = Screens(screen_width, screen_height)
    particle_system = ParticleSystem()
    
    game_state = "LOGIN"
    login_username = ""
    login_password = ""
    login_success_msg = ""  # Pesan sukses setelah login/daftar berhasil
    active_field = "username"
    login_error = ""
    logged_in_user = ""    # Menyimpan nama pengguna yang sedang aktif bermain

    # === VARIABEL SESI PELACAK SKOR KUIS ===
    # pemain_aktif: Nama pemain yang sedang bermain saat ini (diisi setelah login berhasil)
    pemain_aktif = ""
    # skor_kuis_sesi: Akumulasi skor kuis dalam satu sesi bermain (direset setiap sesi baru)
    skor_kuis_sesi = 0
    # soal_benar_sesi: Penghitung jumlah soal yang dijawab benar dalam satu sesi
    soal_benar_sesi = 0
    # total_soal_sesi: Total soal kuis yang sudah muncul dalam satu sesi
    total_soal_sesi = 0
    # Skor maksimal yang mungkin dicapai (5 soal x 20 poin = 100 poin)
    SKOR_PER_SOAL = 20
    game_paused = False
    countdown_timer = 0
    checkpoint_timer = 0
    summary_timer = 0
    quiz_cooldown_timer = 0
    quiz_result_timer = 0
    quiz_was_correct = False
    current_info_text = "Selamat datang! Gunakan sihir untuk melewati rintangan."

    # Load level pertama
    level_manager.load_level(1, item_manager)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "LOGIN":
                    mouse_pos = event.pos
                    u_rect = pygame.Rect(screen_width // 2 - 20, screen_height // 2 - 65, 250, 40)
                    p_rect = pygame.Rect(screen_width // 2 - 20, screen_height // 2 - 5, 250, 40)
                    if u_rect.collidepoint(mouse_pos):
                        active_field = "username"
                    elif p_rect.collidepoint(mouse_pos):
                        active_field = "password"

            if event.type == pygame.KEYDOWN:
                if game_state == "LOGIN":
                    if event.key == pygame.K_TAB:
                        active_field = "password" if active_field == "username" else "username"
                    elif event.key == pygame.K_RETURN:
                        # Proses login atau pendaftaran akun baru secara dinamis
                        berhasil, pesan = proses_login_atau_daftar(login_username, login_password)
                        if berhasil:
                            # Simpan nama pengguna yang login untuk ditampilkan di game
                            logged_in_user = login_username
                            login_error = ""
                            login_success_msg = pesan

                            # === INISIALISASI SESI PEMAIN AKTIF ===
                            # Simpan nama pemain yang berhasil login ke variabel sesi pemain_aktif
                            pemain_aktif = login_username

                            # Inisialisasi entri pemain di dictionary data_pemain dengan skor awal 0
                            # Contoh: data_pemain['luckie'] = {'skor_kuis': 0, 'soal_benar': 0, 'total_soal': 0}
                            data_pemain[pemain_aktif] = {
                                "skor_kuis": 0,
                                "soal_benar": 0,
                                "total_soal": 0
                            }

                            # Reset semua counter skor untuk sesi baru
                            skor_kuis_sesi = 0
                            soal_benar_sesi = 0
                            total_soal_sesi = 0

                            game_state = "MENU"
                        else:
                            # Tampilkan pesan error jika gagal login
                            login_error = pesan
                    elif event.key == pygame.K_BACKSPACE:
                        if active_field == "username":
                            login_username = login_username[:-1]
                        else:
                            login_password = login_password[:-1]
                    else:
                        if event.unicode and event.key not in (pygame.K_TAB, pygame.K_RETURN, pygame.K_ESCAPE):
                            if active_field == "username":
                                login_username += event.unicode
                            else:
                                login_password += event.unicode
                elif game_state == "MENU":
                    if event.key == pygame.K_SPACE:
                        game_state = "GET_READY"
                        countdown_timer = 180
                elif game_state == "GAME_OVER":
                    if event.key == pygame.K_r:
                        # Reset game dan semua counter skor untuk sesi baru
                        player = Player(200, 400)
                        item_manager = ItemManager()
                        level_manager.current_level = 1
                        level_manager.load_level(1, item_manager)
                        game_state = "GET_READY"
                        countdown_timer = 180
                        game_paused = False

                        # === RESET SKOR SESI SAAT GAME DIULANG ===
                        # Saat pemain menekan R untuk ulangi, semua skor kuis direset ke 0
                        skor_kuis_sesi = 0
                        soal_benar_sesi = 0
                        total_soal_sesi = 0
                        # Reset entri data_pemain untuk sesi baru
                        if pemain_aktif:
                            data_pemain[pemain_aktif] = {"skor_kuis": 0, "soal_benar": 0, "total_soal": 0}
                        # Reset flag penyimpanan agar skor bisa disimpan lagi
                        screens._skor_sudah_disimpan = False
                elif game_state == "LEVEL_SUMMARY":
                    if event.key == pygame.K_SPACE and summary_timer <= 0:
                        level_manager.current_level += 1
                        if not level_manager.load_level(level_manager.current_level, item_manager):
                            print("Selamat! Kamu telah menyelesaikan semua level!")
                            running = False
                        else:
                            # Reset posisi player agar aman di awal level baru
                            player.rect.x = 200
                            player.rect.y = 400
                            player.velocity_y = 0
                            game_state = "GET_READY"
                            countdown_timer = 180
                            game_paused = False
                            checkpoint_timer = 0

        # 1. Input Processing (Camera is always running)
        with camera.lock:
            frame = camera.current_frame
            fingers = getattr(camera, 'fingers_up', 0)
            fire_pose = getattr(camera, 'is_fire_pose', False)
            pinch = getattr(camera, 'is_pinching', False)
            finger_pos = getattr(camera, 'current_index_finger_pos', None)
        
        # --- STATE MACHINE RENDERING & LOGIC ---
        if game_state == "LOGIN":
            # Render layar login dengan semua data state yang relevan
            screens.draw_login_screen(screen, login_username, login_password, active_field, login_error)
            
        elif game_state == "MENU":
            screens.draw_main_menu(screen, frame)
            
        elif game_state == "GET_READY":
            # Render statis (tidak ada update logika pergerakan)
            level_manager.draw(screen)
            item_manager.draw(screen)
            player.draw(screen)
            if frame is not None:
                dashboard.draw_hud(screen, player, frame, level_manager.current_level)
                
            countdown_timer -= 1
            font_besar = pygame.font.SysFont("Impact", 150)
            
            if countdown_timer > 120:
                teks = "3"
            elif countdown_timer > 60:
                teks = "2"
            elif countdown_timer > 0:
                teks = "1"
            else:
                teks = "MULAI!"
                if countdown_timer < -30:
                    game_state = "PLAYING"
                    
            t_surface = font_besar.render(teks, True, (255, 255, 0))
            out_surface = font_besar.render(teks, True, (0, 0, 0))
            rect_t = t_surface.get_rect(center=(screen_width//2, screen_height//2))
            screen.blit(out_surface, (rect_t.x + 4, rect_t.y + 4))
            screen.blit(t_surface, rect_t)
            
        elif game_state == "PLAYING":
            # State-Based Input Isolation untuk PLAYING
            pose = "STANDBY"
            if fire_pose:
                pose = "SIHIR API"
            elif pinch:
                pose = "SIHIR ES"
            elif fingers >= 4:
                pose = "LOMPAT"
                
            # Logika Gerakan Horizontal (Berdasarkan posisi jari)
            move_dir = 0
            # ISOLASI INPUT: Hanya gerak jika tidak sedang mengeluarkan sihir
            if pose not in ["SIHIR API", "SIHIR ES"] and finger_pos is not None:
                if finger_pos[0] < 350:      # Area Mundur/Kiri (0-350)
                    move_dir = -1
                elif finger_pos[0] > 650:    # Area Maju/Kanan (650-1000)
                    move_dir = 1
                else:
                    move_dir = 0             # Area Berhenti (350-650) - Diperlebar
            else:
                # Saat sihir aktif, biarkan karakter meluncur pelan (friksi)
                move_dir = 0
                    
            # 2. Game Logic / Level Update
            if not game_paused:
                player.update(pose, move_dir)
                level_manager.update()
                
                # Scroll item manager at the exact speed of ground
                item_manager.update(level_manager.platform_speed, screen_width)
                particle_system.update(level_manager.platform_speed)
                
                # Visual sihir secara permanen di tangan karakter
                if pose == "SIHIR API":
                    particle_system.add_particles(player.rect.centerx + 50, player.rect.centery, color=(255, 69, 0), count=2, speed=2)
                elif pose == "SIHIR ES":
                    particle_system.add_particles(player.rect.centerx + 50, player.rect.centery, color=(200, 255, 255), count=2, speed=2)
                
                # Update rintangan yang sedang hancur
                for obs in level_manager.obstacles[:]:
                    if getattr(obs, 'is_destroying', False):
                        obs.destroy_timer -= 1
                        # Spawn partikel api selama menghancurkan
                        if obs.destroy_timer % 3 == 0:
                            particle_system.add_particles(
                                obs.rect.centerx + random.randint(-obs.rect.width//2, obs.rect.width//2),
                                obs.rect.centery + random.randint(-obs.rect.height//2, obs.rect.height//2),
                                color=(255, 100, 0), count=2, speed=1, size_range=(2, 4), lifetime_range=(10, 20), style="explosion"
                            )
                        if obs.destroy_timer <= 0:
                            level_manager.obstacles.remove(obs)
                            
                # Collectible Collision Logic
                for item in item_manager.items[:]:
                    if player.rect.colliderect(item.rect):
                        if getattr(item, 'atom_type', '') == 'KUIS':
                            print("Mendapat BukuKuis! Kuis dimulai.")
                            game_state = "QUIZ_MODE"
                            quiz_cooldown_timer = 90
                            if hasattr(item, 'question'):
                                quiz_system.show_quiz(item.question, item.options, item.correct_idx, item.explanation)
                            else:
                                quiz_system.show_quiz()
                            item_manager.items.remove(item)
                        else:
                            print(f"Mendapat {item.atom_type}!")
                            player.inventory[item.atom_type] = player.inventory.get(item.atom_type, 0) + 1
                            if hasattr(item, 'fact_text') and item.fact_text:
                                current_info_text = item.fact_text
                            else:
                                current_info_text = f"Bagus! Kamu menemukan {item.atom_type}!"
                            item_manager.items.remove(item)
                            
                # Obstacle Collision & Magic Logic
                for obs in level_manager.obstacles[:]:
                    if getattr(obs, 'is_destroying', False):
                        continue # Lewati collision jika sedang hancur
                        
                    # Deteksi target sihir menggunakan koordinat tangan (finger_pos)
                    target_hit = False
                    if finger_pos is not None:
                        # finger_pos berupa (x, y) sesuai resolusi kamera/layar
                        if obs.rect.collidepoint(finger_pos[0], finger_pos[1]):
                            target_hit = True

                    if obs.obs_type == "KAYU":
                        if pose == "SIHIR API":
                            if player.magic_cooldown == 0 and (target_hit or player.rect.colliderect(obs.rect)):
                                obs.is_destroying = True
                                obs.destroy_timer = 30
                                print("KAYU mulai dihancurkan dengan SIHIR API!")
                                current_info_text = "Luar Biasa! Reaksi Eksoterm menghasilkan panas yang membakar kayu!"
                                player.score += 50
                                player.magic_cooldown = 180
                                particle_system.add_particles(obs.rect.centerx, obs.rect.centery, color=(255, 69, 0), count=40, speed=4)
                        elif player.rect.colliderect(obs.rect):
                            # Dorong pemain agar tidak bisa lewat (berlaku seperti dinding)
                            player.rect.right = obs.rect.left
                                
                    elif obs.obs_type == "SUNGAI_BERACUN":
                        if pose == "SIHIR ES":
                            if player.magic_cooldown == 0 and (target_hit or player.rect.colliderect(obs.rect)):
                                obs.obs_type = "PIJAKAN_ES"
                                print("SUNGAI BERACUN dibekukan menjadi PIJAKAN ES!")
                                current_info_text = "Tepat Sekali! Reaksi Endoterm menyerap panas di sekitar sungai!"
                                player.score += 50
                                player.magic_cooldown = 180
                                particle_system.add_particles(obs.rect.centerx, obs.rect.y, color=(200, 255, 255), count=30, speed=2, style="fountain")
                        elif player.rect.colliderect(obs.rect):
                            # Efek pentalan saat jatuh ke sungai beracun
                            player.rect.bottom = obs.rect.top - 1
                            player.velocity_y = -12
                            # Kurangi HP jika menginjak racun dan sedang tidak kebal
                            if player.invulnerable_timer == 0:
                                player.hp -= 15
                                player.invulnerable_timer = 90 # 1.5 detik kebal
                                if player.hp <= 0:
                                    print("GAME OVER - Terkena Sungai Beracun")
                                    game_state = "GAME_OVER"

                # Enemy Collision & Magic Logic
                for enemy in level_manager.enemy_group:
                    if enemy.state == "DEAD":
                        continue
                        
                    # Deteksi target sihir (finger_pos)
                    target_hit = False
                    if finger_pos is not None:
                        if enemy.rect.collidepoint(finger_pos[0], finger_pos[1]):
                            target_hit = True

                    # 1. SIHIR API (Eksoterm)
                    if pose == "SIHIR API" and (target_hit or player.rect.colliderect(enemy.rect)):
                        if player.magic_cooldown == 0:
                            enemy.die()
                            current_info_text = "Reaksi Eksoterm: Energi panas menghancurkan molekul musuh!"
                            player.score += 75
                            player.magic_cooldown = 120
                            particle_system.add_particles(enemy.rect.centerx, enemy.rect.centery, color=(255, 69, 0), count=30, speed=5, style="explosion")
                    
                    # 2. SIHIR ES (Endoterm/Presipitasi)
                    elif pose == "SIHIR ES" and (target_hit or player.rect.colliderect(enemy.rect)):
                        if player.magic_cooldown == 0 and enemy.state != "FROZEN":
                            enemy.freeze(300) # 5 detik
                            current_info_text = "Reaksi Endoterm: Suhu turun, pergerakan musuh terhenti!"
                            player.score += 50
                            player.magic_cooldown = 120
                            particle_system.add_particles(enemy.rect.centerx, enemy.rect.y, color=(200, 255, 255), count=20, speed=3, style="fountain")

                    # 3. Collision Fisik (Stomp atau Damage)
                    elif player.rect.colliderect(enemy.rect):
                        # Stomp Mechanic: Pemain menginjak musuh dari atas
                        if player.velocity_y > 0 and player.rect.bottom < enemy.rect.centery + 10:
                            enemy.die()
                            player.velocity_y = -12 # Memantul
                            player.score += 100
                            current_info_text = "Serangan Presisi! Struktur musuh hancur!"
                            particle_system.add_particles(enemy.rect.centerx, enemy.rect.top, color=(128, 0, 128), count=15, speed=2)
                        
                        # Damage: Tabrakan samping/bawah
                        elif player.invulnerable_timer == 0 and enemy.state != "FROZEN":
                            player.hp -= 20
                            player.invulnerable_timer = 90
                            current_info_text = "Awas! Tabrakan dengan musuh mengurangi HP!"
                            
                            # Knockback Effect (Mario-style)
                            # Pantul ke belakang dan ke atas sedikit
                            player.velocity_y = -10
                            if player.facing_right:
                                player.velocity_x = -10
                            else:
                                player.velocity_x = 10
                                
                            if player.hp <= 0:
                                game_state = "GAME_OVER"

            # Altar Collision & Chemistry Reaction Logic
            if not game_paused and item_manager.altar and player.rect.colliderect(item_manager.altar.rect):
                level_manager.platform_speed = 0 # Berhenti saat di altar
                
                if pose == "SIHIR API":
                    target = item_manager.altar.target_formula
                    cocok = True
                    for atom, count in target.items():
                        if player.inventory.get(atom, 0) < count:
                            cocok = False
                            break
                    
                    if cocok:
                        # Kurangi bahan
                        for atom, count in target.items():
                            player.inventory[atom] -= count
                            
                        res_name = item_manager.altar.result_name
                        player.inventory[res_name] = player.inventory.get(res_name, 0) + 1
                        player.score += 100
                        print(f"Reaksi Berhasil! Membentuk {res_name}")
                        current_info_text = "REAKSI SEMPURNA! Ikatan Kimia Terbentuk!"
                        
                        # Lanjut level: Pindah ke state LEVEL_SUMMARY
                        game_state = "LEVEL_SUMMARY"
                        summary_timer = 180 # 3 detik pada 60 FPS
                        
                        # Trigger kembang api
                        for _ in range(10):
                            rx = random.randint(100, 900)
                            ry = random.randint(100, 400)
                            color = random.choice([(255,50,50), (50,255,50), (50,50,255), (255,215,0), (255,50,255), (50,255,255)])
                            particle_system.add_particles(rx, ry, color=color, count=50, speed=5, style="explosion", size_range=(3,6), lifetime_range=(30,60))
                    else:
                        print("Reaksi Gagal! Bahan tidak cukup atau salah.")
                        if player.invulnerable_timer == 0:
                            player.hp -= 10
                            player.invulnerable_timer = 90
                            if player.hp <= 0:
                                print("GAME OVER - HP Habis")
                                game_state = "GAME_OVER"
            else:
                level_manager.platform_speed = level_manager.base_speed
            
            # 3. Physics Updates
            if not game_paused:
                physics_engine.apply_gravity(player)
                
                # Gabungkan platform biasa dan rintangan yang sudah jadi PIJAKAN_ES untuk collision
                active_platforms = level_manager.platforms.copy()
                for obs in level_manager.obstacles:
                    if obs.obs_type == "PIJAKAN_ES":
                        active_platforms.append(obs.rect)
                        
                # Pemulihan posisi X (Auto-run ke kanan hingga batas aman jika tidak terhalang)
                if player.rect.x < 200:
                    player.rect.x += 2
                    
                physics_engine.check_collision(player, active_platforms)
                
                # Prevent player from going off screen to the left
                if player.rect.left < 0:
                    player.rect.left = 0
                    if player.invulnerable_timer == 0:
                        player.hp -= 10 # Reduce HP if being crushed against the left edge
                        player.invulnerable_timer = 90
                        if player.hp <= 0:
                            print("GAME OVER - Terjepit layar!")
                            game_state = "GAME_OVER"
            
            # 4. Game Over / Out of bounds logic
            if not game_paused and player.rect.top > screen_height:
                print("GAME OVER - Player fell out of bounds!")
                # Reset player posisi
                player.rect.y = 100
                player.velocity_y = 0
                # Auto reposition safe
                if level_manager.platforms:
                    player.rect.x = level_manager.platforms[0].x + 50
                player.hp -= 10
                if player.hp <= 0:
                    game_state = "GAME_OVER"
                
            # 5. Rendering State PLAYING
            level_manager.draw(screen)
            item_manager.draw(screen)
            player.draw(screen)
            particle_system.draw(screen)
            if frame is not None:
                dashboard.draw_hud(screen, player, frame, level_manager.current_level)
                
            # Render Subtitle Bar
            dashboard.draw_info_panel(screen, current_info_text)

            # Debug: Garis Bantu Area Kontrol (Opsional, bisa dihapus nanti)
            pygame.draw.line(screen, (255, 255, 255), (350, 0), (350, 700), 1)
            pygame.draw.line(screen, (255, 255, 255), (650, 0), (650, 700), 1)
            
        elif game_state == "QUIZ_MODE":
            # Render background dan game world (diam)
            level_manager.draw(screen)
            item_manager.draw(screen)
            player.draw(screen)
            particle_system.draw(screen)
            
            if frame is not None:
                dashboard.draw_hud(screen, player, frame, level_manager.current_level)
                
            # Tambahkan overlay hitam transparan untuk fokus
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
                
            # Tampilkan Kuis
            quiz_system.draw(screen)
            
            if quiz_cooldown_timer > 0:
                quiz_cooldown_timer -= 1
                font_besar = pygame.font.SysFont("Impact", 40)
                txt_cooldown = font_besar.render("Membaca Soal...", True, (255, 255, 0))
                rect_c = txt_cooldown.get_rect(center=(screen_width//2, screen_height - 50))
                screen.blit(txt_cooldown, rect_c)
            else:
                # Logika penerimaan jawaban
                jawaban_pemain = None
                if fingers == 1:
                    jawaban_pemain = 0
                elif fingers == 2:
                    jawaban_pemain = 1
                elif fingers == 3:
                    jawaban_pemain = 2
                    
                if jawaban_pemain is not None:
                    # Tambahkan penghitung total soal kuis yang sudah muncul
                    total_soal_sesi += 1

                    if jawaban_pemain == quiz_system.correct_idx:
                        print("Kuis: Jawaban Benar! (+100 Skor Game, +20 Skor Kuis)")
                        player.score += 100  # Skor gameplay tetap berjalan seperti biasa

                        # === TAMBAH SKOR KUIS JIKA JAWABAN BENAR ===
                        # Setiap jawaban benar memberikan SKOR_PER_SOAL poin (20 poin) ke skor kuis pemain
                        skor_kuis_sesi += SKOR_PER_SOAL
                        soal_benar_sesi += 1

                        # Sinkronisasi: perbarui nilai di dictionary data_pemain berdasarkan pemain_aktif
                        if pemain_aktif and pemain_aktif in data_pemain:
                            data_pemain[pemain_aktif]["skor_kuis"] = skor_kuis_sesi
                            data_pemain[pemain_aktif]["soal_benar"] = soal_benar_sesi
                            data_pemain[pemain_aktif]["total_soal"] = total_soal_sesi

                        quiz_was_correct = True
                        current_info_text = f"Jawaban Benar! +{SKOR_PER_SOAL} poin kuis! ({skor_kuis_sesi} total)"
                    else:
                        print("Kuis: Jawaban Salah! (-10 HP, +0 Skor Kuis)")
                        player.hp -= 10

                        # === JAWABAN SALAH: Skor kuis tidak bertambah (+=0) ===
                        # Hanya total soal yang diperbarui, skor_kuis tidak berubah
                        if pemain_aktif and pemain_aktif in data_pemain:
                            data_pemain[pemain_aktif]["total_soal"] = total_soal_sesi

                        quiz_was_correct = False
                        current_info_text = "Jawaban Salah! Skor kuis tidak bertambah."

                    game_state = "QUIZ_RESULT"
                    quiz_result_timer = 180

        elif game_state == "QUIZ_RESULT":
            # Render background dan game world (diam)
            level_manager.draw(screen)
            item_manager.draw(screen)
            player.draw(screen)
            particle_system.draw(screen)
            
            if frame is not None:
                dashboard.draw_hud(screen, player, frame, level_manager.current_level)
                
            # Overlay warna
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(200)
            if quiz_was_correct:
                overlay.fill((0, 150, 0)) # Hijau
            else:
                overlay.fill((150, 0, 0)) # Merah
            screen.blit(overlay, (0, 0))
            
            # Teks Hasil
            font_besar = pygame.font.SysFont("Impact", 60)
            if quiz_was_correct:
                txt_hasil = font_besar.render("TEPAT SEKALI! +100 Skor", True, (255, 255, 255))
            else:
                txt_hasil = font_besar.render("YAH, KURANG TEPAT! -10 HP", True, (255, 255, 255))
            rect_hasil = txt_hasil.get_rect(center=(screen_width//2, screen_height//2 - 50))
            screen.blit(txt_hasil, rect_hasil)
            
            # Teks Pembahasan
            font_pembahasan = pygame.font.SysFont("Verdana", 24)
            words = quiz_system.explanation.split()
            lines = []
            current_line = []
            current_length = 0
            for word in words:
                if current_length + len(word) > 50:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                    current_length = len(word)
                else:
                    current_line.append(word)
                    current_length += len(word) + 1
            if current_line:
                lines.append(" ".join(current_line))
                
            y_offset = screen_height//2 + 50
            for line in lines:
                txt_penjelasan = font_pembahasan.render(line, True, (255, 255, 255))
                rect_p = txt_penjelasan.get_rect(center=(screen_width//2, y_offset))
                screen.blit(txt_penjelasan, rect_p)
                y_offset += 35
                
            quiz_result_timer -= 1
            if quiz_result_timer <= 0:
                quiz_system.hide_quiz()
                game_state = "PLAYING"
                if player.hp <= 0:
                    print("GAME OVER - HP Habis")
                    game_state = "GAME_OVER"
                
        elif game_state == "GAME_OVER":
            # Tampilkan layar game over dengan nama pemain dan skor kuis
            screens.draw_game_over(screen, player.score, pemain_aktif, skor_kuis_sesi, soal_benar_sesi, total_soal_sesi)

            # === SIMPAN SKOR KE FILE SAAT GAME OVER ===
            # Simpan skor akhir pemain ke file data_skor.json secara otomatis
            if pemain_aktif and not getattr(screens, '_skor_sudah_disimpan', False):
                simpan_skor_pemain(pemain_aktif, skor_kuis_sesi, soal_benar_sesi, total_soal_sesi)
                screens._skor_sudah_disimpan = True  # Tandai agar tidak tersimpan berulang kali

        elif game_state == "LEVEL_SUMMARY":
            if summary_timer > 0:
                summary_timer -= 1
                
            particle_system.update(0)
            
            can_continue = (summary_timer <= 0)
            res_name = getattr(item_manager.altar, 'result_name', '')
            res_fact = getattr(item_manager.altar, 'result_fact', 'Senyawa yang sangat berguna!')
            
            screens.draw_level_summary(screen, res_name, res_fact, can_continue)
            particle_system.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    camera.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
