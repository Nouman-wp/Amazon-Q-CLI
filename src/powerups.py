"""
Powerups module for SpeedRunner X.
Handles power-up items and their effects.
"""
import pygame
import math
from src.settings import *

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, powerup_type='speed', collision_sprites=None):
        super().__init__(groups)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.type = powerup_type
        self.duration = 0
        self.collision_sprites = collision_sprites
        
        # Different power-up types
        if powerup_type == 'speed':
            # Set duration for speed boost
            self.duration = SPEED_BOOST_DURATION
            
            # Create a better looking speed powerup
            # Green circle with lightning bolt
            pygame.draw.circle(self.image, GREEN, (size//2, size//2), size//2)
            pygame.draw.circle(self.image, (100, 255, 100), (size//2, size//2), size//2 - 2)
            
            # Draw lightning bolt
            bolt_points = [
                (size//2 - 3, size//4),
                (size//2 + 4, size//2 - 2),
                (size//2 - 2, size//2),
                (size//2 + 5, size*3//4)
            ]
            pygame.draw.polygon(self.image, YELLOW, bolt_points)
            pygame.draw.polygon(self.image, WHITE, bolt_points, 1)
            
        elif powerup_type == 'invincibility':
            # Set duration for invincibility
            self.duration = INVINCIBILITY_DURATION
            
            # Create a better looking invincibility powerup
            # Yellow star
            pygame.draw.circle(self.image, YELLOW, (size//2, size//2), size//2)
            pygame.draw.circle(self.image, (255, 255, 100), (size//2, size//2), size//2 - 2)
            
            # Draw star
            points = []
            for i in range(5):
                # Outer points of the star
                angle = i * 2 * math.pi / 5 - math.pi / 2
                points.append((
                    size//2 + int(size//2 * 0.8 * math.cos(angle)), 
                    size//2 + int(size//2 * 0.8 * math.sin(angle))
                ))
                
                # Inner points of the star
                angle += math.pi / 5
                points.append((
                    size//2 + int(size//2 * 0.3 * math.cos(angle)), 
                    size//2 + int(size//2 * 0.3 * math.sin(angle))
                ))
            
            pygame.draw.polygon(self.image, WHITE, points)
            pygame.draw.polygon(self.image, (255, 200, 0), points, 1)
        
        elif powerup_type == 'extra_life':
            # Create a heart powerup
            pygame.draw.circle(self.image, RED, (size//2, size//2), size//2)
            pygame.draw.circle(self.image, (255, 100, 100), (size//2, size//2), size//2 - 2)
            
            # Draw heart
            heart_points = [
                (size//2, size//4),
                (size//4, size//2),
                (size//2, size*3//4),
                (size*3//4, size//2)
            ]
            pygame.draw.polygon(self.image, WHITE, heart_points)
        
        self.rect = self.image.get_rect(topleft=pos)
        
        # Animation
        self.float_y = float(pos[1])
        self.float_speed = 0.5
        self.float_direction = 1
        self.float_distance = 5
        
        # Pulsing effect
        self.pulse_scale = 1.0
        self.pulse_direction = -0.01
        self.min_scale = 0.8
        self.max_scale = 1.2
        self.original_image = self.image.copy()
        self.original_size = self.image.get_size()
        
        # Physics
        self.gravity = 0.2
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.position = pygame.math.Vector2(pos)
    
    def apply_gravity(self):
        """Apply gravity to the powerup"""
        if not self.on_ground:
            self.velocity.y += self.gravity
            self.position.y += self.velocity.y
            self.rect.y = int(self.position.y)
            
            # Check for collision with ground
            if self.collision_sprites:
                for sprite in self.collision_sprites:
                    if sprite.rect.colliderect(self.rect):
                        if self.velocity.y > 0:  # Moving down
                            self.rect.bottom = sprite.rect.top
                            self.position.y = self.rect.y
                            self.velocity.y = 0
                            self.on_ground = True
                            self.float_y = float(self.rect.y)
                            break
    
    def update(self):
        """Update powerup animation"""
        # Apply gravity if we have collision sprites
        if self.collision_sprites:
            self.apply_gravity()
        
        # Only do floating animation if on ground
        if self.on_ground:
            # Floating animation
            self.float_y += self.float_speed * self.float_direction
            if abs(self.float_y - self.rect.y) >= self.float_distance:
                self.float_direction *= -1
            
            self.rect.y = int(self.float_y)
        
        # Pulsing animation
        self.pulse_scale += self.pulse_direction
        if self.pulse_scale <= self.min_scale or self.pulse_scale >= self.max_scale:
            self.pulse_direction *= -1
        
        # Scale the image for pulsing effect
        new_width = int(self.original_size[0] * self.pulse_scale)
        new_height = int(self.original_size[1] * self.pulse_scale)
        
        if new_width > 0 and new_height > 0:  # Ensure valid size
            scaled_image = pygame.transform.scale(self.original_image, (new_width, new_height))
            
            # Create a new surface and center the scaled image on it
            self.image = pygame.Surface(self.original_size, pygame.SRCALPHA)
            x_offset = (self.original_size[0] - new_width) // 2
            y_offset = (self.original_size[1] - new_height) // 2
            self.image.blit(scaled_image, (x_offset, y_offset))
