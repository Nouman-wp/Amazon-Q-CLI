"""
UI module for SpeedRunner X.
Handles game menus and HUD elements.
"""
import pygame
import pygame_menu
import math  # Add math module import at the top level
from src.settings import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Create menus
        self.create_main_menu()
        self.create_pause_menu()
        self.create_game_over_menu()
        self.create_victory_menu()
        
        # HUD elements
        self.timer_start = 0
        self.current_time = 0
        self.paused_time = 0
        self.is_timer_running = False
        
        # Powerup notification
        self.powerup_message = ""
        self.powerup_display_time = 0
        self.powerup_duration = 3000  # Display for 3 seconds
    
    def create_main_menu(self):
        """Create the main menu"""
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.widget_font_size = 36
        theme.title_font_size = 60
        theme.title_background_color = (0, 0, 100)
        theme.background_color = (0, 0, 50, 200)
        theme.widget_font_color = (255, 255, 255)
        theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER
        
        # Enhanced UI with custom colors and styling
        theme.title_font_shadow = True
        theme.title_font_shadow_color = (0, 0, 0)
        theme.title_font_shadow_offset = 2
        theme.widget_font_shadow = True
        theme.widget_font_shadow_color = (0, 0, 0)
        theme.widget_font_shadow_offset = 2
        theme.widget_margin = (0, 10)
        theme.widget_padding = 10
        
        self.main_menu = pygame_menu.Menu(
            'SpeedRunner X', 
            WIDTH, HEIGHT,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add a decorative header with game logo
        self.main_menu.add.label('SPEEDRUNNER X', font_size=70, font_color=(255, 215, 0))
        self.main_menu.add.label('The Ultimate Platform Adventure', font_size=30, font_color=(173, 216, 230))
        
        # Add decorative line
        self.main_menu.add.label('⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯', font_size=30, font_color=(100, 200, 255))
        self.main_menu.add.vertical_margin(20)
        
        # Add menu buttons directly without frames
        self.main_menu.add.button('START GAME', self.start_game, font_size=40, 
                                 background_color=(0, 100, 0))
        self.main_menu.add.vertical_margin(10)
        self.main_menu.add.button('LEADERBOARD', self.show_leaderboard, font_size=40,
                                 background_color=(0, 0, 100))
        self.main_menu.add.vertical_margin(10)
        self.main_menu.add.button('EXIT', pygame_menu.events.EXIT, font_size=40,
                                 background_color=(100, 0, 0))
        
        self.main_menu.add.vertical_margin(30)
        
        # Add game instructions
        self.main_menu.add.label('HOW TO PLAY', font_size=30, font_color=(255, 165, 0))
        self.main_menu.add.label('Arrow Keys / WASD: Move', font_size=24)
        self.main_menu.add.label('Space: Jump', font_size=24)
        self.main_menu.add.label('Jump on enemies to defeat them!', font_size=24)
        self.main_menu.add.label('Collect powerups for special abilities!', font_size=24)
        
        # Add version info
        self.main_menu.add.vertical_margin(20)
        self.main_menu.add.label('Version 1.0', font_size=16, font_color=(150, 150, 150))
    
    def create_pause_menu(self):
        """Create the pause menu"""
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.widget_font_size = 32
        theme.title_font_size = 40
        theme.title_background_color = (0, 0, 100)
        theme.background_color = (0, 0, 50, 200)
        theme.widget_font_color = (255, 255, 255)
        
        # Enhanced UI with custom colors and styling
        theme.title_font_shadow = True
        theme.title_font_shadow_color = (0, 0, 0)
        theme.title_font_shadow_offset = 2
        theme.widget_font_shadow = True
        theme.widget_font_shadow_color = (0, 0, 0)
        theme.widget_font_shadow_offset = 2
        theme.widget_margin = (0, 10)
        theme.widget_padding = 10
        
        self.pause_menu = pygame_menu.Menu(
            'GAME PAUSED', 
            WIDTH//2, HEIGHT//2,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add a decorative pause icon
        self.pause_menu.add.label('❚❚', font_size=60, font_color=(255, 255, 0))
        self.pause_menu.add.vertical_margin(20)
        
        # Add buttons directly without frames
        self.pause_menu.add.button('RESUME', self.resume_game, font_size=36,
                                  background_color=(0, 100, 0))
        self.pause_menu.add.vertical_margin(10)
        self.pause_menu.add.button('RESTART LEVEL', self.restart_level, font_size=36,
                                  background_color=(0, 0, 100))
        self.pause_menu.add.vertical_margin(10)
        self.pause_menu.add.button('QUIT TO MENU', self.quit_to_menu, font_size=36,
                                  background_color=(100, 0, 0))
        
        # Add keyboard shortcut hints
        self.pause_menu.add.vertical_margin(20)
        self.pause_menu.add.label('ESC: Resume   R: Restart', font_size=20, font_color=(200, 200, 200))
    
    def create_game_over_menu(self):
        """Create the game over menu"""
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.widget_font_size = 32
        theme.title_font_size = 50
        theme.title_background_color = (150, 0, 0)  # Dark red
        theme.background_color = (50, 0, 0, 200)  # Semi-transparent dark red
        theme.widget_font_color = (255, 255, 255)
        
        # Enhanced UI with custom colors and styling
        theme.title_font_shadow = True
        theme.title_font_shadow_color = (0, 0, 0)
        theme.title_font_shadow_offset = 2
        theme.widget_font_shadow = True
        theme.widget_font_shadow_color = (0, 0, 0)
        theme.widget_font_shadow_offset = 2
        theme.widget_margin = (0, 10)
        theme.widget_padding = 10
        
        self.game_over_menu = pygame_menu.Menu(
            'GAME OVER', 
            WIDTH//2, HEIGHT//2,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add a decorative skull icon
        self.game_over_menu.add.label('☠', font_size=80, font_color=(255, 255, 255))
        self.game_over_menu.add.label('You lost all your lives!', font_size=36, font_color=(255, 100, 100))
        self.game_over_menu.add.vertical_margin(30)
        
        # Add buttons directly without frames
        self.game_over_menu.add.button('RETRY LEVEL', self.restart_level, font_size=36,
                                      background_color=(0, 100, 0))
        self.game_over_menu.add.vertical_margin(15)
        self.game_over_menu.add.button('QUIT TO MENU', self.quit_to_menu, font_size=36,
                                      background_color=(100, 0, 0))
        
        # Add keyboard shortcut hints
        self.game_over_menu.add.vertical_margin(20)
        self.game_over_menu.add.label('R: Retry   ESC: Quit to Menu', font_size=20, font_color=(200, 200, 200))
    
    def create_victory_menu(self):
        """Create the victory menu"""
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.widget_font_size = 32
        theme.title_font_size = 50
        theme.title_background_color = (0, 100, 0)  # Dark green
        theme.background_color = (20, 50, 20, 200)  # Semi-transparent dark green
        theme.widget_font_color = (255, 255, 255)
        
        # Enhanced UI with custom colors and styling
        theme.title_font_shadow = True
        theme.title_font_shadow_color = (0, 0, 0)
        theme.title_font_shadow_offset = 2
        theme.widget_font_shadow = True
        theme.widget_font_shadow_color = (0, 0, 0)
        theme.widget_font_shadow_offset = 2
        theme.widget_margin = (0, 10)
        theme.widget_padding = 10
        
        self.victory_menu = pygame_menu.Menu(
            'LEVEL COMPLETE!', 
            WIDTH//2, HEIGHT//2,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add a decorative trophy icon
        self.victory_menu.add.label('🏆', font_size=80, font_color=(255, 215, 0))
        self.victory_menu.add.vertical_margin(10)
        
        # Add time display
        self.victory_time_label = self.victory_menu.add.label(
            'Your Time: 00:00.000', font_size=36, font_color=(255, 255, 0))
        self.victory_best_label = self.victory_menu.add.label(
            'Best Time: 00:00.000', font_size=36, font_color=(255, 215, 0))
        
        self.victory_menu.add.vertical_margin(20)
        
        # Add buttons directly without frames
        self.victory_menu.add.button('NEXT LEVEL', self.next_level, font_size=36,
                                   background_color=(0, 100, 0))
        self.victory_menu.add.vertical_margin(10)
        self.victory_menu.add.button('RETRY LEVEL', self.restart_level, font_size=36,
                                   background_color=(0, 0, 100))
        self.victory_menu.add.vertical_margin(10)
        self.victory_menu.add.button('QUIT TO MENU', self.quit_to_menu, font_size=36,
                                   background_color=(100, 0, 0))
        
        # Add keyboard shortcut hints
        self.victory_menu.add.vertical_margin(20)
        self.victory_menu.add.label('N: Next Level   R: Retry   ESC: Quit to Menu', font_size=20, font_color=(200, 200, 200))
    
    # Menu callback placeholders - these will be overridden by the game class
    def start_game(self):
        print("Start game button pressed!")  # Debug print
        pass
    
    def show_leaderboard(self):
        print("Show leaderboard button pressed!")  # Debug print
        pass
    
    def resume_game(self):
        print("Resume game button pressed!")  # Debug print
        pass
    
    def restart_level(self):
        print("Restart level button pressed!")  # Debug print
        pass
    
    def quit_to_menu(self):
        print("Quit to menu button pressed!")  # Debug print
        pass
    
    def next_level(self):
        print("Next level button pressed!")  # Debug print
        pass
    
    def show_powerup_notification(self, powerup_type):
        """Display a notification when player collects a powerup"""
        self.powerup_message = powerup_type.upper() + " ACTIVATED!"
        self.powerup_display_time = pygame.time.get_ticks()
    
    def draw_hud(self, lives, current_level):
        """Draw the HUD (heads-up display)"""
        # Create a semi-transparent HUD background with gradient
        hud_height = 100
        hud_surface = pygame.Surface((WIDTH, hud_height), pygame.SRCALPHA)
        
        # Create gradient background
        for y in range(hud_height):
            alpha = max(128 - y, 0)  # Fade out as we go down
            pygame.draw.line(hud_surface, (0, 0, 0, alpha), (0, y), (WIDTH, y))
        
        self.screen.blit(hud_surface, (0, 0))
        
        # Draw decorative border at the bottom of HUD
        pygame.draw.line(self.screen, (100, 100, 255, 128), (0, hud_height-1), (WIDTH, hud_height-1), 2)
        
        # Draw lives with animated heart icons
        lives_text = self.font_medium.render("Lives:", True, WHITE)
        self.screen.blit(lives_text, (20, 20))
        
        for i in range(lives):
            # Draw a heart with pulsing effect
            heart_pos = (lives_text.get_width() + 40 + i * 40, 20)
            pulse = 0.1 * abs(math.sin(pygame.time.get_ticks() / 500))
            self.draw_heart(heart_pos, 1.0 + pulse)
        
        # Draw level with a fancy border and glow effect
        level_text = self.font_medium.render(f"Level {current_level}", True, YELLOW)
        level_rect = level_text.get_rect(center=(WIDTH // 2, 30))
        
        # Draw glow
        glow_surf = pygame.Surface((level_rect.width + 40, level_rect.height + 20), pygame.SRCALPHA)
        for i in range(10, 0, -2):
            alpha = 10 * i
            color = (0, 0, 255, alpha)
            pygame.draw.rect(glow_surf, color, 
                            (10-i, 10-i, level_rect.width + i*2, level_rect.height + i*2), 
                            border_radius=10)
        
        # Draw border
        border_rect = level_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, BLUE, border_rect, border_radius=5)
        pygame.draw.rect(self.screen, LIGHT_BLUE, border_rect, 2, border_radius=5)
        
        # Draw level text with shadow
        shadow_text = self.font_medium.render(f"Level {current_level}", True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 2, 32))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(level_text, level_rect)
        
        # Draw timer with a fancy display
        if self.is_timer_running:
            self.current_time = pygame.time.get_ticks() - self.timer_start - self.paused_time
            timer_text = self.font_medium.render(f"Time: {self.format_time(self.current_time)}", True, WHITE)
            timer_rect = timer_text.get_rect(topright=(WIDTH - 20, 20))
            
            # Draw timer background with gradient
            timer_bg_rect = timer_rect.inflate(20, 10)
            timer_bg_surf = pygame.Surface((timer_bg_rect.width, timer_bg_rect.height), pygame.SRCALPHA)
            for y in range(timer_bg_rect.height):
                alpha = 180 - y * 3
                if alpha > 0:
                    pygame.draw.line(timer_bg_surf, (50, 50, 50, alpha), 
                                    (0, y), (timer_bg_rect.width, y))
            
            self.screen.blit(timer_bg_surf, timer_bg_rect)
            pygame.draw.rect(self.screen, (100, 100, 100), timer_bg_rect, 2, border_radius=5)
            
            # Draw timer text with shadow
            shadow_timer = self.font_medium.render(f"Time: {self.format_time(self.current_time)}", True, (0, 0, 0))
            shadow_timer_rect = shadow_timer.get_rect(topright=(WIDTH - 18, 22))
            self.screen.blit(shadow_timer, shadow_timer_rect)
            self.screen.blit(timer_text, timer_rect)
        
        # Draw powerup notification if active
        current_time = pygame.time.get_ticks()
        if current_time - self.powerup_display_time < self.powerup_duration:
            # Calculate alpha for fade effect
            alpha = 255
            if current_time - self.powerup_display_time > self.powerup_duration - 1000:
                # Fade out in the last second
                alpha = 255 * (1 - (current_time - self.powerup_display_time - (self.powerup_duration - 1000)) / 1000)
            
            # Create notification text with pulsing effect
            pulse = 0.1 * abs(math.sin((current_time - self.powerup_display_time) / 100))
            size = int(40 + pulse * 10)
            powerup_font = pygame.font.Font(None, size)
            
            powerup_text = powerup_font.render(self.powerup_message, True, (255, 255, 0))
            powerup_text.set_alpha(int(alpha))
            
            # Create a background for better visibility
            text_rect = powerup_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            bg_rect = text_rect.inflate(40, 20)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            
            # Gradient background
            for y in range(bg_rect.height):
                bg_alpha = min(int(alpha * 0.7), 180)
                color_value = max(0, 50 - abs(y - bg_rect.height//2) * 2)
                pygame.draw.line(bg_surface, (color_value, color_value, color_value, bg_alpha), 
                                (0, y), (bg_rect.width, y))
            
            # Draw background and text
            self.screen.blit(bg_surface, bg_rect)
            
            # Draw glowing border
            pygame.draw.rect(self.screen, (255, 255, 0, int(alpha * 0.5)), bg_rect, 2, border_radius=10)
            
            # Draw text with shadow
            shadow_powerup = powerup_font.render(self.powerup_message, True, (0, 0, 0))
            shadow_powerup.set_alpha(int(alpha * 0.7))
            shadow_rect = shadow_powerup.get_rect(center=(WIDTH // 2 + 2, HEIGHT // 4 + 2))
            self.screen.blit(shadow_powerup, shadow_rect)
            self.screen.blit(powerup_text, text_rect)
            
            # Add a glowing effect
            glow_size = int(size * 1.1)
            glow_font = pygame.font.Font(None, glow_size)
            glow_text = glow_font.render(self.powerup_message, True, (255, 255, 0, int(alpha * 0.3)))
            glow_rect = glow_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            self.screen.blit(glow_text, glow_rect)
            
            # Add animated particles around the text
            particle_count = 10
            for i in range(particle_count):
                angle = (current_time / 200 + i * (2 * math.pi / particle_count)) % (2 * math.pi)
                distance = 50 + 10 * math.sin(current_time / 300 + i)
                x = WIDTH // 2 + math.cos(angle) * distance
                y = HEIGHT // 4 + math.sin(angle) * distance
                size = 3 + 2 * math.sin(current_time / 200 + i)
                particle_alpha = int(alpha * 0.8)
                pygame.draw.circle(self.screen, (255, 255, 0, particle_alpha), (int(x), int(y)), int(size))
    
    def draw_heart(self, pos, scale=1.0):
        """Draw a heart icon for lives with optional scaling"""
        x, y = pos
        size = 24 * scale
        
        # Draw a simple heart shape
        heart_color = (255, 0, 0)  # Red
        
        # Create a surface for the heart
        heart_surf = pygame.Surface((size*1.2, size*1.2), pygame.SRCALPHA)
        
        # Draw the two circles for the top of the heart
        pygame.draw.circle(heart_surf, heart_color, (size//3, size//3), size//3)
        pygame.draw.circle(heart_surf, heart_color, (size - size//3, size//3), size//3)
        
        # Draw the triangle for the bottom of the heart
        pygame.draw.polygon(heart_surf, heart_color, [
            (0, size//3),
            (size//2, size),
            (size, size//3)
        ])
        
        # Add a shine effect
        pygame.draw.circle(heart_surf, (255, 200, 200), (size//4, size//4), size//8)
        
        # Blit the heart to the screen
        self.screen.blit(heart_surf, (x - size*0.6, y - size*0.6))
    
    def start_timer(self):
        """Start the game timer"""
        self.timer_start = pygame.time.get_ticks()
        self.is_timer_running = True
        self.paused_time = 0
    
    def pause_timer(self):
        """Pause the game timer"""
        if self.is_timer_running:
            self.current_time = pygame.time.get_ticks() - self.timer_start - self.paused_time
            self.is_timer_running = False
    
    def resume_timer(self):
        """Resume the game timer"""
        if not self.is_timer_running:
            self.paused_time += pygame.time.get_ticks() - self.timer_start - self.current_time
            self.is_timer_running = True
    
    def format_time(self, milliseconds):
        """Format time in milliseconds to MM:SS.mmm"""
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        milliseconds = milliseconds % 1000
        return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    
    def get_elapsed_time(self):
        """Get the elapsed time in milliseconds"""
        if self.is_timer_running:
            return pygame.time.get_ticks() - self.timer_start - self.paused_time
        else:
            return self.current_time
    
    def reset_timer(self):
        """Reset the game timer"""
        self.timer_start = pygame.time.get_ticks()
        self.is_timer_running = True
        self.paused_time = 0
        self.current_time = 0
    
    def update_victory_menu(self, current_time, best_time):
        """Update the victory menu with current and best times"""
        # Format times
        current_time_str = self.format_time(current_time)
        best_time_str = self.format_time(best_time) if best_time else "None"
        
        # Update labels
        self.victory_time_label.set_title(f"Your Time: {current_time_str}")
        self.victory_best_label.set_title(f"Best Time: {best_time_str}")
        
    def draw_countdown(self, count):
        """Draw countdown before level starts"""
        # Create a fancy countdown display with multiple effects
        
        # Create a darkening overlay for better visibility
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Calculate pulsing effect
        pulse_time = pygame.time.get_ticks() % 1000
        pulse_scale = 1.0
        if pulse_time < 500:
            pulse_scale = 1.0 + (pulse_time / 500) * 0.5
        else:
            pulse_scale = 1.5 - ((pulse_time - 500) / 500) * 0.5
            
        count_size = int(150 * pulse_scale)
        
        # Create a larger font for the countdown
        count_font = pygame.font.Font(None, count_size)
        
        # Create glowing layers with different colors
        colors = [
            (255, 0, 0, 50),    # Red glow
            (255, 165, 0, 80),  # Orange glow
            (255, 255, 0, 120), # Yellow glow
            (255, 255, 255)     # White text
        ]
        
        # Draw multiple layers for glow effect
        for i, color in enumerate(colors):
            size_offset = (len(colors) - i - 1) * 15
            glow_font = pygame.font.Font(None, count_size + size_offset)
            glow_text = glow_font.render(str(count), True, color)
            glow_rect = glow_text.get_rect(center=(WIDTH/2, HEIGHT/2))
            self.screen.blit(glow_text, glow_rect)
        
        # Add a circle background
        circle_radius = count_size + 30
        for i in range(5):
            alpha = 150 - i * 30
            if alpha > 0:
                pygame.draw.circle(self.screen, (0, 0, 100, alpha), (WIDTH/2, HEIGHT/2), circle_radius + i*10)
        
        pygame.draw.circle(self.screen, (0, 0, 200, 150), (WIDTH/2, HEIGHT/2), circle_radius)
        pygame.draw.circle(self.screen, (100, 100, 255, 200), (WIDTH/2, HEIGHT/2), circle_radius, 5)
        
        # Add "Get Ready!" text with animation
        ready_text = "Get Ready!"
        char_spacing = 20
        total_width = len(ready_text) * char_spacing
        
        for i, char in enumerate(ready_text):
            # Calculate vertical bounce for each character
            char_time = (pygame.time.get_ticks() + i * 100) % 1000
            y_offset = abs(math.sin(char_time / 1000 * math.pi * 2)) * 10
            
            # Calculate position
            x_pos = WIDTH/2 - total_width/2 + i * char_spacing
            y_pos = HEIGHT/2 + circle_radius + 40 - y_offset
            
            # Draw character with shadow
            char_font = self.font_medium
            shadow = char_font.render(char, True, (0, 0, 0))
            text = char_font.render(char, True, WHITE)
            
            self.screen.blit(shadow, (x_pos + 2, y_pos + 2))
            self.screen.blit(text, (x_pos, y_pos))
        
        # Add particles around the countdown
        particle_count = 20
        for i in range(particle_count):
            angle = (pygame.time.get_ticks() / 200 + i * (2 * math.pi / particle_count)) % (2 * math.pi)
            distance = circle_radius + 20 + 10 * math.sin(pygame.time.get_ticks() / 300 + i)
            x = WIDTH/2 + math.cos(angle) * distance
            y = HEIGHT/2 + math.sin(angle) * distance
            size = 3 + 2 * math.sin(pygame.time.get_ticks() / 200 + i)
            
            # Gradient color based on position
            r = 255
            g = int(128 + 127 * math.sin(angle))
            b = int(128 + 127 * math.cos(angle))
            
            pygame.draw.circle(self.screen, (r, g, b), (int(x), int(y)), int(size))
