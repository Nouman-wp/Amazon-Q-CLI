"""
Player module for SpeedRunner X.
Handles player movement, physics, and interactions.
"""
import pygame
import os
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
        
    def animate(self):
        """Update player animation based on state"""
        # Determine which animation to use
        if self.direction.y < 0:  # Jumping
            self.is_jumping = True
            self.is_falling = False
            self.is_running = False
            if self.facing_right:
                self.image = self.jump_frame_right
            else:
                self.image = self.jump_frame_left
        elif self.direction.y > 1:  # Falling (with some threshold)
            self.is_jumping = False
            self.is_falling = True
            self.is_running = False
            if self.facing_right:
                self.image = self.fall_frame_right
            else:
                self.image = self.fall_frame_left
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
                self.image = self.run_frames_right[int(self.frame_index)]
            else:
                self.image = self.run_frames_left[int(self.frame_index)]
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
                self.image = self.idle_frames_right[int(self.frame_index)]
            else:
                self.image = self.idle_frames_left[int(self.frame_index)]
                
        # On-wall animation (if implemented)
        if self.on_wall:
            if self.facing_right:
                self.image = pygame.transform.flip(self.idle_frames_right[0], True, False)
            else:
                self.image = pygame.transform.flip(self.idle_frames_left[0], True, False)
                
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
        self.on_wall = False
        self.wall_slide_speed = PLAYER_WALL_SLIDE_SPEED
        self.wall_jump_strength = PLAYER_WALL_JUMP_STRENGTH
        
        # Power-up status
        self.has_speed_boost = False
        self.speed_boost_timer = 0
        self.has_slow_time = False
        self.slow_time_timer = 0
        self.is_invincible = False
        self.invincibility_timer = 0
        
        # Position history for ghost replay
        self.position_history = []
        self.start_time = pygame.time.get_ticks()
        
        # Lives
        self.lives = PLAYER_START_LIVES
        
    def apply_gravity(self):
        self.direction.y += self.gravity
        if self.direction.y > TERMINAL_VELOCITY:
            self.direction.y = TERMINAL_VELOCITY
    
    def jump(self):
        if self.on_ground:
            self.direction.y = -self.jump_strength
        elif self.on_wall:
            # Wall jump - push away from wall
            self.direction.y = -self.wall_jump_strength
            if self.facing_right:
                self.direction.x = -self.wall_jump_strength * 0.6
            else:
                self.direction.x = self.wall_jump_strength * 0.6
    
    def wall_slide(self):
        if self.on_wall and not self.on_ground and self.direction.y > 0:
            self.direction.y = self.wall_slide_speed
    
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_RIGHT]:
            self.direction.x += self.acceleration
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x -= self.acceleration
            self.facing_right = False
        else:
            # Apply friction
            if self.direction.x > 0:
                self.direction.x = max(0, self.direction.x - self.friction)
            elif self.direction.x < 0:
                self.direction.x = min(0, self.direction.x + self.friction)
        
        # Apply speed limit
        current_speed = self.speed
        if self.has_speed_boost:
            current_speed *= SPEED_BOOST_MULTIPLIER
            
        if self.direction.x > current_speed:
            self.direction.x = current_speed
        elif self.direction.x < -current_speed:
            self.direction.x = -current_speed
        
        # Jump
        if keys[pygame.K_SPACE] and (self.on_ground or self.on_wall):
            self.jump()
    
    def horizontal_collisions(self):
        self.rect.x += self.direction.x
        self.on_wall = False
        
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction.x > 0:  # Moving right
                    self.rect.right = sprite.rect.left
                    self.on_wall = True
                elif self.direction.x < 0:  # Moving left
                    self.rect.left = sprite.rect.right
                    self.on_wall = True
                self.direction.x = 0
    
    def vertical_collisions(self):
        self.apply_gravity()
        self.rect.y += self.direction.y
        self.on_ground = False
        
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:  # Moving down
                    self.rect.bottom = sprite.rect.top
                    self.on_ground = True
                elif self.direction.y < 0:  # Moving up
                    self.rect.top = sprite.rect.bottom
                self.direction.y = 0
    
    def check_enemy_collisions(self, enemy_sprites):
        for enemy in enemy_sprites:
            if self.rect.colliderect(enemy.rect):
                # Check if landing on top of enemy (bouncing)
                if self.rect.bottom <= enemy.rect.centery and self.direction.y > 0:
                    self.direction.y = -self.jump_strength * 0.7  # Bounce
                    enemy.kill()  # Defeat enemy
                elif not self.is_invincible:
                    # Take damage
                    self.take_damage()
                    return True
        return False
    
    def check_hazard_collisions(self, hazard_sprites):
        for hazard in hazard_sprites:
            if self.rect.colliderect(hazard.rect) and not self.is_invincible:
                self.take_damage()
                return True
        return False
    
    def check_powerup_collisions(self, powerup_sprites):
        for powerup in powerup_sprites:
            if self.rect.colliderect(powerup.rect):
                powerup_type = powerup.type
                if powerup_type == 'speed':
                    self.has_speed_boost = True
                    self.speed_boost_timer = pygame.time.get_ticks()
                elif powerup_type == 'slow_time':
                    self.has_slow_time = True
                    self.slow_time_timer = pygame.time.get_ticks()
                elif powerup_type == 'invincibility':
                    self.is_invincible = True
                    self.invincibility_timer = pygame.time.get_ticks()
                powerup.kill()
    
    def update_powerups(self):
        current_time = pygame.time.get_ticks()
        
        # Speed boost
        if self.has_speed_boost and current_time - self.speed_boost_timer > SPEED_BOOST_DURATION:
            self.has_speed_boost = False
        
        # Slow time
        if self.has_slow_time and current_time - self.slow_time_timer > SLOW_TIME_DURATION:
            self.has_slow_time = False
        
        # Invincibility
        if self.is_invincible and current_time - self.invincibility_timer > INVINCIBILITY_DURATION:
            self.is_invincible = False
    
    def take_damage(self):
        self.lives -= 1
        # Flash effect or temporary invincibility could be added here
        self.is_invincible = True
        self.invincibility_timer = pygame.time.get_ticks()
        
        # Reset position to a safe spot (would be handled by the level)
        # self.rect.topleft = (safe_x, safe_y)
    
    def record_position(self, elapsed_time):
        """Record current position with timestamp for ghost replay"""
        self.position_history.append({
            'time': elapsed_time,
            'x': self.rect.x,
            'y': self.rect.y,
            'facing_right': self.facing_right
        })
    
    def update(self, elapsed_time=0):
        """Update player state"""
        # Get input
        self.get_input()
        
        # Apply gravity
        self.apply_gravity()
        
        # Wall slide
        self.wall_slide()
        
        # Handle collisions
        self.horizontal_collisions()
        self.vertical_collisions()
        
        # Update power-up timers
        self.update_powerups()
        
        # Update animation
        self.animate()
        
        # Record position for ghost replay
        if elapsed_time > 0:
            self.position_history.append({
                'time': elapsed_time,
                'x': self.rect.x,
                'y': self.rect.y,
                'facing_right': self.facing_right,
                'is_running': self.is_running,
                'is_jumping': self.is_jumping,
                'is_falling': self.is_falling
            })
        elif self.has_speed_boost:
            self.image.fill(GREEN)
        elif self.has_slow_time:
            self.image.fill(PURPLE)
        else:
            self.image.fill(BLUE)
