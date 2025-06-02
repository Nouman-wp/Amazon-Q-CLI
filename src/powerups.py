"""
Powerups module for SpeedRunner X.
Handles power-up items and their effects.
"""
import pygame
import math
from src.settings import *

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, powerup_type='speed'):
        super().__init__(groups)
        self.image = pygame.Surface((size, size))
        self.type = powerup_type
        
        # Different power-up types
        if powerup_type == 'speed':
            self.image.fill(GREEN)
            # Draw a lightning bolt or arrow
            pygame.draw.polygon(self.image, WHITE, [(size/2, 0), (size, size/2), (size/2, size/2), (size, size)])
        elif powerup_type == 'slow_time':
            self.image.fill(PURPLE)
            # Draw a clock
            pygame.draw.circle(self.image, WHITE, (size/2, size/2), size/3)
            pygame.draw.line(self.image, BLACK, (size/2, size/2), (size/2, size/4), 2)
            pygame.draw.line(self.image, BLACK, (size/2, size/2), (size*3/4, size/2), 2)
        elif powerup_type == 'invincibility':
            self.image.fill(YELLOW)
            # Draw a star
            points = []
            for i in range(5):
                angle = i * 2 * 3.14159 / 5 - 3.14159 / 2
                points.append((size/2 + size/3 * math.cos(angle), size/2 + size/3 * math.sin(angle)))
                angle += 3.14159 / 5
                points.append((size/2 + size/6 * math.cos(angle), size/2 + size/6 * math.sin(angle)))
            pygame.draw.polygon(self.image, WHITE, points)
        
        self.rect = self.image.get_rect(topleft=pos)
        
        # Animation
        self.float_y = float(pos[1])
        self.float_speed = 0.5
        self.float_direction = 1
        self.float_distance = 5
    
    def update(self):
        # Simple floating animation
        self.float_y += self.float_speed * self.float_direction
        if abs(self.float_y - self.rect.y) >= self.float_distance:
            self.float_direction *= -1
        
        self.rect.y = int(self.float_y)
