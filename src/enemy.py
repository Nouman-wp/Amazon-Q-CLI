"""
Enemy module for SpeedRunner X.
Handles enemy behavior and interactions.
"""
import pygame
import math
from src.settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, patrol_distance=None, enemy_type='basic'):
        super().__init__(groups)
        self.image = pygame.Surface((size, size))
        self.enemy_type = enemy_type
        
        # Different enemy types
        if enemy_type == 'basic':
            self.image.fill(RED)
        elif enemy_type == 'flying':
            self.image.fill(PURPLE)
        elif enemy_type == 'jumping':
            self.image.fill(YELLOW)
        
        self.rect = self.image.get_rect(topleft=pos)
        
        # Movement
        self.direction = pygame.math.Vector2(-1, 0)  # Start moving left
        self.speed = ENEMY_SPEED
        self.start_pos = pygame.math.Vector2(pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
        # Patrol behavior
        self.patrol_distance = patrol_distance if patrol_distance else size * 4
        self.moving_right = False
        
        # For jumping enemies
        self.gravity = GRAVITY * 0.8  # Slightly less gravity than player
        self.jump_timer = 0
        self.jump_interval = 2000  # ms between jumps
        
        # For flying enemies
        self.fly_amplitude = size  # How high it flies
        self.fly_speed = 0.05  # Speed of flying oscillation
        self.fly_offset = 0
    
    def patrol(self):
        """Basic patrol behavior - move back and forth"""
        if self.moving_right:
            self.pos.x += self.speed
            if self.pos.x >= self.start_pos.x + self.patrol_distance:
                self.moving_right = False
        else:
            self.pos.x -= self.speed
            if self.pos.x <= self.start_pos.x - self.patrol_distance:
                self.moving_right = True
    
    def fly(self):
        """Flying behavior - move in a sine wave pattern"""
        self.patrol()  # Handle horizontal movement
        
        # Add vertical oscillation
        self.fly_offset += self.fly_speed
        self.pos.y = self.start_pos.y + math.sin(self.fly_offset) * self.fly_amplitude
    
    def jump(self):
        """Jumping behavior - jump at intervals"""
        current_time = pygame.time.get_ticks()
        
        # Apply gravity
        self.pos.y += self.direction.y
        self.direction.y += self.gravity
        
        # Check if it's time to jump
        if current_time - self.jump_timer > self.jump_interval and self.direction.y == 0:
            self.direction.y = -10  # Jump strength
            self.jump_timer = current_time
        
        # Handle horizontal movement
        self.patrol()
    
    def update(self, collision_sprites=None):
        if self.enemy_type == 'basic':
            self.patrol()
        elif self.enemy_type == 'flying':
            self.fly()
        elif self.enemy_type == 'jumping':
            self.jump()
            
            # Simple collision for jumping enemies
            if collision_sprites:
                # Vertical collision
                self.rect.y += self.direction.y
                for sprite in collision_sprites:
                    if sprite.rect.colliderect(self.rect):
                        if self.direction.y > 0:  # Moving down
                            self.rect.bottom = sprite.rect.top
                            self.direction.y = 0
                        elif self.direction.y < 0:  # Moving up
                            self.rect.top = sprite.rect.bottom
                            self.direction.y = 0
                
                # Update position after collision check
                self.pos.y = self.rect.y
        
        # Update the rect position
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
