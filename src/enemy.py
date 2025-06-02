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
        
        # Load enemy sprites based on type
        self.enemy_type = enemy_type
        self.load_enemy_sprites()
        
        # Animation variables
        self.frame_index = 0
        self.animation_speed = 0.15
        
        # Initial image and rect
        self.image = self.frames_right[int(self.frame_index)]
        self.rect = self.image.get_rect(topleft=pos)
        
        # Movement
        self.direction = pygame.math.Vector2(-1, 0)  # Start moving left
        self.speed = ENEMY_SPEED
        self.start_pos = pygame.math.Vector2(pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.facing_right = False
        
    def animate(self):
        """Update enemy animation"""
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames_right):
            self.frame_index = 0
        
        if self.facing_right:
            self.image = self.frames_right[int(self.frame_index)]
        else:
            self.image = self.frames_left[int(self.frame_index)]
    
    def load_enemy_sprites(self):
        """Load enemy sprite images"""
        self.frames_right = []
        self.frames_left = []
        
        if self.enemy_type == 'basic':
            # Create a goomba-like enemy
            BROWN = (139, 69, 19)
            DARK_BROWN = (101, 67, 33)
            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)
            
            # Create 2 animation frames
            for i in range(2):
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                
                # Draw the body
                pygame.draw.ellipse(surf, BROWN, (0, TILE_SIZE//2, TILE_SIZE, TILE_SIZE//2))
                
                # Draw the feet
                foot_offset = 2 if i == 0 else -2
                pygame.draw.rect(surf, DARK_BROWN, (4, TILE_SIZE-6, 8, 6))
                pygame.draw.rect(surf, DARK_BROWN, (TILE_SIZE-12, TILE_SIZE-6, 8, 6))
                
                # Draw the eyes
                pygame.draw.circle(surf, WHITE, (TILE_SIZE//3, TILE_SIZE//2), 4)
                pygame.draw.circle(surf, WHITE, (TILE_SIZE*2//3, TILE_SIZE//2), 4)
                pygame.draw.circle(surf, BLACK, (TILE_SIZE//3, TILE_SIZE//2), 2)
                pygame.draw.circle(surf, BLACK, (TILE_SIZE*2//3, TILE_SIZE//2), 2)
                
                # Add to frames
                self.frames_right.append(surf)
                self.frames_left.append(pygame.transform.flip(surf, True, False))
                
        elif self.enemy_type == 'flying':
            # Create a flying enemy (like a Koopa Paratroopa)
            GREEN = (0, 128, 0)
            YELLOW = (255, 255, 0)
            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)
            
            # Create 2 animation frames
            for i in range(2):
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                
                # Draw the body
                pygame.draw.rect(surf, GREEN, (4, 8, TILE_SIZE-8, TILE_SIZE-16))
                
                # Draw the shell
                pygame.draw.ellipse(surf, YELLOW, (2, 4, TILE_SIZE-4, TILE_SIZE-8))
                
                # Draw the wings
                wing_y = 6 if i == 0 else 10
                pygame.draw.polygon(surf, WHITE, [(0, wing_y), (0, wing_y+12), (8, wing_y+6)])
                pygame.draw.polygon(surf, WHITE, [(TILE_SIZE, wing_y), (TILE_SIZE, wing_y+12), (TILE_SIZE-8, wing_y+6)])
                
                # Draw the eyes
                pygame.draw.circle(surf, WHITE, (TILE_SIZE//3, TILE_SIZE//3), 3)
                pygame.draw.circle(surf, BLACK, (TILE_SIZE//3, TILE_SIZE//3), 1)
                
                # Add to frames
                self.frames_right.append(surf)
                self.frames_left.append(pygame.transform.flip(surf, True, False))
                
        elif self.enemy_type == 'jumping':
            # Create a jumping enemy
            RED = (255, 0, 0)
            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)
            
            # Create 2 animation frames
            for i in range(2):
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                
                # Draw the body
                height = TILE_SIZE-8 if i == 0 else TILE_SIZE-12
                pygame.draw.rect(surf, RED, (4, TILE_SIZE-height, TILE_SIZE-8, height))
                
                # Draw the eyes
                pygame.draw.circle(surf, WHITE, (TILE_SIZE//3, TILE_SIZE//3), 3)
                pygame.draw.circle(surf, WHITE, (TILE_SIZE*2//3, TILE_SIZE//3), 3)
                pygame.draw.circle(surf, BLACK, (TILE_SIZE//3, TILE_SIZE//3), 1)
                pygame.draw.circle(surf, BLACK, (TILE_SIZE*2//3, TILE_SIZE//3), 1)
                
                # Add to frames
                self.frames_right.append(surf)
                self.frames_left.append(pygame.transform.flip(surf, True, False))
        
        else:
            # Default enemy (simple colored box with eyes)
            for i in range(2):
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                surf.fill(RED)
                
                # Draw eyes
                eye_y = TILE_SIZE//3 if i == 0 else TILE_SIZE//3 + 2
                pygame.draw.circle(surf, WHITE, (TILE_SIZE//3, eye_y), 4)
                pygame.draw.circle(surf, WHITE, (TILE_SIZE*2//3, eye_y), 4)
                pygame.draw.circle(surf, BLACK, (TILE_SIZE//3, eye_y), 2)
                pygame.draw.circle(surf, BLACK, (TILE_SIZE*2//3, eye_y), 2)
                
                self.frames_right.append(surf)
                self.frames_left.append(pygame.transform.flip(surf, True, False))
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
        
        # Update facing direction
        if self.direction.x > 0:
            self.facing_right = True
        elif self.direction.x < 0:
            self.facing_right = False
        
        # Update animation
        self.animate()
        
        # Update position
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        
        # Update the rect position
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
