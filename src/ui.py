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
    
    def create_modern_theme(self):
        """Create a modern theme for menus"""
        theme = pygame_menu.themes.Theme()
        theme.title_background_color = (20, 20, 60, 230)
        theme.background_color = (30, 30, 50, 200)
        theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        theme.title_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        theme.title_font_size = 60
        theme.widget_font_size = 36
        theme.widget_font_color = (220, 220, 255)
        theme.title_font_color = (255, 255, 255)
        theme.selection_color = (0, 120, 215)
        theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER
        theme.widget_margin = (0, 12)
        theme.widget_padding = 12
        theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
        theme.title_font_shadow = True
        theme.title_font_shadow_color = (0, 0, 0)
        theme.title_font_shadow_offset = 2
        theme.widget_font_shadow = True
        theme.widget_font_shadow_color = (0, 0, 0)
        theme.widget_font_shadow_offset = 2
        theme.cursor_selection_color = (0, 120, 215)
        return theme
    
    def create_main_menu(self):
        """Create the main menu with enhanced visuals"""
        # Create a custom theme with premium styling
        theme = self.create_modern_theme()
        
        # Create the menu with a custom background
        self.main_menu = pygame_menu.Menu(
            'SpeedRunner X', 
            WIDTH, HEIGHT,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add a decorative header with game logo and glow effect
        self.main_menu.add.label('SPEEDRUNNER X', font_size=90, font_color=(255, 215, 0))
        
        self.main_menu.add.label('ULTIMATE CHALLENGE EDITION', font_size=40, font_color=(173, 216, 230))
        
        # Add decorative line with animation effect
        self.main_menu.add.label('★ ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ ★', font_size=30, font_color=(100, 200, 255))
        self.main_menu.add.vertical_margin(30)
        
        # Add menu buttons with premium styling and effects
        start_button = self.main_menu.add.button('START GAME', self.start_game, font_size=45)
        start_button.set_background_color((0, 120, 0))
        start_button.set_border(3, (0, 255, 0))
        
        self.main_menu.add.vertical_margin(15)
        
        leaderboard_button = self.main_menu.add.button('LEADERBOARD', self.show_leaderboard, font_size=45)
        leaderboard_button.set_background_color((0, 0, 150))
        leaderboard_button.set_border(3, (0, 150, 255))
        
        self.main_menu.add.vertical_margin(15)
        
        exit_button = self.main_menu.add.button('EXIT', pygame_menu.events.EXIT, font_size=45)
        exit_button.set_background_color((150, 0, 0))
        exit_button.set_border(3, (255, 0, 0))
        
        self.main_menu.add.vertical_margin(40)
        
        # Add game instructions with premium styling
        self.main_menu.add.label('HOW TO PLAY', font_size=35, font_color=(255, 165, 0))
        
        # Add a decorative separator
        self.main_menu.add.label('✧ ✧ ✧', font_size=24, font_color=(255, 255, 150))
        
        # Add instructions with icons
        self.main_menu.add.label('➤ Arrow Keys / WASD: Move', font_size=28, font_color=(220, 220, 220))
        self.main_menu.add.label('➤ Space: Jump', font_size=28, font_color=(220, 220, 220))
        self.main_menu.add.label('➤ P: Pause Game', font_size=28, font_color=(220, 220, 220))
        self.main_menu.add.label('➤ Jump on enemies to defeat them!', font_size=28, font_color=(220, 220, 220))
        self.main_menu.add.label('➤ Collect powerups for special abilities!', font_size=28, font_color=(220, 220, 220))
        
        # Add version info with premium styling
        self.main_menu.add.vertical_margin(30)
        self.main_menu.add.label('Version 2.0 - Extended Challenge Edition', font_size=18, font_color=(150, 150, 200))
    
    def create_pause_menu(self):
        """Create the pause menu with premium styling"""
        theme = self.create_modern_theme()
        theme.title_font_size = 45
        theme.title_background_color = (0, 0, 100, 200)
        theme.background_color = (0, 0, 50, 180)
        
        self.pause_menu = pygame_menu.Menu(
            'GAME PAUSED', 
            WIDTH//2, HEIGHT//2,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add a decorative pause icon with glow effect
        self.pause_menu.add.label('❚❚', font_size=80, font_color=(255, 255, 0))
        self.pause_menu.add.vertical_margin(25)
        
        # Add a decorative separator
        self.pause_menu.add.label('✧ ✧ ✧', font_size=24, font_color=(255, 255, 150))
        self.pause_menu.add.vertical_margin(15)
        
        # Add buttons with premium styling
        resume_button = self.pause_menu.add.button('RESUME', self.resume_game, font_size=40)
        resume_button.set_background_color((0, 120, 0))
        resume_button.set_border(3, (0, 255, 0))
        
        self.pause_menu.add.vertical_margin(15)
        
        restart_button = self.pause_menu.add.button('RESTART LEVEL', self.restart_level, font_size=40)
        restart_button.set_background_color((0, 0, 150))
        restart_button.set_border(3, (0, 150, 255))
        
        self.pause_menu.add.vertical_margin(15)
        
        quit_button = self.pause_menu.add.button('QUIT TO MENU', self.quit_to_menu, font_size=40)
        quit_button.set_background_color((150, 0, 0))
        quit_button.set_border(3, (255, 0, 0))
        
        # Add keyboard shortcut hints with improved styling
        self.pause_menu.add.vertical_margin(25)
        self.pause_menu.add.label('ESC: Resume   R: Restart', font_size=22, font_color=(200, 200, 255))
    
    def create_game_over_menu(self):
        """Create the game over menu with premium styling"""
        theme = self.create_modern_theme()
        theme.title_font_size = 55
        theme.title_background_color = (150, 0, 0, 220)
        theme.background_color = (50, 0, 0, 180)
        
        self.game_over_menu = pygame_menu.Menu(
            'GAME OVER', 
            WIDTH//2, HEIGHT//2,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add a decorative skull icon with glow effect
        self.game_over_menu.add.label('☠', font_size=100, font_color=(255, 255, 255))
        
        # Add message with dramatic styling
        self.game_over_menu.add.label('You lost all your lives!', font_size=40, font_color=(255, 100, 100))
        
        self.game_over_menu.add.vertical_margin(30)
        
        # Add a decorative separator
        self.game_over_menu.add.label('✧ ✧ ✧', font_size=24, font_color=(255, 100, 100))
        self.game_over_menu.add.vertical_margin(15)
        
        # Add buttons with premium styling
        retry_button = self.game_over_menu.add.button('RETRY LEVEL', self.restart_level, font_size=40)
        retry_button.set_background_color((0, 120, 0))
        retry_button.set_border(3, (0, 255, 0))
        
        self.game_over_menu.add.vertical_margin(15)
        
        quit_button = self.game_over_menu.add.button('QUIT TO MENU', self.quit_to_menu, font_size=40)
        quit_button.set_background_color((150, 0, 0))
        quit_button.set_border(3, (255, 0, 0))
        
        # Add keyboard shortcut hints with improved styling
        self.game_over_menu.add.vertical_margin(25)
        self.game_over_menu.add.label('R: Retry   ESC: Quit to Menu', font_size=22, font_color=(255, 200, 200))
    
    def create_victory_menu(self):
        """Create the victory menu with premium styling"""
        theme = self.create_modern_theme()
        theme.title_font_size = 55
        theme.title_background_color = (0, 120, 0, 220)
        theme.background_color = (20, 60, 20, 180)
        
        self.victory_menu = pygame_menu.Menu(
            'LEVEL COMPLETE!', 
            WIDTH//2, HEIGHT//2,
            theme=theme,
            mouse_enabled=True,
            keyboard_enabled=True,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add a decorative trophy icon with glow effect
        self.victory_menu.add.label('🏆', font_size=100, font_color=(255, 215, 0))
        self.victory_menu.add.vertical_margin(15)
        
        # Add a decorative separator
        self.victory_menu.add.label('★ ★ ★', font_size=24, font_color=(255, 255, 100))
        self.victory_menu.add.vertical_margin(10)
        
        # Add time display with premium styling
        self.victory_time_label = self.victory_menu.add.label(
            'Your Time: 00:00.000', font_size=40, font_color=(255, 255, 100))
        
        self.victory_best_label = self.victory_menu.add.label(
            'Best Time: 00:00.000', font_size=40, font_color=(255, 215, 0))
        
        self.victory_menu.add.vertical_margin(25)
        
        # Add buttons with premium styling
        next_button = self.victory_menu.add.button('NEXT LEVEL', self.next_level, font_size=40)
        next_button.set_background_color((0, 120, 0))
        next_button.set_border(3, (0, 255, 0))
        
        self.victory_menu.add.vertical_margin(15)
        
        retry_button = self.victory_menu.add.button('RETRY LEVEL', self.restart_level, font_size=40)
        retry_button.set_background_color((0, 0, 150))
        retry_button.set_border(3, (0, 150, 255))
        
        self.victory_menu.add.vertical_margin(15)
        
        quit_button = self.victory_menu.add.button('QUIT TO MENU', self.quit_to_menu, font_size=40)
        quit_button.set_background_color((150, 0, 0))
        quit_button.set_border(3, (255, 0, 0))
        
        # Add keyboard shortcut hints with improved styling
        self.victory_menu.add.vertical_margin(25)
        self.victory_menu.add.label('N: Next Level   R: Retry   ESC: Quit to Menu', 
                                   font_size=22, font_color=(200, 255, 200))
    
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
        elif powerup_type.lower() == "checkpoint reached!":
            self.powerup_message = "CHECKPOINT REACHED!"
        else:
            self.powerup_message = powerup_type.upper() + "!"
            
        self.powerup_display_time = pygame.time.get_ticks()
    
    def draw_hud(self, lives, current_level):
        """Draw the HUD (heads-up display) with premium styling"""
        # Create a semi-transparent HUD background with gradient effect
        hud_height = 70
        hud_surface = pygame.Surface((WIDTH, hud_height), pygame.SRCALPHA)
        
        # Create gradient background for HUD
        for y in range(hud_height):
            alpha = max(180 - y * 2, 50)  # Fade from top to bottom
            pygame.draw.line(hud_surface, (0, 0, 30, alpha), (0, y), (WIDTH, y))
            
        # Add decorative border at the bottom
        pygame.draw.line(hud_surface, (100, 150, 255, 150), (0, hud_height-1), (WIDTH, hud_height-1), 2)
        
        self.screen.blit(hud_surface, (0, 0))
        
        # Draw lives with animated heart icons
        lives_text = self.font_medium.render("LIVES:", True, (220, 220, 255))
        self.screen.blit(lives_text, (20, 15))
        
        heart_time = pygame.time.get_ticks() // 500  # For pulsing effect
        heart_scale = 1.0 + 0.1 * math.sin(heart_time % 2 * math.pi)
        
        for i in range(lives):
            # Draw a heart with pulsing effect
            heart_pos = (lives_text.get_width() + 40 + i * 40, 15)
            self.draw_heart(heart_pos, scale=heart_scale)
        
        # Draw level with a fancy border and glow effect
        level_text = self.font_medium.render(f"LEVEL {current_level}", True, (255, 255, 100))
        level_rect = level_text.get_rect(center=(WIDTH // 2, 30))
        
        # Draw glowing border
        glow_color = (0, 100, 255)
        border_rect = level_rect.inflate(30, 15)
        pygame.draw.rect(self.screen, glow_color, border_rect, border_radius=8)
        pygame.draw.rect(self.screen, (100, 200, 255), border_rect, 2, border_radius=8)
        
        # Add inner border for depth
        inner_rect = border_rect.inflate(-6, -6)
        pygame.draw.rect(self.screen, (0, 50, 100), inner_rect, 1, border_radius=6)
        
        # Draw level text with shadow
        shadow_rect = level_rect.move(2, 2)
        shadow_text = self.font_medium.render(f"LEVEL {current_level}", True, (0, 0, 0))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(level_text, level_rect)
        
        # Draw timer with a premium display
        if self.is_timer_running:
            self.current_time = pygame.time.get_ticks() - self.timer_start - self.paused_time
            timer_text = self.font_medium.render(f"TIME: {self.format_time(self.current_time)}", True, (220, 220, 255))
            timer_rect = timer_text.get_rect(topright=(WIDTH - 20, 15))
            
            # Draw timer background with gradient
            timer_bg_rect = timer_rect.inflate(30, 15)
            timer_surface = pygame.Surface((timer_bg_rect.width, timer_bg_rect.height), pygame.SRCALPHA)
            
            for y in range(timer_bg_rect.height):
                alpha = 150 - y
                pygame.draw.line(timer_surface, (0, 0, 100, max(alpha, 50)), 
                                (0, y), (timer_bg_rect.width, y))
                
            pygame.draw.rect(timer_surface, (0, 0, 0, 0), (0, 0, timer_bg_rect.width, timer_bg_rect.height), 
                            border_radius=8)
            pygame.draw.rect(timer_surface, (100, 150, 255, 200), (0, 0, timer_bg_rect.width, timer_bg_rect.height), 
                            2, border_radius=8)
            
            self.screen.blit(timer_surface, timer_bg_rect)
            
            # Draw timer text with shadow
            shadow_rect = timer_rect.move(2, 2)
            shadow_text = self.font_medium.render(f"TIME: {self.format_time(self.current_time)}", True, (0, 0, 0))
            self.screen.blit(shadow_text, shadow_rect)
            self.screen.blit(timer_text, timer_rect)
            
            # Draw best time if available
            best_time = self.get_best_time(current_level)
            if best_time:
                best_text = self.font_small.render(f"BEST: {self.format_time(best_time)}", True, (255, 255, 100))
                best_rect = best_text.get_rect(topright=(WIDTH - 20, 45))
                
                # Draw shadow
                shadow_rect = best_rect.move(1, 1)
                shadow_text = self.font_small.render(f"BEST: {self.format_time(best_time)}", True, (0, 0, 0))
                self.screen.blit(shadow_text, shadow_rect)
                self.screen.blit(best_text, best_rect)
        
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
            
            # Create a background with glow effect
            text_rect = powerup_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            bg_rect = text_rect.inflate(60, 30)
            
            # Draw multiple layers for glow effect
            for i in range(3):
                glow_surf = pygame.Surface((bg_rect.width + i*10, bg_rect.height + i*10), pygame.SRCALPHA)
                glow_color = (255, 165, 0, max(0, int(alpha * 0.3) - i*30))
                pygame.draw.rect(glow_surf, glow_color, 
                                (0, 0, bg_rect.width + i*10, bg_rect.height + i*10), 
                                border_radius=15)
                self.screen.blit(glow_surf, bg_rect.inflate(i*10, i*10))
            
            # Draw main background
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, int(alpha * 0.7)))
            pygame.draw.rect(bg_surface, (255, 165, 0, int(alpha * 0.9)), 
                            (0, 0, bg_rect.width, bg_rect.height), 2, border_radius=10)
            
            self.screen.blit(bg_surface, bg_rect)
            self.screen.blit(powerup_text, text_rect)
    
    def get_best_time(self, level):
        """Get the best time for the current level"""
        # This is a placeholder - in a real implementation, you would load this from a file
        # For now, just return a fixed value for demonstration
        return 45000  # 45 seconds
    
    def draw_heart(self, pos, scale=1.0):
        """Draw a heart icon for lives with optional scaling for animation"""
        x, y = pos
        size = int(24 * scale)
        
        # Draw a heart shape with gradient and glow
        heart_color = (255, 0, 0)  # Red
        heart_glow = (255, 100, 100)  # Light red
        
        # Draw the two circles for the top of the heart
        pygame.draw.circle(self.screen, heart_glow, (x + size//4, y + size//4), size//4 + 1)
        pygame.draw.circle(self.screen, heart_glow, (x + size - size//4, y + size//4), size//4 + 1)
        
        # Draw the main heart shape
        pygame.draw.circle(self.screen, heart_color, (x + size//4, y + size//4), size//4)
        pygame.draw.circle(self.screen, heart_color, (x + size - size//4, y + size//4), size//4)
        
        # Draw the triangle for the bottom of the heart
        pygame.draw.polygon(self.screen, heart_color, [
            (x, y + size//4),
            (x + size//2, y + size),
            (x + size, y + size//4)
        ])
        
        # Add highlight for 3D effect
        pygame.draw.circle(self.screen, (255, 150, 150), (x + size//4 - 2, y + size//4 - 2), size//8)
    
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
