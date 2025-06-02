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
    
    def load_leaderboard(self):
        """Load leaderboard data from file"""
        if os.path.exists(LEADERBOARD_PATH):
            try:
                with open(LEADERBOARD_PATH, 'r') as f:
                    self.leaderboard_data = json.load(f)
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
        
        # Add new time
        self.leaderboard_data[level_name].append({
            'name': player_name,
            'time': time
        })
        
        # Sort by time (ascending)
        self.leaderboard_data[level_name].sort(key=lambda x: x['time'])
        
        # Keep only top 5
        self.leaderboard_data[level_name] = self.leaderboard_data[level_name][:5]
        
        # Save updated leaderboard
        self.save_leaderboard()
    
    def get_best_time(self, level_name):
        """Get the best time for a level"""
        if level_name in self.leaderboard_data and self.leaderboard_data[level_name]:
            return self.leaderboard_data[level_name][0]['time']
        return None
    
    def is_new_record(self, level_name, time):
        """Check if a time is a new record"""
        best_time = self.get_best_time(level_name)
        if best_time is None or time < best_time:
            return True
        return False
    
    def render(self, surface, level_name=None):
        """Render the leaderboard to a surface"""
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)
        
        # Title
        title_text = font_large.render("LEADERBOARD", True, WHITE)
        title_rect = title_text.get_rect(midtop=(WIDTH/2, 50))
        surface.blit(title_text, title_rect)
        
        # If a specific level is selected
        if level_name and level_name in self.leaderboard_data:
            level_text = font_medium.render(f"Level: {level_name}", True, WHITE)
            level_rect = level_text.get_rect(midtop=(WIDTH/2, title_rect.bottom + 20))
            surface.blit(level_text, level_rect)
            
            # Display times for this level
            y_offset = level_rect.bottom + 30
            if not self.leaderboard_data[level_name]:
                no_times_text = font_small.render("No times recorded yet!", True, WHITE)
                no_times_rect = no_times_text.get_rect(midtop=(WIDTH/2, y_offset))
                surface.blit(no_times_text, no_times_rect)
            else:
                for i, entry in enumerate(self.leaderboard_data[level_name]):
                    # Format time as MM:SS.ms
                    minutes = int(entry['time'] / 60000)
                    seconds = int((entry['time'] % 60000) / 1000)
                    milliseconds = entry['time'] % 1000
                    time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
                    
                    rank_text = font_small.render(f"{i+1}.", True, WHITE)
                    name_text = font_small.render(entry['name'], True, WHITE)
                    time_text = font_small.render(time_str, True, WHITE)
                    
                    surface.blit(rank_text, (WIDTH/2 - 150, y_offset))
                    surface.blit(name_text, (WIDTH/2 - 100, y_offset))
                    surface.blit(time_text, (WIDTH/2 + 50, y_offset))
                    
                    y_offset += 30
        else:
            # Display all levels
            y_offset = title_rect.bottom + 30
            for level in sorted(self.leaderboard_data.keys()):
                level_text = font_medium.render(f"Level: {level}", True, WHITE)
                surface.blit(level_text, (WIDTH/2 - 150, y_offset))
                
                best_time = self.get_best_time(level)
                if best_time is not None:
                    # Format time as MM:SS.ms
                    minutes = int(best_time / 60000)
                    seconds = int((best_time % 60000) / 1000)
                    milliseconds = best_time % 1000
                    time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
                    
                    time_text = font_small.render(f"Best: {time_str}", True, WHITE)
                    surface.blit(time_text, (WIDTH/2 + 50, y_offset + 5))
                else:
                    no_time_text = font_small.render("No times recorded", True, WHITE)
                    surface.blit(no_time_text, (WIDTH/2 + 50, y_offset + 5))
                
                y_offset += 50
