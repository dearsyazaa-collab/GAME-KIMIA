import pygame
import cv2

class Screens:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        pygame.font.init()
        self.title_font = pygame.font.SysFont('Arial', 64, bold=True)
        self.subtitle_font = pygame.font.SysFont('Arial', 32)
        self.text_font = pygame.font.SysFont('Arial', 24)

    def draw_login_screen(self, screen, username_text, password_text, active_field, error_msg):
        """Menggambar layar Login/Registrasi dinamis berbasis Pygame."""
        screen.fill((20, 20, 35))  # Latar belakang gelap premium
        
        # === JUDUL UTAMA ===
        title_surf = self.title_font.render("ALCHEMIST ADVENTURE", True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(self.width // 2, 100))
        screen.blit(title_surf, title_rect)
        
        # === SUBTITLE ===
        sub_surf = self.subtitle_font.render("Login atau Daftar untuk Bermain", True, (180, 180, 220))
        sub_rect = sub_surf.get_rect(center=(self.width // 2, 165))
        screen.blit(sub_surf, sub_rect)
        
        # === KOTAK PANEL LOGIN ===
        panel_rect = pygame.Rect(self.width // 2 - 220, 210, 440, 310)
        pygame.draw.rect(screen, (40, 40, 60), panel_rect, border_radius=15)
        pygame.draw.rect(screen, (100, 100, 150), panel_rect, 2, border_radius=15)

        # === FIELD USERNAME ===
        u_label = self.text_font.render("Username", True, (180, 180, 220))
        screen.blit(u_label, (self.width // 2 - 190, 240))

        u_color = (255, 215, 0) if active_field == "username" else (80, 80, 110)
        u_rect = pygame.Rect(self.width // 2 - 190, 270, 380, 44)
        pygame.draw.rect(screen, (30, 30, 50), u_rect, border_radius=8)
        pygame.draw.rect(screen, u_color, u_rect, 2, border_radius=8)
        u_surf = self.text_font.render(username_text, True, (255, 255, 255))
        screen.blit(u_surf, (u_rect.x + 12, u_rect.y + 10))
        
        # Cursor berkedip pada field aktif
        if active_field == "username" and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = u_rect.x + 12 + self.text_font.size(username_text)[0]
            pygame.draw.line(screen, (255, 255, 255), (cursor_x, u_rect.y + 8), (cursor_x, u_rect.y + 34), 2)

        # === FIELD PASSWORD ===
        p_label = self.text_font.render("Password", True, (180, 180, 220))
        screen.blit(p_label, (self.width // 2 - 190, 335))

        p_color = (255, 215, 0) if active_field == "password" else (80, 80, 110)
        p_rect = pygame.Rect(self.width // 2 - 190, 365, 380, 44)
        pygame.draw.rect(screen, (30, 30, 50), p_rect, border_radius=8)
        pygame.draw.rect(screen, p_color, p_rect, 2, border_radius=8)
        p_display = "*" * len(password_text)
        p_surf = self.text_font.render(p_display, True, (255, 255, 255))
        screen.blit(p_surf, (p_rect.x + 12, p_rect.y + 10))

        if active_field == "password" and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = p_rect.x + 12 + self.text_font.size(p_display)[0]
            pygame.draw.line(screen, (255, 255, 255), (cursor_x, p_rect.y + 8), (cursor_x, p_rect.y + 34), 2)
        
        # === TOMBOL ENTER (Visual) ===
        btn_rect = pygame.Rect(self.width // 2 - 100, 435, 200, 50)
        pygame.draw.rect(screen, (80, 60, 160), btn_rect, border_radius=10)
        btn_surf = self.subtitle_font.render("MASUK", True, (255, 255, 255))
        btn_text_rect = btn_surf.get_rect(center=btn_rect.center)
        screen.blit(btn_surf, btn_text_rect)
        
        # === INSTRUKSI NAVIGASI ===
        inst1 = self.text_font.render("TAB / Klik mouse untuk pindah field", True, (120, 120, 160))
        inst2 = self.text_font.render("ENTER untuk Login (atau Daftar Otomatis jika baru)", True, (120, 120, 160))
        screen.blit(inst1, inst1.get_rect(center=(self.width // 2, 550)))
        screen.blit(inst2, inst2.get_rect(center=(self.width // 2, 580)))
        
        # === PESAN ERROR / INFORMASI ===
        if error_msg:
            err_surf = self.text_font.render(error_msg, True, (255, 80, 80))
            err_rect = err_surf.get_rect(center=(self.width // 2, 625))
            # Kotak latar belakang error
            bg_rect = err_rect.inflate(20, 10)
            pygame.draw.rect(screen, (80, 20, 20), bg_rect, border_radius=6)
            screen.blit(err_surf, err_rect)

    def draw_main_menu(self, screen, frame):
        screen.fill((30, 30, 40))  # Dark background
        
        # Title
        title_surf = self.title_font.render("Alchemist Adventure", True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(title_surf, title_rect)
        
        # Instruction
        inst_surf = self.subtitle_font.render("Tekan SPACE untuk Mulai", True, (255, 255, 255))
        inst_rect = inst_surf.get_rect(center=(self.width // 2, self.height // 2 + 50))
        screen.blit(inst_surf, inst_rect)
        
        # Camera Feed
        if frame is not None:
            # Resize frame for PIP (Picture-in-Picture)
            pip_width, pip_height = 160, 120
            resized_frame = cv2.resize(frame, (pip_width, pip_height))
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            # Rotate and flip to match Pygame surface (cv2 is (H,W,C), Pygame is (W,H))
            frame_surface = pygame.surfarray.make_surface(rgb_frame.swapaxes(0, 1))
            
            # Draw frame in bottom right corner
            pip_rect = pygame.Rect(self.width - pip_width - 20, self.height - pip_height - 20, pip_width, pip_height)
            pygame.draw.rect(screen, (255, 255, 255), pip_rect.inflate(4, 4)) # Border
            screen.blit(frame_surface, pip_rect)
            
            cam_text = self.text_font.render("Kamera Aktif", True, (200, 200, 200))
            screen.blit(cam_text, (self.width - pip_width - 20, self.height - pip_height - 50))

    def draw_game_over(self, screen, score, nama_pemain="", skor_kuis=0, soal_benar=0, total_soal=0):
        """
        Menampilkan layar Game Over dengan hasil pencapaian lengkap per pemain.
        Menampilkan: nama pemain, skor gameplay, skor kuis, dan ringkasan jawaban benar.
        """
        screen.fill((30, 10, 20))  # Dark red premium background

        # === JUDUL GAME OVER ===
        title_surf = self.title_font.render("GAME OVER", True, (255, 50, 50))
        title_rect = title_surf.get_rect(center=(self.width // 2, 100))
        screen.blit(title_surf, title_rect)

        # === PANEL HASIL PENCAPAIAN ===
        # Kotak panel untuk menampilkan ringkasan pencapaian pemain
        panel_rect = pygame.Rect(self.width // 2 - 280, 160, 560, 340)
        pygame.draw.rect(screen, (50, 20, 30), panel_rect, border_radius=15)
        pygame.draw.rect(screen, (200, 80, 80), panel_rect, 2, border_radius=15)

        # === TEKS PENCAPAIAN PEMAIN ===
        if nama_pemain:
            # Tampilkan ucapan selamat beserta nama pemain aktif dari sesi login
            if total_soal > 0:
                # Format: "Selamat [nama]! Kamu berhasil menyelesaikan permainan dengan skor: [x]/[total]"
                pesan = f"Selamat {nama_pemain}!"
            else:
                pesan = f"Pemain: {nama_pemain}"
            nama_surf = self.subtitle_font.render(pesan, True, (255, 215, 0))
            nama_rect = nama_surf.get_rect(center=(self.width // 2, 210))
            screen.blit(nama_surf, nama_rect)

        # === SKOR GAMEPLAY (poin dari aksi dalam level) ===
        score_surf = self.subtitle_font.render(f"Skor Permainan: {score}", True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(self.width // 2, 265))
        screen.blit(score_surf, score_rect)

        # === STATISTIK SKOR KUIS ===
        # Garis pemisah visual antara skor game dan skor kuis
        pygame.draw.line(screen, (150, 80, 80),
                         (panel_rect.x + 30, 300), (panel_rect.right - 30, 300), 1)

        # Label bagian kuis
        kuis_label = self.text_font.render("--- Hasil Kuis Edukatif ---", True, (180, 180, 220))
        screen.blit(kuis_label, kuis_label.get_rect(center=(self.width // 2, 320)))

        # Hitung skor maksimal yang bisa diraih (setiap soal bernilai 20 poin)
        maks = total_soal * 20
        maks_str = str(maks) if total_soal > 0 else "0"

        # Tampilkan skor kuis dengan format "Skor Kuis: X/Y"
        kuis_surf = self.subtitle_font.render(
            f"Skor Kuis: {skor_kuis}/{maks_str}", True, (100, 255, 150))
        kuis_rect = kuis_surf.get_rect(center=(self.width // 2, 360))
        screen.blit(kuis_surf, kuis_rect)

        # Tampilkan jumlah soal yang berhasil dijawab benar dari total soal
        detail_surf = self.text_font.render(
            f"Soal Benar: {soal_benar} dari {total_soal} soal", True, (200, 200, 200))
        detail_rect = detail_surf.get_rect(center=(self.width // 2, 400))
        screen.blit(detail_surf, detail_rect)

        # Tampilkan kalimat ringkasan pencapaian akhir pemain
        if nama_pemain and total_soal > 0:
            ringkasan = f"{nama_pemain} menyelesaikan permainan dengan skor kuis: {skor_kuis}/{maks_str}"
            ring_surf = self.text_font.render(ringkasan, True, (255, 220, 100))
            ring_rect = ring_surf.get_rect(center=(self.width // 2, 450))
            screen.blit(ring_surf, ring_rect)

        # === INSTRUKSI ===
        inst_surf = self.text_font.render("Tekan R untuk Ulangi", True, (180, 180, 180))
        inst_rect = inst_surf.get_rect(center=(self.width // 2, 540))
        screen.blit(inst_surf, inst_rect)

    def draw_level_complete(self, screen, score):
        screen.fill((10, 50, 10))  # Dark green background
        
        # Title
        title_surf = self.title_font.render("LEVEL SELESAI!", True, (50, 255, 50))
        title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(title_surf, title_rect)
        
        # Subtitle
        sub_surf = self.subtitle_font.render("Senyawa Terbentuk!", True, (255, 215, 0))
        sub_rect = sub_surf.get_rect(center=(self.width // 2, self.height // 2 + 10))
        screen.blit(sub_surf, sub_rect)
        
        # Score
        score_surf = self.text_font.render(f"Skor Saat Ini: {score}", True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(self.width // 2, self.height // 2 + 60))
        screen.blit(score_surf, score_rect)
        
        # Instruction
        inst_surf = self.text_font.render("Tekan SPACE untuk Lanjut", True, (200, 200, 200))
        inst_rect = inst_surf.get_rect(center=(self.width // 2, self.height // 2 + 110))
        screen.blit(inst_surf, inst_rect)

    def draw_level_summary(self, screen, compound_name, compound_fact, can_continue):
        screen.fill((20, 20, 40))  # Dark blue background
        
        # Title
        title_surf = self.title_font.render("REAKSI BERHASIL!", True, (50, 255, 50))
        title_rect = title_surf.get_rect(center=(self.width // 2, 100))
        screen.blit(title_surf, title_rect)
        
        # Senyawa Terbentuk
        sub_surf = self.subtitle_font.render(f"Senyawa Terbentuk: {compound_name}", True, (255, 215, 0))
        sub_rect = sub_surf.get_rect(center=(self.width // 2, 200))
        screen.blit(sub_surf, sub_rect)
        
        # Visual/Kotak Fakta
        fact_rect = pygame.Rect(self.width // 8, 280, self.width * 3 // 4, 250)
        pygame.draw.rect(screen, (50, 50, 70), fact_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), fact_rect, 2, border_radius=10)
        
        # Override compound_fact based on compound_name for casual language
        if compound_name == "NaCl":
            compound_fact = "Na itu murah hati, dia kasih 1 elektronnya ke Cl yang butuh. Hasilnya? Ikatan Ion yang kuat kayak cinta mereka!"
        elif compound_name == "H2O":
            compound_fact = "H dan O itu tim solid. Mereka patungan (sharing) elektron biar sama-sama stabil. Itulah Ikatan Kovalen!"
        elif compound_name == "Lithium":
            compound_fact = "Di pusat atom ada 'geng' Proton dan Neutron. Mereka yang nentuin massa atom. Makin banyak mereka, makin berat atomnya!"
            
        # Teks Edukasi (Fakta Senyawa) - Simple word wrap
        words = compound_fact.split(' ')
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if self.text_font.size(test_line)[0] > fact_rect.width - 40:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
            
        y_offset = 310
        for line in lines:
            line_surf = self.text_font.render(line, True, (255, 255, 255))
            line_rect = line_surf.get_rect(center=(self.width // 2, y_offset))
            screen.blit(line_surf, line_rect)
            y_offset += 35
            
        # Instruction
        if can_continue:
            # Berkedip
            if pygame.time.get_ticks() % 1000 < 500:
                inst_surf = self.subtitle_font.render("Tekan SPACE untuk Lanjut", True, (200, 255, 200))
                inst_rect = inst_surf.get_rect(center=(self.width // 2, self.height - 100))
                screen.blit(inst_surf, inst_rect)
        else:
            inst_surf = self.text_font.render("Membaca informasi...", True, (150, 150, 150))
            inst_rect = inst_surf.get_rect(center=(self.width // 2, self.height - 100))
            screen.blit(inst_surf, inst_rect)

