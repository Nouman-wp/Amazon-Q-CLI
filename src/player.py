"""
Player module for SpeedRunner X.
Handles player movement, physics, and interactions.
"""
import pygame
import os
import time
from src.settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, groups, collision_sprites):
        super().__init__(groups)
        
        # Load player images
        self.load_player_sprites()
        
        # Animation variables
        self.frame_index = 0
        self.animation_speed = 0.15
        self.current_animation = self.idle_frames_right
        
        # Initial image and rect
        self.image = self.current_animation[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Collision
        self.collision_sprites = collision_sprites
        
        # Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED
        self.base_speed = PLAYER_SPEED  # Store original speed for powerups
        self.gravity = PLAYER_GRAVITY
        self.jump_strength = PLAYER_JUMP_STRENGTH
        self.friction = PLAYER_FRICTION
        self.acceleration = PLAYER_ACCELERATION
        
        # Status
        self.facing_right = True
        self.on_ground = False
        self.is_jumping = False
        self.is_falling = False
        self.is_running = False
        self.lives = PLAYER_START_LIVES
        
        # Powerup effects
        self.speed_boost_active = False
        self.speed_boost_end_time = 0
        self.invincible = False
        self.invincible_end_time = 0
        self.invincible_flash = False
        self.flash_timer = 0
        
        # Position history for ghost replay
        self.position_history = []
        self.last_record_time = 0
    
    def load_player_sprites(self):
        """Load player sprite images"""
        # Create a simple character sprite if we don't have assets
        # This creates a Mario-like character using basic shapes
        
        # Create base images for different states
        self.idle_frames_right = []
        self.idle_frames_left = []
        self.run_frames_right = []
        self.run_frames_left = []
        self.jump_frame_right = None
        self.jump_frame_left = None
        self.fall_frame_right = None
        self.fall_frame_left = None
        
        # Colors for our character
        RED = (255, 0, 0)       # Cap/hat
        BLUE = (0, 0, 255)      # Overalls
        SKIN = (255, 200, 150)  # Skin tone
        BROWN = (139, 69, 19)   # Shoes
        
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
    
    def get_input(self):
        """Get player input"""
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        else:
            self.direction.x = 0
        
        # Jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.jump()
    
    def jump(self):
        if self.on_ground:
            self.direction.y = -self.jump_strength
            # Increase jump height to reach higher platforms
            self.direction.y *= 1.2  # 20% higher jump
    
    def apply_physics(self):
        """Apply physics to player movement"""
        # Apply gravity
        self.direction.y += self.gravity
        if self.direction.y > TERMINAL_VELOCITY:
            self.direction.y = TERMINAL_VELOCITY
        
        # Apply friction
        if self.on_ground and abs(self.direction.x) < 0.1:
            self.direction.x = 0
    
    def handle_collisions(self):
        """Handle collisions with the environment"""
        # Horizontal movement
        self.rect.x += self.direction.x * self.speed
        
        # Check for horizontal collisions
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction.x > 0:  # Moving right
                    self.rect.right = sprite.rect.left
                elif self.direction.x < 0:  # Moving left
                    self.rect.left = sprite.rect.right
        
        # Vertical movement
        self.rect.y += self.direction.y
        
        # Check for vertical collisions
        self.on_ground = False
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:  # Moving down
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:  # Moving up
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
    
    def animate(self):
        """Update player animation based on state"""
        # Store the original image for invincibility effect
        original_image = None
        
        # Determine which animation to use
        if self.direction.y < 0:  # Jumping
            self.is_jumping = True
            self.is_falling = False
            self.is_running = False
            
            if self.facing_right:
                original_image = self.jump_frame_right
            else:
                original_image = self.jump_frame_left
        elif self.direction.y > 1:  # Falling (with a small threshold)
            self.is_jumping = False
            self.is_falling = True
            self.is_running = False
            
            if self.facing_right:
                original_image = self.fall_frame_right
            else:
                original_image = self.fall_frame_left
        elif abs(self.direction.x) > 0.1:  # Running
            self.is_jumping = False
            self.is_falling = False
            self.is_running = True
            
            # Update animation frame
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.run_frames_right):
                self.frame_index = 0
                
            # Set correct animation based on direction
            if self.facing_right:
                original_image = self.run_frames_right[int(self.frame_index)]
            else:
                original_image = self.run_frames_left[int(self.frame_index)]
        else:  # Idle
            self.is_jumping = False
            self.is_falling = False
            self.is_running = False
            
            # Update animation frame
            self.frame_index += self.animation_speed * 0.5  # Slower for idle
            if self.frame_index >= len(self.idle_frames_right):
                self.frame_index = 0
                
            # Set correct animation based on direction
            if self.facing_right:
                original_image = self.idle_frames_right[int(self.frame_index)]
            else:
                original_image = self.idle_frames_left[int(self.frame_index)]
        
        # Apply invincibility effect (flashing)
        if self.invincible and self.invincible_flash:
            # Create a white silhouette for flashing effect
            white_image = original_image.copy()
            white_image.fill((255, 255, 255, 180), None, pygame.BLEND_RGBA_MULT)
            self.image = white_image
        else:
            self.image = original_image
    
    def update(self, elapsed_time=0):
        """Update player state"""
        # Get input
        self.get_input()
        
        # Check powerup timers
        self.update_powerups()
        
        # Apply physics
        self.apply_physics()
        
        # Handle collisions
        self.handle_collisions()
        
        # Update animation
        self.animate()
        
        # Record position for ghost replay (every 50ms)
        if elapsed_time - self.last_record_time > 50:
            self.record_position(elapsed_time)
            self.last_record_time = elapsed_time
    
    def update_powerups(self):
        """Update powerup effects"""
        current_time = pygame.time.get_ticks()
        
        # Check speed boost
        if self.speed_boost_active and current_time >= self.speed_boost_end_time:
            self.speed_boost_active = False
            self.speed = self.base_speed
            print("Speed boost ended")
        
        # Check invincibility
        if self.invincible and current_time >= self.invincible_end_time:
            self.invincible = False
            print("Invincibility ended")
        
        # Flash effect for invincibility
        if self.invincible:
            if current_time - self.flash_timer > 100:  # Flash every 100ms
                self.invincible_flash = not self.invincible_flash
                self.flash_timer = current_time
    
    def activate_speed_boost(self, duration=SPEED_BOOST_DURATION):
        """Activate speed boost powerup"""
        self.base_speed = PLAYER_SPEED  # Store current base speed
        self.speed = self.base_speed * SPEED_BOOST_MULTIPLIER
        self.speed_boost_active = True
        self.speed_boost_end_time = pygame.time.get_ticks() + duration
    
    def activate_invincibility(self, duration=INVINCIBILITY_DURATION):
        """Activate invincibility powerup"""
        self.invincible = True
        self.invincible_end_time = pygame.time.get_ticks() + duration
        self.flash_timer = pygame.time.get_ticks()
    
    def record_position(self, time):
        """Record current position for ghost replay"""
        self.position_history.append({
            'time': time,
            'x': self.rect.x,
            'y': self.rect.y,
            'facing_right': self.facing_right,
            'is_running': self.is_running,
            'is_jumping': self.is_jumping,
            'is_falling': self.is_falling
        })
