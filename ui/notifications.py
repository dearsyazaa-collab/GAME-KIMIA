import pygame

class NotificationManager:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.notifications = []
        self.pending_notifications = []

    def add_notification(self, text, color, duration=240, font_size=24, delay=0):
        if delay > 0:
            self.pending_notifications.append({
                "delay": delay, 
                "text": text, 
                "color": color, 
                "duration": duration, 
                "font_size": font_size
            })
        else:
            font = pygame.font.SysFont("Verdana", font_size, bold=True)
            self.notifications.append({
                "text": text,
                "color": color,
                "duration": duration,
                "max_duration": duration,
                "font": font,
                "y": 80 # Posisi awalnya sedikit di bawah HUD
            })

    def update(self):
        # Update pending notifications
        for p in self.pending_notifications[:]:
            p["delay"] -= 1
            if p["delay"] <= 0:
                self.add_notification(p["text"], p["color"], p["duration"], p["font_size"], 0)
                self.pending_notifications.remove(p)

        # Update active notifications (Queue behavior)
        if len(self.notifications) > 0:
            active_notif = self.notifications[0]
            active_notif["duration"] -= 1
            active_notif["y"] -= 0.1 # Melayang lebih lambat
            if active_notif["duration"] <= 0:
                self.notifications.pop(0)

    def draw(self, surface):
        if len(self.notifications) > 0:
            notif = self.notifications[0]
            
            # Fade out effect in the last quarter of the duration
            alpha = 255
            fade_duration = notif["max_duration"] / 4
            if notif["duration"] < fade_duration:
                alpha = int((notif["duration"] / fade_duration) * 255)
            
            if alpha <= 0:
                return
                
            y_pos = notif["y"]
            
            txt_surface = notif["font"].render(notif["text"], True, notif["color"])
            out_surface = notif["font"].render(notif["text"], True, (0, 0, 0)) # Outline color
            
            txt_surface.set_alpha(alpha)
            out_surface.set_alpha(alpha)
            
            rect = txt_surface.get_rect(center=(self.screen_width // 2, int(y_pos)))
            
            # Draw outline (stroke)
            offsets = [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, -2), (0, 2), (-2, 0), (2, 0)]
            for dx, dy in offsets:
                surface.blit(out_surface, (rect.x + dx, rect.y + dy))
                
            # Draw text
            surface.blit(txt_surface, rect)
