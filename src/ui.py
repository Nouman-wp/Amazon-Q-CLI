"""
UI module for SpeedRunner X.
Handles game menus and HUD elements.
"""
import pygame
import pygame_menu
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
    
    def create_main_menu(self):
        """Create the main menu"""
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.widget_font_size = 36
        
        self.main_menu = pygame_menu.Menu(
            'SpeedRunner X', 
            WIDTH, HEIGHT,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True
        )
        
        self.main_menu.add.button('Start Game', self.start_game)
        self.main_menu.add.button('Leaderboard', self.show_leaderboard)
        self.main_menu.add.button('Exit', pygame_menu.events.EXIT)
    
    def create_pause_menu(self):
        """Create the pause menu"""
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.widget_font_size = 32
        
        self.pause_menu = pygame_menu.Menu(
            'Paused', 
            WIDTH//2, HEIGHT//2,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True
        )
        
        self.pause_menu.add.button('Resume', self.resume_game)
        self.pause_menu.add.button('Restart Level', self.restart_level)
        self.pause_menu.add.button('Quit to Menu', self.quit_to_menu)
    
    def create_game_over_menu(self):
        """Create the game over menu"""
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.widget_font_size = 32
        
        self.game_over_menu = pygame_menu.Menu(
            'Game Over', 
            WIDTH//2, HEIGHT//2,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True
        )
        
        self.game_over_menu.add.button('Retry Level', self.restart_level)
        self.game_over_menu.add.button('Quit to Menu', self.quit_to_menu)
    
    def create_victory_menu(self):
        """Create the victory menu"""
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.widget_font_size = 32
        
        self.victory_menu = pygame_menu.Menu(
            'Level Complete!', 
            WIDTH//2, HEIGHT//2,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True
        )
        
        self.victory_time_label = self.victory_menu.add.label('Your Time: 00:00.000')
        self.victory_best_label = self.victory_menu.add.label('Best Time: 00:00.000')
        self.victory_menu.add.button('Next Level', self.next_level)
        self.victory_menu.add.button('Retry Level', self.restart_level)
        self.victory_menu.add.button('Quit to Menu', self.quit_to_menu)
    
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
    
    def reset_timer(self):
        """Reset the game timer"""
        self.timer_start = pygame.time.get_ticks()
        self.is_timer_running = True
        self.paused_time = 0
        self.current_time = 0
    
    def get_elapsed_time(self):
        """Get the elapsed time in milliseconds"""
        if self.is_timer_running:
            return pygame.time.get_ticks() - self.timer_start - self.paused_time
        return self.current_time
    
    def format_time(self, time_ms):
        """Format time in milliseconds to MM:SS.ms format"""
        minutes = int(time_ms / 60000)
        seconds = int((time_ms % 60000) / 1000)
        milliseconds = time_ms % 1000
        return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    
    def update_victory_menu(self, current_time, best_time):
        """Update the victory menu with current and best times"""
        self.victory_time_label.set_title(f'Your Time: {self.format_time(current_time)}')
        
        if best_time:
            self.victory_best_label.set_title(f'Best Time: {self.format_time(best_time)}')
        else:
            self.victory_best_label.set_title('Best Time: N/A')
    
    def draw_hud(self, player_lives, current_level):
        """Draw the in-game HUD"""
        # Draw timer
        time_text = self.font_medium.render(
            f"Time: {self.format_time(self.get_elapsed_time())}", 
            True, WHITE
        )
        self.screen.blit(time_text, (20, 20))
        
        # Draw lives
        lives_text = self.font_medium.render(f"Lives: {player_lives}", True, WHITE)
        self.screen.blit(lives_text, (20, 60))
        
        # Draw current level
        level_text = self.font_medium.render(f"Level: {current_level}", True, WHITE)
        self.screen.blit(level_text, (WIDTH - level_text.get_width() - 20, 20))
    
    def draw_countdown(self, count):
        """Draw countdown before level starts"""
        count_text = self.font_large.render(str(count), True, WHITE)
        count_rect = count_text.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.screen.blit(count_text, count_rect)
