"""
UI module for SpeedRunner X.
Handles game menus and HUD elements.
"""
import pygame
import pygame_menu
import math
import os
from src.settings import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Load background image for main menu
        self.bg_image = None
        try:
            bg_path = os.path.join("assets", "images", "menu_bg.jpg")
            if os.path.exists(bg_path):
                self.bg_image = pygame.image.load(bg_path)
                self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        except Exception as e:
            print(f"Could not load background image: {e}")
        
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
        """Create a modern main menu"""
        # Create a custom theme
        theme = pygame_menu.themes.Theme()
        theme.background_color = (20, 30, 60, 230)  # Dark blue with transparency
        theme.title_background_color = (30, 50, 100, 255)
        theme.title_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        theme.title_font_size = 60
        theme.title_font_color = (255, 165, 0)  # Orange
        theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        theme.widget_font_size = 36
        theme.widget_font_color = (220, 220, 255)
        theme.selection_color = (255, 140, 0)  # Bright orange for selection
        theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER
        theme.widget_margin = (0, 14)
        
        # Fix for pygame-menu 4.4.3
        theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()
        
        # Create the menu
        self.main_menu = pygame_menu.Menu(
            'SPEEDRUNNER X', 
            WIDTH, HEIGHT,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add subtitle
        self.main_menu.add.label('ULTIMATE CHALLENGE', font_size=36, font_color=(173, 216, 230))
        
        # Add decorative separator
        self.main_menu.add.label('★ ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ ★', font_size=30, font_color=(100, 200, 255))
        self.main_menu.add.vertical_margin(40)
        
        # Add menu buttons
        start_button = self.main_menu.add.button('START GAME', self.start_game, font_size=45)
        self.main_menu.add.vertical_margin(20)
        
        leaderboard_button = self.main_menu.add.button('LEADERBOARD', self.show_leaderboard, font_size=45)
        self.main_menu.add.vertical_margin(20)
        
        exit_button = self.main_menu.add.button('EXIT', pygame_menu.events.EXIT, font_size=45)
        self.main_menu.add.vertical_margin(40)
        
        # Add instructions
        self.main_menu.add.label('HOW TO PLAY', font_size=35, font_color=(255, 165, 0))
        self.main_menu.add.label('✧ ✧ ✧', font_size=24, font_color=(255, 255, 150))
        self.main_menu.add.vertical_margin(10)
        
        self.main_menu.add.label('➤ Arrow Keys / WASD: Move', font_size=28, font_color=(220, 220, 220))
        self.main_menu.add.label('➤ Space: Jump', font_size=28, font_color=(220, 220, 220))
        self.main_menu.add.label('➤ P: Pause Game', font_size=28, font_color=(220, 220, 220))
        
        # Add version info
        self.main_menu.add.vertical_margin(20)
        self.main_menu.add.label('Version 2.0', font_size=18, font_color=(150, 150, 200))
    
    def create_pause_menu(self):
        """Create the pause menu"""
        theme = pygame_menu.themes.Theme()
        theme.background_color = (10, 20, 40, 200)
        theme.title_background_color = (30, 60, 100, 230)
        theme.title_font_size = 48
        theme.title_font_color = (220, 220, 255)
        theme.widget_font_color = (220, 220, 255)
        theme.widget_font_size = 36
        
        # Fix for pygame-menu 4.4.3
        theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()
        
        self.pause_menu = pygame_menu.Menu(
            'GAME PAUSED', 
            WIDTH//2, HEIGHT//2,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add pause icon
        self.pause_menu.add.label('❚❚', font_size=80, font_color=(255, 255, 0))
        self.pause_menu.add.vertical_margin(25)
        
        # Add buttons
        self.pause_menu.add.button('RESUME', self.resume_game, font_size=40)
        self.pause_menu.add.vertical_margin(15)
        self.pause_menu.add.button('RESTART LEVEL', self.restart_level, font_size=40)
        self.pause_menu.add.vertical_margin(15)
        self.pause_menu.add.button('QUIT TO MENU', self.quit_to_menu, font_size=40)
    
    def create_game_over_menu(self):
        """Create the game over menu"""
        theme = pygame_menu.themes.Theme()
        theme.background_color = (40, 10, 10, 220)
        theme.title_background_color = (120, 20, 20, 255)
        theme.title_font_size = 55
        theme.title_font_color = (255, 200, 200)
        theme.widget_font_color = (255, 220, 220)
        theme.widget_font_size = 36
        
        # Fix for pygame-menu 4.4.3
        theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()
        
        self.game_over_menu = pygame_menu.Menu(
            'GAME OVER', 
            WIDTH//2, HEIGHT//2,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add skull icon
        self.game_over_menu.add.label('☠', font_size=100, font_color=(255, 255, 255))
        self.game_over_menu.add.label('You lost all your lives!', font_size=40, font_color=(255, 100, 100))
        self.game_over_menu.add.vertical_margin(30)
        
        # Add buttons
        self.game_over_menu.add.button('RETRY LEVEL', self.restart_level, font_size=40)
        self.game_over_menu.add.vertical_margin(15)
        self.game_over_menu.add.button('QUIT TO MENU', self.quit_to_menu, font_size=40)
    
    def create_victory_menu(self):
        """Create the victory menu"""
        theme = pygame_menu.themes.Theme()
        theme.background_color = (10, 40, 20, 220)
        theme.title_background_color = (20, 80, 40, 255)
        theme.title_font_size = 55
        theme.title_font_color = (220, 255, 220)
        theme.widget_font_color = (220, 255, 220)
        theme.widget_font_size = 36
        
        # Fix for pygame-menu 4.4.3
        theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()
        
        self.victory_menu = pygame_menu.Menu(
            'LEVEL COMPLETE!', 
            WIDTH//2, HEIGHT//2,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add trophy icon
        self.victory_menu.add.label('🏆', font_size=100, font_color=(255, 215, 0))
        self.victory_menu.add.vertical_margin(15)
        
        # Add time display
        self.victory_time_label = self.victory_menu.add.label(
            'Your Time: 00:00.000', font_size=40, font_color=(255, 255, 100))
        
        self.victory_best_label = self.victory_menu.add.label(
            'Best Time: 00:00.000', font_size=40, font_color=(255, 215, 0))
        
        self.victory_menu.add.vertical_margin(25)
        
        # Add buttons
        self.victory_menu.add.button('NEXT LEVEL', self.next_level, font_size=40)
        self.victory_menu.add.vertical_margin(15)
        self.victory_menu.add.button('RETRY LEVEL', self.restart_level, font_size=40)
        self.victory_menu.add.vertical_margin(15)
        self.victory_menu.add.button('QUIT TO MENU', self.quit_to_menu, font_size=40)
    
    # Menu callback placeholders - these will be overridden by the game class
    def start_game(self):
        print("Start game button pressed!")
        pass
    
    def show_leaderboard(self):
        print("Show leaderboard button pressed!")
        pass
    
    def resume_game(self):
        print("Resume game button pressed!")
        pass
    
    def restart_level(self):
        print("Restart level button pressed!")
        pass
    
    def quit_to_menu(self):
        print("Quit to menu button pressed!")
        pass
    
    def next_level(self):
        print("Next level button pressed!")
        pass
    
    def show_powerup_notification(self, powerup_type):
        """Display a notification when player collects a powerup"""
        if powerup_type.lower() == "speed boost":
            self.powerup_message = "SPEED BOOST!"
        elif powerup_type.lower() == "invincibility":
            self.powerup_message = "INVINCIBILITY!"
        elif powerup_type.lower() == "extra life":
            self.powerup_message = "EXTRA LIFE!"
        elif powerup_type.lower() == "checkpoint reached!":
            self.powerup_message = "CHECKPOINT REACHED!"
        else:
            self.powerup_message = powerup_type.upper() + "!"
            
        self.powerup_display_time = pygame.time.get_ticks()
    
    def draw_hud(self, lives, current_level):
        """Draw the HUD (heads-up display)"""
        # Create a semi-transparent HUD background
        hud_height = 70
        hud_surface = pygame.Surface((WIDTH, hud_height), pygame.SRCALPHA)
        
        # Create gradient background for HUD
        for y in range(hud_height):
            alpha = max(180 - y * 2, 50)  # Fade from top to bottom
            pygame.draw.line(hud_surface, (0, 0, 30, alpha), (0, y), (WIDTH, y))
            
        # Add decorative border at the bottom
        pygame.draw.line(hud_surface, (100, 150, 255, 150), (0, hud_height-1), (WIDTH, hud_height-1), 2)
        
        self.screen.blit(hud_surface, (0, 0))
        
        # Draw lives with heart icons
        lives_text = self.font_medium.render("LIVES:", True, (220, 220, 255))
        self.screen.blit(lives_text, (20, 15))
        
        for i in range(lives):
            heart_pos = (lives_text.get_width() + 40 + i * 40, 15)
            self.draw_heart(heart_pos)
        
        # Draw level with a fancy border
        level_text = self.font_medium.render(f"LEVEL {current_level}", True, (255, 255, 100))
        level_rect = level_text.get_rect(center=(WIDTH // 2, 30))
        
        # Draw border
        border_rect = level_rect.inflate(30, 15)
        pygame.draw.rect(self.screen, (0, 100, 255), border_rect, border_radius=8)
        pygame.draw.rect(self.screen, (100, 200, 255), border_rect, 2, border_radius=8)
        
        # Draw level text with shadow
        shadow_rect = level_rect.move(2, 2)
        shadow_text = self.font_medium.render(f"LEVEL {current_level}", True, (0, 0, 0))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(level_text, level_rect)
        
        # Draw timer
        if self.is_timer_running:
            self.current_time = pygame.time.get_ticks() - self.timer_start - self.paused_time
            timer_text = self.font_medium.render(f"TIME: {self.format_time(self.current_time)}", True, (220, 220, 255))
            timer_rect = timer_text.get_rect(topright=(WIDTH - 20, 15))
            
            # Draw timer background
            timer_bg_rect = timer_rect.inflate(30, 15)
            timer_surface = pygame.Surface((timer_bg_rect.width, timer_bg_rect.height), pygame.SRCALPHA)
            timer_surface.fill((0, 0, 100, 150))
            pygame.draw.rect(timer_surface, (100, 150, 255, 200), (0, 0, timer_bg_rect.width, timer_bg_rect.height), 
                            2, border_radius=8)
            
            self.screen.blit(timer_surface, timer_bg_rect)
            
            # Draw timer text with shadow
            shadow_rect = timer_rect.move(2, 2)
            shadow_text = self.font_medium.render(f"TIME: {self.format_time(self.current_time)}", True, (0, 0, 0))
            self.screen.blit(shadow_text, shadow_rect)
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
            pulse = math.sin(current_time / 150) * 0.1 + 1.0
            size = int(45 * pulse)
            powerup_font = pygame.font.Font(None, size)
            
            powerup_text = powerup_font.render(self.powerup_message, True, (255, 255, 0))
            powerup_text.set_alpha(int(alpha))
            
            # Create a background
            text_rect = powerup_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            bg_rect = text_rect.inflate(60, 30)
            
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, int(alpha * 0.7)))
            pygame.draw.rect(bg_surface, (255, 165, 0, int(alpha * 0.9)), 
                            (0, 0, bg_rect.width, bg_rect.height), 2, border_radius=10)
            
            self.screen.blit(bg_surface, bg_rect)
            self.screen.blit(powerup_text, text_rect)
    
    def draw_heart(self, pos, scale=1.0):
        """Draw a heart icon for lives"""
        x, y = pos
        size = int(24 * scale)
        
        # Draw a heart shape
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
        # Create a darkening overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Draw the number
        count_size = 150
        count_font = pygame.font.Font(None, count_size)
        
        # Draw shadow
        shadow_text = count_font.render(str(count), True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(WIDTH/2 + 5, HEIGHT/2 + 5))
        self.screen.blit(shadow_text, shadow_rect)
        
        # Draw main text
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
