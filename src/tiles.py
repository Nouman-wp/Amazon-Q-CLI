"""
Tiles module for SpeedRunner X.
Handles game tiles, platforms, and hazards.
"""
import pygame
import math
from src.settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, tile_type='normal'):
        super().__init__(groups)
        
        # Create a more visually appealing tile
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Different tile types
        if tile_type == 'normal':
            # Create a brick-like pattern
            BRICK_COLOR = (139, 69, 19)  # Brown
            MORTAR_COLOR = (210, 180, 140)  # Tan
            
            # Fill with base color
            self.image.fill(BRICK_COLOR)
            
            # Add brick pattern
            brick_size = size // 4
            for y in range(0, size, brick_size):
                offset = brick_size // 2 if y % (brick_size * 2) == 0 else 0
                for x in range(offset, size, brick_size * 2):
                    pygame.draw.rect(self.image, MORTAR_COLOR, 
                                    (x, y, brick_size, brick_size), 1)
        
        elif tile_type == 'grass':
            # Create a grass-topped dirt block
            DIRT_COLOR = (139, 69, 19)  # Brown
            GRASS_COLOR = (34, 139, 34)  # Green
            
            # Fill with dirt color
            self.image.fill(DIRT_COLOR)
            
            # Add grass on top
            pygame.draw.rect(self.image, GRASS_COLOR, (0, 0, size, size // 4))
            
            # Add some texture
            for i in range(10):
                x = pygame.time.get_ticks() % size
                y = pygame.time.get_ticks() % (size // 4)
                pygame.draw.rect(self.image, (45, 160, 45), (x, y, 2, 2))
                
        elif tile_type == 'dirt':
            # Create a dirt block
            DIRT_COLOR = (139, 69, 19)  # Brown
            DARK_DIRT = (101, 67, 33)  # Darker brown
            
            # Fill with dirt color
            self.image.fill(DIRT_COLOR)
            
            # Add some texture/variation
            for i in range(5):
                x = (pygame.time.get_ticks() + i * 50) % size
                y = (pygame.time.get_ticks() + i * 30) % size
                width = 4 + i % 4
                height = 4 + i % 3
                pygame.draw.rect(self.image, DARK_DIRT, (x, y, width, height))
                
        elif tile_type == 'invisible':
            # Create an invisible collision tile
            self.image.fill((0, 0, 0, 0))  # Completely transparent
        
        self.rect = self.image.get_rect(topleft=pos)


class Hazard(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, hazard_type='spike'):
        super().__init__(groups)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.hazard_type = hazard_type
        self.animation_frame = 0
        self.animation_speed = 0.2
        
        # Different hazard types
        if hazard_type == 'spike':
            # Create a spike hazard
            SPIKE_COLOR = (200, 0, 0)  # Bright red
            METAL_COLOR = (150, 150, 150)  # Gray
            
            # Draw the base
            pygame.draw.rect(self.image, METAL_COLOR, (0, size * 3//4, size, size//4))
            
            # Draw the spikes
            spike_count = 3
            spike_width = size // spike_count
            for i in range(spike_count):
                x1 = i * spike_width
                x2 = (i + 0.5) * spike_width
                x3 = (i + 1) * spike_width
                y1 = size * 3//4
                y2 = size // 4
                
                pygame.draw.polygon(self.image, SPIKE_COLOR, [(x1, y1), (x2, y2), (x3, y1)])
                # Add highlight for 3D effect
                pygame.draw.line(self.image, (255, 100, 100), (x1+2, y1-2), (x2, y2+2), 1)
        
        elif hazard_type == 'lava':
            # Create a lava hazard - store base image for animation
            self.lava_base = pygame.Surface((size, size), pygame.SRCALPHA)
            self.lava_frames = []
            
            # Create base lava color
            LAVA_COLOR = (255, 69, 0)  # Orange-red
            LAVA_DARK = (200, 30, 0)   # Darker orange-red
            LAVA_BRIGHT = (255, 200, 0)  # Bright yellow
            
            # Fill base with gradient
            for y in range(size):
                # Make bottom darker
                intensity = 1.0 - (y / size) * 0.5
                color = (
                    int(LAVA_COLOR[0] * intensity),
                    int(LAVA_COLOR[1] * intensity),
                    int(LAVA_COLOR[2] * intensity)
                )
                pygame.draw.line(self.lava_base, color, (0, y), (size, y))
            
            # Create animation frames
            for frame in range(4):
                frame_surf = self.lava_base.copy()
                
                # Add bubbles and surface details at different positions for each frame
                for i in range(5):
                    # Randomize bubble positions based on frame
                    x = (i * size // 5 + frame * 7) % size
                    y = size - (i % 3) * 8 - frame * 3
                    radius = 2 + (i % 3)
                    
                    # Draw bubble
                    pygame.draw.circle(frame_surf, LAVA_BRIGHT, (x, y), radius)
                    pygame.draw.circle(frame_surf, (255, 255, 200), (x, y-1), radius//2)
                
                # Add surface waves
                for x in range(0, size, 4):
                    wave_height = int(math.sin((x / 10 + frame) % (2 * math.pi)) * 3)
                    pygame.draw.line(frame_surf, LAVA_BRIGHT, 
                                    (x, size//4 + wave_height), 
                                    (x+3, size//4 + wave_height), 2)
                
                self.lava_frames.append(frame_surf)
            
            # Set initial frame
            self.image = self.lava_frames[0]
        
        self.rect = self.image.get_rect(topleft=pos)
    
    def update(self):
        """Animate hazards like lava"""
        if self.hazard_type == 'lava':
            # Animate lava
            self.animation_frame += self.animation_speed
            if self.animation_frame >= len(self.lava_frames):
                self.animation_frame = 0
            
            self.image = self.lava_frames[int(self.animation_frame)]


class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, move_distance, speed, direction='horizontal'):
        super().__init__(groups)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Create a nice looking platform
        PLATFORM_COLOR = (100, 100, 255)  # Light blue
        HIGHLIGHT_COLOR = (150, 150, 255)  # Lighter blue
        
        # Fill with base color
        self.image.fill(PLATFORM_COLOR)
        
        # Add some details
        pygame.draw.rect(self.image, HIGHLIGHT_COLOR, (2, 2, size-4, size//3))
        pygame.draw.rect(self.image, HIGHLIGHT_COLOR, (2, 2, size//3, size-4))
        
        # Add some mechanical details to suggest it's a moving platform
        for i in range(3):
            pygame.draw.circle(self.image, (50, 50, 50), (size//4 + i*size//4, size//2), 2)
        
        self.rect = self.image.get_rect(topleft=pos)
        
        self.direction = direction
        self.speed = speed
        self.move_distance = move_distance
        self.start_pos = pygame.math.Vector2(pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.moving_forward = True
        
    def update(self):
        # Move the platform back and forth
        if self.direction == 'horizontal':
            if self.moving_forward:
                self.pos.x += self.speed
                if self.pos.x >= self.start_pos.x + self.move_distance:
                    self.moving_forward = False
            else:
                self.pos.x -= self.speed
                if self.pos.x <= self.start_pos.x:
                    self.moving_forward = True
        else:  # vertical
            if self.moving_forward:
                self.pos.y += self.speed
                if self.pos.y >= self.start_pos.y + self.move_distance:
                    self.moving_forward = False
            else:
                self.pos.y -= self.speed
                if self.pos.y <= self.start_pos.y:
                    self.moving_forward = True
        
        # Update the rect position
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))


class FinishFlag(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface((size, size * 2), pygame.SRCALPHA)
        
        # Create a flag pole and flag
        POLE_COLOR = (150, 150, 150)  # Gray
        FLAG_COLOR = (255, 215, 0)    # Gold
        
        # Draw the pole
        pygame.draw.rect(self.image, POLE_COLOR, (size//2 - 2, 0, 4, size * 2))
        
        # Draw the flag
        flag_points = [
            (size//2, size//4),
            (size - 4, size//2),
            (size//2, size * 3//4)
        ]
        pygame.draw.polygon(self.image, FLAG_COLOR, flag_points)
        
        # Add a base
        pygame.draw.rect(self.image, POLE_COLOR, (size//4, size * 2 - 8, size//2, 8))
        
        # Add some details to the flag
        pygame.draw.circle(self.image, (255, 255, 255), (size * 3//4, size//2), size//8)
        
        self.rect = self.image.get_rect(bottomleft=pos)
        
        # Animation variables
        self.frame = 0
        self.animation_speed = 0.1
        self.wave_amplitude = 2
        
    def update(self):
        # Make the flag wave
        self.frame += self.animation_speed
        wave = math.sin(self.frame) * self.wave_amplitude
        
        # We could update the flag's appearance here to make it wave
        # For now, we'll just move it slightly
        self.rect.y = self.rect.y + round(wave)
