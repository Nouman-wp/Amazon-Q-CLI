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
        
        # Create ghost animations
        self.load_ghost_sprites()
        
        # Animation variables
        self.frame_index = 0
        self.animation_speed = 0.15
        self.current_animation = self.idle_frames_right
        
        # Initial image and rect
        self.image = self.current_animation[self.frame_index]
        self.rect = self.image.get_rect()
        
        self.position_data = []
        self.current_index = 0
        self.active = False
        self.facing_right = True
        self.is_running = False
        self.is_jumping = False
        self.is_falling = False
    
    def load_ghost_sprites(self):
        """Load ghost sprite images - similar to player but semi-transparent"""
        # Create base images for different states
        self.idle_frames_right = []
        self.idle_frames_left = []
        self.run_frames_right = []
        self.run_frames_left = []
        self.jump_frame_right = None
        self.jump_frame_left = None
        self.fall_frame_right = None
        self.fall_frame_left = None
        
        # Colors for our ghost character (semi-transparent)
        RED = (255, 0, 0, 128)       # Cap/hat
        BLUE = (0, 0, 255, 128)      # Overalls
        SKIN = (255, 200, 150, 128)  # Skin tone
        BROWN = (139, 69, 19, 128)   # Shoes
        
        # Create idle frames (2 frames)
        for i in range(2):
            # Create a surface for the character
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            
            # Draw character (simple Mario-like)
            # Hat
            pygame.draw.rect(surf, RED, (4, 4, 24, 8))
            # Head
            pygame.draw.rect(surf, SKIN, (8, 8, 16, 8))
            # Body
            pygame.draw.rect(surf, BLUE, (8, 16, 16, 12))
            # Arms (slightly different in second frame)
            if i == 0:
                pygame.draw.rect(surf, SKIN, (4, 16, 4, 8))
                pygame.draw.rect(surf, SKIN, (24, 16, 4, 8))
            else:
                pygame.draw.rect(surf, SKIN, (4, 18, 4, 8))
                pygame.draw.rect(surf, SKIN, (24, 18, 4, 8))
            # Legs
            pygame.draw.rect(surf, BLUE, (8, 28, 6, 4))
            pygame.draw.rect(surf, BLUE, (18, 28, 6, 4))
            # Shoes
            pygame.draw.rect(surf, BROWN, (6, 30, 8, 2))
            pygame.draw.rect(surf, BROWN, (18, 30, 8, 2))
            
            # Add to idle frames
            self.idle_frames_right.append(surf)
            # Create left-facing version
            self.idle_frames_left.append(pygame.transform.flip(surf, True, False))
        
        # Create run frames (4 frames)
        for i in range(4):
            # Create a surface for the character
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            
            # Draw character (simple Mario-like)
            # Hat
            pygame.draw.rect(surf, RED, (4, 4, 24, 8))
            # Head
            pygame.draw.rect(surf, SKIN, (8, 8, 16, 8))
            # Body
            pygame.draw.rect(surf, BLUE, (8, 16, 16, 12))
            
            # Different arm and leg positions for running animation
            if i == 0:  # Frame 1
                pygame.draw.rect(surf, SKIN, (4, 16, 4, 8))
                pygame.draw.rect(surf, SKIN, (24, 16, 4, 8))
                pygame.draw.rect(surf, BLUE, (8, 28, 6, 4))
                pygame.draw.rect(surf, BLUE, (18, 28, 6, 4))
                pygame.draw.rect(surf, BROWN, (6, 30, 8, 2))
                pygame.draw.rect(surf, BROWN, (18, 30, 8, 2))
            elif i == 1:  # Frame 2
                pygame.draw.rect(surf, SKIN, (4, 14, 4, 8))
                pygame.draw.rect(surf, SKIN, (24, 18, 4, 8))
                pygame.draw.rect(surf, BLUE, (6, 26, 6, 6))
                pygame.draw.rect(surf, BLUE, (20, 28, 6, 4))
                pygame.draw.rect(surf, BROWN, (4, 30, 8, 2))
                pygame.draw.rect(surf, BROWN, (20, 30, 8, 2))
            elif i == 2:  # Frame 3
                pygame.draw.rect(surf, SKIN, (4, 16, 4, 8))
                pygame.draw.rect(surf, SKIN, (24, 16, 4, 8))
                pygame.draw.rect(surf, BLUE, (10, 28, 6, 4))
                pygame.draw.rect(surf, BLUE, (16, 28, 6, 4))
                pygame.draw.rect(surf, BROWN, (8, 30, 8, 2))
                pygame.draw.rect(surf, BROWN, (16, 30, 8, 2))
            else:  # Frame 4
                pygame.draw.rect(surf, SKIN, (4, 18, 4, 8))
                pygame.draw.rect(surf, SKIN, (24, 14, 4, 8))
                pygame.draw.rect(surf, BLUE, (6, 28, 6, 4))
                pygame.draw.rect(surf, BLUE, (20, 26, 6, 6))
                pygame.draw.rect(surf, BROWN, (4, 30, 8, 2))
                pygame.draw.rect(surf, BROWN, (20, 30, 8, 2))
            
            # Add to run frames
            self.run_frames_right.append(surf)
            # Create left-facing version
            self.run_frames_left.append(pygame.transform.flip(surf, True, False))
        
        # Create jump frame
        jump_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # Hat
        pygame.draw.rect(jump_surf, RED, (4, 2, 24, 8))
        # Head
        pygame.draw.rect(jump_surf, SKIN, (8, 6, 16, 8))
        # Body
        pygame.draw.rect(jump_surf, BLUE, (8, 14, 16, 12))
        # Arms up
        pygame.draw.rect(jump_surf, SKIN, (4, 10, 4, 8))
        pygame.draw.rect(jump_surf, SKIN, (24, 10, 4, 8))
        # Legs bent
        pygame.draw.rect(jump_surf, BLUE, (8, 26, 6, 6))
        pygame.draw.rect(jump_surf, BLUE, (18, 26, 6, 6))
        # Shoes
        pygame.draw.rect(jump_surf, BROWN, (6, 30, 8, 2))
        pygame.draw.rect(jump_surf, BROWN, (18, 30, 8, 2))
        
        self.jump_frame_right = jump_surf
        self.jump_frame_left = pygame.transform.flip(jump_surf, True, False)
        
        # Create fall frame
        fall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # Hat
        pygame.draw.rect(fall_surf, RED, (4, 4, 24, 8))
        # Head
        pygame.draw.rect(fall_surf, SKIN, (8, 8, 16, 8))
        # Body
        pygame.draw.rect(fall_surf, BLUE, (8, 16, 16, 12))
        # Arms out
        pygame.draw.rect(fall_surf, SKIN, (2, 16, 6, 4))
        pygame.draw.rect(fall_surf, SKIN, (24, 16, 6, 4))
        # Legs spread
        pygame.draw.rect(fall_surf, BLUE, (6, 28, 6, 4))
        pygame.draw.rect(fall_surf, BLUE, (20, 28, 6, 4))
        # Shoes
        pygame.draw.rect(fall_surf, BROWN, (4, 30, 8, 2))
        pygame.draw.rect(fall_surf, BROWN, (18, 30, 8, 2))
        
        self.fall_frame_right = fall_surf
        self.fall_frame_left = pygame.transform.flip(fall_surf, True, False)
    
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
            
            # Update facing direction and animation states
            self.facing_right = pos_data.get('facing_right', True)
            self.is_running = pos_data.get('is_running', False)
            self.is_jumping = pos_data.get('is_jumping', False)
            self.is_falling = pos_data.get('is_falling', False)
            
            # Update animation
            self.animate()
    
    def animate(self):
        """Update ghost animation based on state"""
        # Determine which animation to use
        if self.is_jumping:
            if self.facing_right:
                self.image = self.jump_frame_right
            else:
                self.image = self.jump_frame_left
        elif self.is_falling:
            if self.facing_right:
                self.image = self.fall_frame_right
            else:
                self.image = self.fall_frame_left
        elif self.is_running:
            # Update animation frame
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.run_frames_right):
                self.frame_index = 0
                
            # Set correct animation based on direction
            if self.facing_right:
                self.image = self.run_frames_right[int(self.frame_index)]
            else:
                self.image = self.run_frames_left[int(self.frame_index)]
        else:  # Idle
            # Update animation frame
            self.frame_index += self.animation_speed * 0.5  # Slower for idle
            if self.frame_index >= len(self.idle_frames_right):
                self.frame_index = 0
                
            # Set correct animation based on direction
            if self.facing_right:
                self.image = self.idle_frames_right[int(self.frame_index)]
            else:
                self.image = self.idle_frames_left[int(self.frame_index)]
