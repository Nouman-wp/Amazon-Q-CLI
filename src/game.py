"""
Game module for SpeedRunner X.
Main game class that manages game states and flow.
"""
import pygame
import sys
import os
import math
from src.settings import *
from src.level import Level
from src.ui import UI
from src.leaderboard import Leaderboard
from src.ghost import Ghost
from src.menu_effects import MenuEffects

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Create the game window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = STATE_MENU
        self.current_level = 1
        self.countdown = 3
        self.countdown_timer = 0
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(LEADERBOARD_PATH), exist_ok=True)
        os.makedirs(GHOST_RUNS_PATH, exist_ok=True)
        os.makedirs(MAPS_PATH, exist_ok=True)
        
        # Create UI
        self.ui = UI(self.screen)
        self.setup_ui_callbacks()
        
        # Create menu effects
        self.menu_effects = MenuEffects(self.screen)
        
        # Create leaderboard
        self.leaderboard = Leaderboard()
        
        # Create level
        self.level = None
        self.load_level(f"level{self.current_level}")
    
    def setup_ui_callbacks(self):
        """Set up UI menu callbacks"""
        # Main menu callbacks
        self.ui.start_game = self.start_game
        self.ui.show_leaderboard = self.show_leaderboard
        
        # Pause menu callbacks
        self.ui.resume_game = self.resume_game
        self.ui.restart_level = self.restart_level
        self.ui.quit_to_menu = self.quit_to_menu
        
        # Victory menu callbacks
        self.ui.next_level = self.next_level
    
    def load_level(self, level_name):
        """Load a level"""
        self.level = Level(level_name, self.screen)
        # Pass UI reference to level for powerup notifications
        self.level.ui = self.ui
    
    def start_game(self):
        """Start the game"""
        print("Starting game from Game.start_game()")
        self.state = STATE_PLAYING
        self.countdown = 3
        self.countdown_timer = pygame.time.get_ticks()
        self.level.reset()
        
        # Ensure the level is properly initialized
        self.level.active = False  # Will be set to True after countdown
        self.level.completed = False
        
        # Reset UI timer
        self.ui.reset_timer()
    
    def show_leaderboard(self):
        """Show the leaderboard screen"""
        self.state = STATE_LEADERBOARD
    
    def resume_game(self):
        """Resume the game from pause"""
        self.state = STATE_PLAYING
        self.ui.resume_timer()
    
    def restart_level(self):
        """Restart the current level"""
        print("Restarting level...")
        self.level.reset()
        self.state = STATE_PLAYING
        self.countdown = 3
        self.countdown_timer = pygame.time.get_ticks()
        
        # Reset UI timer
        self.ui.reset_timer()
        
        # Ensure player lives are reset
        if self.level and self.level.player:
            self.level.player.lives = PLAYER_START_LIVES
            print(f"Player lives reset to {self.level.player.lives}")
    
    def quit_to_menu(self):
        """Return to the main menu"""
        print("Quitting to main menu...")
        self.state = STATE_MENU
        
        # Force reload the level to ensure clean state
        self.load_level(f"level{self.current_level}")
    
    def next_level(self):
        """Go to the next level"""
        print("Going to next level")
        self.current_level += 1
        if self.current_level > LEVEL_COUNT:
            self.current_level = 1  # Loop back to first level
            print("Looping back to first level")
        
        # Force reload the level
        self.load_level(f"level{self.current_level}")
        self.state = STATE_PLAYING
        self.countdown = 3
        self.countdown_timer = pygame.time.get_ticks()
        
        # Reset UI timer
        self.ui.reset_timer()
    
    def handle_events(self):
        """Handle pygame events"""
        # Don't get events here for the menu state, as we handle them in render()
        if self.state != STATE_MENU and self.state != STATE_VICTORY and self.state != STATE_GAME_OVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.state == STATE_PLAYING:
                        self.state = STATE_PAUSED
                        self.ui.pause_timer()
                    elif event.key == pygame.K_r and self.state == STATE_PLAYING:
                        self.restart_level()
    
    def update(self):
        """Update game state"""
        if self.state == STATE_PLAYING:
            # Handle countdown
            if self.countdown > 0:
                current_time = pygame.time.get_ticks()
                if current_time - self.countdown_timer > 1000:
                    self.countdown -= 1
                    self.countdown_timer = current_time
                    print(f"Countdown: {self.countdown}")
                    
                    if self.countdown == 0:
                        # Start level and timer
                        print("Countdown finished, starting level")
                        self.level.start()
                        self.ui.start_timer()
            else:
                # Update level
                elapsed_time = self.ui.get_elapsed_time()
                self.level.update(elapsed_time)
                
                # Check if level is completed
                if self.level.completed:
                    # Save ghost data if it's a new record
                    final_time = self.ui.get_elapsed_time()
                    level_name = f"level{self.current_level}"
                    
                    try:
                        if self.leaderboard.is_new_record(level_name, final_time):
                            ghost_data = self.level.get_player_position_history()
                            self.level.ghost.save_ghost_data(level_name, ghost_data)
                        
                        # Add time to leaderboard
                        self.leaderboard.add_time(level_name, final_time)
                        
                        # Show victory menu
                        best_time = self.leaderboard.get_best_time(level_name)
                        self.ui.update_victory_menu(final_time, best_time)
                        self.state = STATE_VICTORY
                    except Exception as e:
                        print(f"Error handling level completion: {e}")
                        # Fallback to just showing victory menu
                        self.ui.update_victory_menu(final_time, None)
                        self.state = STATE_VICTORY
                
                # Check if player is dead
                if self.level.player.lives <= 0:
                    self.state = STATE_GAME_OVER
    
    def render(self):
        """Render the game"""
        # Clear the screen first
        self.screen.fill(BLACK)
        
        if self.state == STATE_MENU:
            # Draw animated menu background
            self.menu_effects.draw_main_menu_effects()
            
            # Handle menu events
            events = pygame.event.get()
            
            # Check for quit event
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Start the game directly when Enter is pressed on the main menu
                        print("Enter key pressed on main menu, starting game...")
                        self.start_game()
                        return
            
            # Update and draw the menu
            self.ui.main_menu.update(events)
            self.ui.main_menu.draw(self.screen)
        
        elif self.state == STATE_PLAYING:
            # Draw level
            self.level.draw()
            
            # Draw HUD
            self.ui.draw_hud(self.level.player.lives, self.current_level)
            
            # Draw countdown if active
            if self.countdown > 0:
                self.ui.draw_countdown(self.countdown)
        
        elif self.state == STATE_PAUSED:
            # Draw level in background
            self.level.draw()
            
            # Handle pause menu events
            events = pygame.event.get()
            
            # Check for quit event
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Update and draw the pause menu
            self.ui.pause_menu.update(events)
            self.ui.pause_menu.draw(self.screen)
            
            # Handle menu selection
            for event in events:
                if event.type == pygame.KEYDOWN:
                    print(f"Key pressed in pause menu: {pygame.key.name(event.key)}")
                    if event.key == pygame.K_RETURN:
                        selected_widget = self.ui.pause_menu.get_selected_widget()
                        if selected_widget:
                            title = selected_widget.get_title()
                            print(f"Selected pause menu item: {title}")
                            
                            if title == 'RESUME':
                                self.resume_game()
                            elif title == 'RESTART LEVEL':
                                self.restart_level()
                            elif title == 'QUIT TO MENU':
                                self.quit_to_menu()
                    
                    # Also handle arrow keys for menu navigation
                    elif event.key == pygame.K_UP:
                        print("UP key pressed in pause menu")
                        # Move selection up (previous widget)
                        self.ui.pause_menu.update([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)])
                    elif event.key == pygame.K_DOWN:
                        print("DOWN key pressed in pause menu")
                        # Move selection down (next widget)
                        self.ui.pause_menu.update([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)])
        
        elif self.state == STATE_GAME_OVER:
            # Fill with dark background
            self.screen.fill((20, 20, 20))
            
            # Handle game over menu events
            events = pygame.event.get()
            
            # Check for quit event
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Direct key handling for game over menu
                    if event.key == pygame.K_r:
                        print("R key pressed in game over menu - restarting level")
                        self.restart_level()
                        return
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        print("ESC/Q key pressed in game over menu - quitting to menu")
                        self.quit_to_menu()
                        return
                    elif event.key == pygame.K_RETURN:
                        print("ENTER key pressed in game over menu - restarting level")
                        self.restart_level()
                        return
            
            # Update and draw the game over menu
            self.ui.game_over_menu.update(events)
            self.ui.game_over_menu.draw(self.screen)
            
            # Draw additional instructions
            instructions_text = self.ui.font_small.render("Press R to restart or ESC to quit to menu", True, WHITE)
            self.screen.blit(instructions_text, (WIDTH/2 - instructions_text.get_width()/2, HEIGHT - 50))
        
        elif self.state == STATE_VICTORY:
            # Fill with victory background
            self.screen.fill((20, 50, 20))
            
            # Handle victory menu events
            events = pygame.event.get()
            
            # Check for quit event
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Direct key handling for victory menu
                    if event.key == pygame.K_n:
                        print("N key pressed in victory menu - next level")
                        self.next_level()
                        return
                    elif event.key == pygame.K_r:
                        print("R key pressed in victory menu - restarting level")
                        self.restart_level()
                        return
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        print("ESC/Q key pressed in victory menu - quitting to menu")
                        self.quit_to_menu()
                        return
                    elif event.key == pygame.K_RETURN:
                        # Default action for Enter key is to go to next level
                        print("ENTER key pressed in victory menu - next level")
                        self.next_level()
                        return
            
            # Update and draw the victory menu
            self.ui.victory_menu.update(events)
            self.ui.victory_menu.draw(self.screen)
            
            # Draw additional instructions
            instructions_text = self.ui.font_small.render("Press N for next level, R to restart, or ESC to quit", True, WHITE)
            self.screen.blit(instructions_text, (WIDTH/2 - instructions_text.get_width()/2, HEIGHT - 50))
        
        elif self.state == STATE_LEADERBOARD:
            # Draw leaderboard
            self.screen.fill(BLACK)
            self.leaderboard.render(self.screen)
            
            # Draw back button
            back_text = self.ui.font_medium.render("Press ESC to return to menu", True, WHITE)
            self.screen.blit(back_text, (WIDTH/2 - back_text.get_width()/2, HEIGHT - 50))
            
            # Handle leaderboard events
            events = pygame.event.get()
            
            # Check for quit event
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = STATE_MENU
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while True:
            # Handle events based on game state
            self.handle_events()
            
            # Update game logic
            self.update()
            
            # Render everything
            self.render()
            
            # Debug info - print current state
            if self.state == STATE_MENU:
                state_name = "MENU"
            elif self.state == STATE_PLAYING:
                state_name = "PLAYING"
            elif self.state == STATE_PAUSED:
                state_name = "PAUSED"
            elif self.state == STATE_GAME_OVER:
                state_name = "GAME_OVER"
            elif self.state == STATE_VICTORY:
                state_name = "VICTORY"
            elif self.state == STATE_LEADERBOARD:
                state_name = "LEADERBOARD"
            
            # Uncomment for debugging
            # print(f"Current state: {state_name}")
            
            # Cap the frame rate
            self.clock.tick(FPS)
