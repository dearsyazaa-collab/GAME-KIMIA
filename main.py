import pygame
import sys
import random
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

    # Initialize modules
    camera = CameraTracker(device_index=0)
    camera.start()
    level_manager = LevelManager(screen_width, screen_height)
    physics_engine = PhysicsEngine(gravity=0.8, terminal_velocity=18)
    item_manager = ItemManager()
    player = Player(200, 400) # Starting safe position
    dashboard = Dashboard()
    quiz_system = QuizSystem()
    screens = Screens(screen_width, screen_height)
    particle_system = ParticleSystem()
    
    game_state = "MENU"
    game_paused = False
    countdown_timer = 0

    # Load level pertama
    level_manager.load_level(1, item_manager)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if game_state == "MENU":
                    if event.key == pygame.K_SPACE:
                        game_state = "GET_READY"
                        countdown_timer = 180
                elif game_state == "GAME_OVER":
                    if event.key == pygame.K_r:
                        # Reset game
                        player = Player(200, 400)
                        item_manager = ItemManager()
                        level_manager.current_level = 1
                        level_manager.load_level(1, item_manager)
                        game_state = "GET_READY"
                        countdown_timer = 180
                        game_paused = False
                elif game_state == "LEVEL_COMPLETE":
                    if event.key == pygame.K_SPACE:
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

        # 1. Input Processing (Camera is always running)
        with camera.lock:
            frame = camera.current_frame
            pose = camera.current_pose
            finger_pos = getattr(camera, 'current_index_finger_pos', None)
        
        # --- STATE MACHINE RENDERING & LOGIC ---
        if game_state == "MENU":
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
            # 2. Game Logic / Level Update
            if not game_paused:
                player.update(pose)
                level_manager.update()
                
                # Scroll item manager at the exact speed of ground
                item_manager.update(level_manager.platform_speed, screen_width)
                particle_system.update(level_manager.platform_speed)
                
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
                            print("Mendapat QuestionBlock! Kuis dimulai.")
                            game_paused = True
                            quiz_system.show_quiz()
                            item_manager.items.remove(item)
                        else:
                            print(f"Mendapat {item.atom_type}!")
                            player.inventory[item.atom_type] = player.inventory.get(item.atom_type, 0) + 1
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
                        # Hancurkan kayu jika pose SIHIR API dan tangan menunjuk ke KAYU
                        if target_hit and pose == "SIHIR API" and player.magic_cooldown == 0:
                            obs.is_destroying = True
                            obs.destroy_timer = 30
                            print("KAYU mulai dihancurkan dengan SIHIR API (Target Tangan)!")
                            player.score += 50
                            player.magic_cooldown = 180
                            # Ledakan awal partikel api
                            particle_system.add_particles(obs.rect.centerx, obs.rect.centery, color=(255, 69, 0), count=20, speed=3)
                        elif player.rect.colliderect(obs.rect):
                            # Dorong pemain agar tidak bisa lewat (berlaku seperti dinding)
                            if player.rect.right > obs.rect.left and player.rect.centerx < obs.rect.left:
                                player.rect.right = obs.rect.left
                                
                    elif obs.obs_type == "SUNGAI_BERACUN":
                        # Bekukan sungai jika pose SIHIR ES dan tangan menunjuk ke SUNGAI_BERACUN
                        if target_hit and pose == "SIHIR ES" and player.magic_cooldown == 0:
                            obs.obs_type = "PIJAKAN_ES"
                            print("SUNGAI BERACUN dibekukan menjadi PIJAKAN ES (Target Tangan)!")
                            player.score += 50
                            player.magic_cooldown = 180
                            # Partikel es memancar ke atas
                            particle_system.add_particles(obs.rect.centerx, obs.rect.y, color=(200, 255, 255), count=30, speed=2, style="fountain")
                        elif player.rect.colliderect(obs.rect):
                            # Kurangi HP jika menginjak racun dan sedang tidak kebal
                            if player.invulnerable_timer == 0:
                                player.hp -= 15
                                player.invulnerable_timer = 90 # 1.5 detik kebal
                                if player.hp <= 0:
                                    print("GAME OVER - Terkena Sungai Beracun")
                                    game_state = "GAME_OVER"
            else:
                # Game dalam state Pause untuk Kuis
                quiz_result = quiz_system.check_answer(finger_pos, pose)
                if quiz_result is not None:
                    if quiz_result:
                        print("Kuis: Jawaban Benar! (+100 Skor)")
                        player.score += 100
                    else:
                        print("Kuis: Jawaban Salah! (-10 HP)")
                        player.hp -= 10
                        
                    game_paused = False # Lanjutkan game setelah menjawab
                    if player.hp <= 0:
                        print("GAME OVER - HP Habis")
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
                        
                        # Lanjut level: Pindah ke state LEVEL_COMPLETE
                        game_state = "LEVEL_COMPLETE"
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
                
            if game_paused:
                quiz_system.draw(screen, finger_pos)
                
        elif game_state == "GAME_OVER":
            screens.draw_game_over(screen, player.score)
            
        elif game_state == "LEVEL_COMPLETE":
            screens.draw_level_complete(screen, player.score)

        pygame.display.flip()
        clock.tick(60)

    camera.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
