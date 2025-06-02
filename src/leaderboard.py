"""
Leaderboard module for SpeedRunner X.
Handles storing and displaying best times.
"""
import pygame
import json
import os
from src.settings import *

class Leaderboard:
    def __init__(self):
        self.leaderboard_data = {}
        self.load_leaderboard()
    
    def get_best_time(self, level_name):
        """Get the best time for a level"""
        if level_name in self.leaderboard_data and self.leaderboard_data[level_name]:
            # Return the fastest time
            return min(self.leaderboard_data[level_name])
        return None
    
    def is_new_record(self, level_name, time):
        """Check if a time is a new record for the level"""
        best_time = self.get_best_time(level_name)
        return best_time is None or time < best_time
    
    def load_leaderboard(self):
        """Load leaderboard data from file"""
        if os.path.exists(LEADERBOARD_PATH):
            try:
                with open(LEADERBOARD_PATH, 'r') as f:
                    loaded_data = json.load(f)
                    
                    # Convert any old format data (dictionaries) to new format (simple times)
                    self.leaderboard_data = {}
                    for level, times in loaded_data.items():
                        self.leaderboard_data[level] = []
                        for time_entry in times:
                            if isinstance(time_entry, dict):
                                # Old format with dictionaries
                                self.leaderboard_data[level].append(time_entry['time'])
                            else:
                                # New format with simple times
                                self.leaderboard_data[level].append(time_entry)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading leaderboard: {e}")
                self.leaderboard_data = {}
        else:
            # Initialize empty leaderboard
            self.leaderboard_data = {}
            for i in range(1, LEVEL_COUNT + 1):
                self.leaderboard_data[f"level{i}"] = []
            self.save_leaderboard()
    
    def save_leaderboard(self):
        """Save leaderboard data to file"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(LEADERBOARD_PATH), exist_ok=True)
        
        try:
            with open(LEADERBOARD_PATH, 'w') as f:
                json.dump(self.leaderboard_data, f)
        except IOError as e:
            print(f"Error saving leaderboard: {e}")
    
    def add_time(self, level_name, time, player_name="Player"):
        """Add a new time to the leaderboard"""
        if level_name not in self.leaderboard_data:
            self.leaderboard_data[level_name] = []
        
        # Add new time (ensure it's a simple number, not a dictionary)
        self.leaderboard_data[level_name].append(time)
        
        # Sort by time (ascending)
        self.leaderboard_data[level_name].sort()
        
        # Keep only top 5
        self.leaderboard_data[level_name] = self.leaderboard_data[level_name][:5]
        
        # Save updated leaderboard
        self.save_leaderboard()
    
    def render(self, screen):
        """Render the leaderboard on screen"""
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)
        
        # Draw title
        title = font_large.render("LEADERBOARD", True, WHITE)
        screen.blit(title, (WIDTH/2 - title.get_width()/2, 50))
        
        y_offset = 120
        
        # Draw each level's times
        for i in range(1, LEVEL_COUNT + 1):
            level_name = f"level{i}"
            
            # Draw level title
            level_title = font_medium.render(f"Level {i}", True, WHITE)
            screen.blit(level_title, (WIDTH/2 - level_title.get_width()/2, y_offset))
            y_offset += 40
            
            # Draw times
            if level_name in self.leaderboard_data and self.leaderboard_data[level_name]:
                for j, time in enumerate(self.leaderboard_data[level_name]):
                    # Format time
                    minutes = time // 60000
                    seconds = (time % 60000) // 1000
                    milliseconds = time % 1000
                    time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
                    
                    # Draw time
                    time_text = font_small.render(f"{j+1}. {time_str}", True, WHITE)
                    screen.blit(time_text, (WIDTH/2 - time_text.get_width()/2, y_offset))
                    y_offset += 30
            else:
                no_times = font_small.render("No times recorded", True, WHITE)
                screen.blit(no_times, (WIDTH/2 - no_times.get_width()/2, y_offset))
                y_offset += 30
            
            y_offset += 20
