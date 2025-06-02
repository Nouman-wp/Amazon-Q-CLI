"""
Ghost module for SpeedRunner X.
Handles ghost replay functionality.
"""
import pygame
import json
import os
from src.settings import *

class Ghost(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        # Create a semi-transparent player sprite
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (*BLUE, 128), (0, 0, TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        
        self.position_data = []
        self.current_index = 0
        self.active = False
        self.facing_right = True
    
    def load_ghost_data(self, level_name):
        """Load ghost data from file for the specified level"""
        ghost_file = os.path.join(GHOST_RUNS_PATH, f"{level_name}_ghost.json")
        
        if os.path.exists(ghost_file):
            try:
                with open(ghost_file, 'r') as f:
                    self.position_data = json.load(f)
                self.active = True
                self.current_index = 0
                return True
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading ghost data: {e}")
                self.active = False
                return False
        else:
            self.active = False
            return False
    
    def save_ghost_data(self, level_name, position_history):
        """Save ghost data to file for the specified level"""
        ghost_file = os.path.join(GHOST_RUNS_PATH, f"{level_name}_ghost.json")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(ghost_file), exist_ok=True)
        
        try:
            with open(ghost_file, 'w') as f:
                json.dump(position_history, f)
            return True
        except IOError as e:
            print(f"Error saving ghost data: {e}")
            return False
    
    def update(self, elapsed_time):
        """Update ghost position based on elapsed time"""
        if not self.active or not self.position_data:
            return
        
        # Find the appropriate position data for the current time
        while (self.current_index < len(self.position_data) - 1 and 
               self.position_data[self.current_index]['time'] < elapsed_time):
            self.current_index += 1
        
        # Set ghost position
        if self.current_index < len(self.position_data):
            pos_data = self.position_data[self.current_index]
            self.rect.x = pos_data['x']
            self.rect.y = pos_data['y']
            
            # Update facing direction
            if 'facing_right' in pos_data:
                self.facing_right = pos_data['facing_right']
                # Could flip the sprite here based on facing direction
                # if self.facing_right:
                #     self.image = self.original_image
                # else:
                #     self.image = pygame.transform.flip(self.original_image, True, False)
