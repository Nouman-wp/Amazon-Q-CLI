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
        # Format the message nicely based on powerup type
        if powerup_type.lower() == "speed boost":
            self.powerup_message = "SPEED BOOST!"
        elif powerup_type.lower() == "invincibility":
            self.powerup_message = "INVINCIBILITY!"
        elif powerup_type.lower() == "extra life":
            self.powerup_message = "EXTRA LIFE!"
        else:
            self.powerup_message = powerup_type.upper() + "!"
            
        self.powerup_display_time = pygame.time.get_ticks()
    
    def draw_hud(self, lives, current_level):
        """Draw the HUD (heads-up display)"""
        # Create a semi-transparent HUD background
        hud_surface = pygame.Surface((WIDTH, 100), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(hud_surface, (0, 0))
        
        # Draw lives with heart icons
        lives_text = self.font_medium.render("Lives:", True, WHITE)
        self.screen.blit(lives_text, (20, 20))
        
        for i in range(lives):
            # Draw a heart
            heart_pos = (lives_text.get_width() + 40 + i * 40, 20)
            self.draw_heart(heart_pos)
        
        # Draw level with a fancy border
        level_text = self.font_medium.render(f"Level {current_level}", True, YELLOW)
        level_rect = level_text.get_rect(center=(WIDTH // 2, 30))
        
        # Draw border
        border_rect = level_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, BLUE, border_rect, border_radius=5)
        pygame.draw.rect(self.screen, LIGHT_BLUE, border_rect, 2, border_radius=5)
        
        # Draw level text
        self.screen.blit(level_text, level_rect)
        
        # Draw timer with a fancy display
        if self.is_timer_running:
            self.current_time = pygame.time.get_ticks() - self.timer_start - self.paused_time
            timer_text = self.font_medium.render(f"Time: {self.format_time(self.current_time)}", True, WHITE)
            timer_rect = timer_text.get_rect(topright=(WIDTH - 20, 20))
            
            # Draw timer background
            timer_bg_rect = timer_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, (50, 50, 50, 180), timer_bg_rect, border_radius=5)
            pygame.draw.rect(self.screen, (100, 100, 100), timer_bg_rect, 2, border_radius=5)
            
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
            size = 40
            powerup_font = pygame.font.Font(None, size)
            
            powerup_text = powerup_font.render(self.powerup_message, True, (255, 255, 0))
            powerup_text.set_alpha(int(alpha))
            
            # Create a background for better visibility
            text_rect = powerup_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            bg_rect = text_rect.inflate(40, 20)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, int(alpha * 0.7)))
            
            # Draw background and text
            self.screen.blit(bg_surface, bg_rect)
            self.screen.blit(powerup_text, text_rect)
    
    def draw_heart(self, pos):
        """Draw a heart icon for lives"""
        x, y = pos
        size = 24
        
        # Draw a simple heart shape
        heart_color = (255, 0, 0)  # Red
        
        # Draw the two circles for the top of the heart
        pygame.draw.circle(self.screen, heart_color, (x + size//4, y + size//4), size//4)
        pygame.draw.circle(self.screen, heart_color, (x + size - size//4, y + size//4), size//4)
        
        # Draw the triangle for the bottom of the heart
        pygame.draw.polygon(self.screen, heart_color, [
            (x, y + size//4),
            (x + size//2, y + size),
            (x + size, y + size//4)
        ])
    
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
        # Create a darkening overlay for better visibility
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Simple, large countdown number that's clearly visible
        count_size = 150
        count_font = pygame.font.Font(None, count_size)
        
        # Draw the number with a glow effect
        # First draw shadow
        shadow_text = count_font.render(str(count), True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(WIDTH/2 + 5, HEIGHT/2 + 5))
        self.screen.blit(shadow_text, shadow_rect)
        
        # Then draw main text
        count_text = count_font.render(str(count), True, (255, 255, 0))
        count_rect = count_text.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.screen.blit(count_text, count_rect)
        
        # Add a circle background
        circle_radius = count_size
        pygame.draw.circle(self.screen, (0, 0, 100, 150), (WIDTH/2, HEIGHT/2), circle_radius, 5)
        
        # Add "Get Ready!" text
        ready_text = self.font_medium.render("Get Ready!", True, WHITE)
        ready_rect = ready_text.get_rect(center=(WIDTH/2, HEIGHT/2 + circle_radius + 20))
        self.screen.blit(ready_text, ready_rect)
