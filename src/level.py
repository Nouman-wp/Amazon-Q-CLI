"""
Level module for SpeedRunner X.
Handles level loading, rendering, and management.
"""
import pygame
import os
import math
from src.settings import *
from src.player import Player
from src.enemy import Enemy
from src.tiles import Tile, Hazard, MovingPlatform, FinishFlag
from src.powerups import PowerUp
from src.ghost import Ghost

# Import pytmx conditionally to handle potential import errors
try:
    import pytmx
    PYTMX_AVAILABLE = True
except ImportError:
    PYTMX_AVAILABLE = False
    print("Warning: pytmx module not found. Using fallback level creation.")

class Level:
    def __init__(self, level_name, surface):
        # Setup
        self.display_surface = surface
        self.level_name = level_name
        
        # Level status
        self.active = False
        self.completed = False
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.hazard_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.powerup_sprites = pygame.sprite.Group()
        self.finish_sprites = pygame.sprite.Group()
        
        # Player and ghost
        self.player = None
        self.ghost = Ghost([self.all_sprites])
        self.ghost.load_ghost_data(level_name)
        
        # Camera
        self.camera_offset = pygame.math.Vector2(0, 0)
        
        # UI reference for powerup notifications
        self.ui = None
        
        # Load the level
        self.load_level()
    
    def load_level(self):
        """Load level from TMX file or create a simple test level"""
        # Skip TMX loading for now and just create a test level
        # This avoids the image format error
        self.create_test_level()
    
    def load_tmx_level(self, tmx_path):
        """Load level from TMX file using PyTMX"""
        if not PYTMX_AVAILABLE:
            print("PyTMX not available, using test level instead")
            self.create_test_level()
            return
            
        tmx_data = pytmx.load_pygame(tmx_path)
        
        # Process tile layers
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, gid in layer.iter_data():
                    # Get tile properties
                    tile_props = tmx_data.get_tile_properties_by_gid(gid)
                    if tile_props is None:
                        continue
                    
                    # Calculate position
                    pos = (x * tmx_data.tilewidth, y * tmx_data.tileheight)
                    
                    # Create appropriate tile based on properties
                    if 'type' in tile_props:
                        if tile_props['type'] == 'solid':
                            Tile(pos, tmx_data.tilewidth, [self.all_sprites, self.collision_sprites])
                        elif tile_props['type'] == 'hazard':
                            Hazard(pos, tmx_data.tilewidth, [self.all_sprites, self.hazard_sprites])
                    
        # Process object layers
        for obj in tmx_data.objects:
            pos = (obj.x, obj.y)
            
            if obj.type == 'player_start':
                self.player = Player(pos, [self.all_sprites], self.collision_sprites)
            elif obj.type == 'enemy':
                enemy_type = obj.properties.get('enemy_type', 'basic')
                patrol_distance = obj.properties.get('patrol_distance', 128)
                Enemy(pos, TILE_SIZE, [self.all_sprites, self.enemy_sprites], patrol_distance, enemy_type)
            elif obj.type == 'powerup':
                powerup_type = obj.properties.get('powerup_type', 'speed')
                PowerUp(pos, TILE_SIZE, [self.all_sprites, self.powerup_sprites], powerup_type)
            elif obj.type == 'finish':
                FinishFlag(pos, TILE_SIZE, [self.all_sprites, self.finish_sprites])
            elif obj.type == 'moving_platform':
                direction = obj.properties.get('direction', 'horizontal')
                distance = obj.properties.get('distance', 128)
                speed = obj.properties.get('speed', 2)
                MovingPlatform(pos, TILE_SIZE, [self.all_sprites, self.collision_sprites], distance, speed, direction)
    
    def create_test_level(self):
        """Create a simple test level if no TMX file is available"""
        # Create a much longer level (3x the screen width)
        level_width = WIDTH * 3
        
        # Create ground for the entire level - fill the bottom completely
        for x in range(0, level_width + TILE_SIZE, TILE_SIZE):
            # Create the top grass layer
            ground_tile = Tile((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.collision_sprites], 'grass')
            
            # Fill in dirt blocks below the grass to prevent void
            for y in range(HEIGHT, HEIGHT + TILE_SIZE * 3, TILE_SIZE):
                Tile((x, y), TILE_SIZE, [self.all_sprites, self.collision_sprites], 'dirt')
        
        # Create platforms throughout the level
        # First section
        for x in range(200, 400, TILE_SIZE):
            Tile((x, HEIGHT - 180), TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        for x in range(500, 700, TILE_SIZE):
            Tile((x, HEIGHT - 260), TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        # Middle section
        for x in range(WIDTH + 100, WIDTH + 300, TILE_SIZE):
            Tile((x, HEIGHT - 200), TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        for x in range(WIDTH + 400, WIDTH + 700, TILE_SIZE):
            Tile((x, HEIGHT - 300), TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        # Final section
        for x in range(WIDTH * 2, WIDTH * 2 + 300, TILE_SIZE):
            Tile((x, HEIGHT - 220), TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        for x in range(WIDTH * 2 + 400, WIDTH * 2 + 800, TILE_SIZE):
            Tile((x, HEIGHT - 350), TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        # Create hazards throughout the level
        Hazard((300, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((600, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
        Hazard((WIDTH + 200, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((WIDTH + 500, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
        Hazard((WIDTH * 2 + 300, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        
        # Create enemies throughout the level
        Enemy((400, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'basic')
        Enemy((800, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'basic')
        Enemy((WIDTH + 300, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'basic')
        Enemy((WIDTH + 600, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'flying')
        Enemy((WIDTH * 2 + 200, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'basic')
        Enemy((WIDTH * 2 + 500, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'jumping')
        Enemy((WIDTH * 2 + 700, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'basic')
        
        # Create power-ups throughout the level with collision detection
        PowerUp((250, HEIGHT - 250), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'speed', self.collision_sprites)
        PowerUp((550, HEIGHT - 350), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'invincibility', self.collision_sprites)
        PowerUp((WIDTH + 150, HEIGHT - 300), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'extra_life', self.collision_sprites)
        PowerUp((WIDTH + 650, HEIGHT - 400), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'invincibility', self.collision_sprites)
        PowerUp((WIDTH * 2 + 350, HEIGHT - 320), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'speed', self.collision_sprites)
        PowerUp((WIDTH * 2 + 700, HEIGHT - 450), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'extra_life', self.collision_sprites)
        
        # Create finish flag at the end of the extended level
        FinishFlag((WIDTH * 3 - 100, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.finish_sprites])
        
        # Create player - fixed the argument order to match Player.__init__
        self.player = Player(100, HEIGHT - 200, [self.all_sprites], self.collision_sprites)
    
    def update_camera(self):
        """Update camera position to follow player"""
        # Target position is centered on player
        target_x = WIDTH / 2 - self.player.rect.centerx
        target_y = HEIGHT / 2 - self.player.rect.centery
        
        # Smooth camera movement
        self.camera_offset.x += (target_x - self.camera_offset.x) * 0.05
        self.camera_offset.y += (target_y - self.camera_offset.y) * 0.05
    
    def check_level_complete(self):
        """Check if player has reached the finish flag"""
        for flag in self.finish_sprites:
            if self.player.rect.colliderect(flag.rect):
                self.completed = True
                return True
        return False
    
    def update(self, elapsed_time):
        """Update all level elements"""
        if not self.active:
            print("Level not active, skipping update")
            return
        
        print(f"Updating level at time {elapsed_time}")
        
        # Update player
        self.player.update(elapsed_time)
        
        # Update ghost
        self.ghost.update(elapsed_time)
        
        # Update enemies
        for enemy in self.enemy_sprites:
            enemy.update(self.collision_sprites)
        
        # Update power-ups
        for powerup in self.powerup_sprites:
            powerup.update()
        
        # Update moving platforms
        for sprite in self.collision_sprites:
            if isinstance(sprite, MovingPlatform):
                sprite.update()
        
        # Check collisions
        self.check_collisions()
        
        # Check level completion
        self.check_level_complete()
        
        # Update camera
        self.update_camera()
    
    def check_collisions(self):
        """Check all collisions"""
        # Check enemy collisions
        for enemy in self.enemy_sprites:
            if self.player.rect.colliderect(enemy.rect):
                # Check if player is stomping the enemy from above
                if self.player.rect.bottom < enemy.rect.centery and self.player.direction.y > 0:
                    # Player is stomping the enemy
                    enemy.kill()
                    # Give player a small bounce
                    self.player.direction.y = -10
                    print("Enemy stomped!")
                elif self.player.invincible:
                    # If player is invincible, defeat the enemy
                    enemy.kill()
                    print("Enemy defeated with invincibility!")
                else:
                    # Player takes damage
                    self.player.lives -= 1
                    print(f"Player hit by enemy! Lives left: {self.player.lives}")
                    # Reset player position
                    self.player.rect.x = 100
                    self.player.rect.y = HEIGHT - 200
                break
        
        # Check hazard collisions
        for hazard in self.hazard_sprites:
            if self.player.rect.colliderect(hazard.rect):
                if not self.player.invincible:
                    # Player takes damage
                    self.player.lives -= 1
                    print(f"Player hit by hazard! Lives left: {self.player.lives}")
                    # Reset player position
                    self.player.rect.x = 100
                    self.player.rect.y = HEIGHT - 200
                break
        
        # Check powerup collisions
        for powerup in list(self.powerup_sprites):
            if self.player.rect.colliderect(powerup.rect):
                # Apply powerup effect
                if powerup.type == 'speed':
                    self.player.activate_speed_boost(powerup.duration)
                    print("Speed boost activated!")
                    # Show notification on UI
                    self.ui.show_powerup_notification("Speed Boost")
                elif powerup.type == 'invincibility':
                    self.player.activate_invincibility(powerup.duration)
                    print("Invincibility activated!")
                    # Show notification on UI
                    self.ui.show_powerup_notification("Invincibility")
                elif powerup.type == 'extra_life':
                    self.player.lives += 1
                    print("Extra life collected! Lives:", self.player.lives)
                    # Show notification on UI
                    self.ui.show_powerup_notification("Extra Life")
                
                # Remove powerup
                powerup.kill()
                break
    
    def draw(self):
        """Draw all level elements with camera offset"""
        # Fill background
        self.display_surface.fill(BLACK)
        
        # Draw all sprites with camera offset
        for sprite in self.all_sprites:
            offset_pos = sprite.rect.topleft + self.camera_offset
            self.display_surface.blit(sprite.image, offset_pos)
    
    def start(self):
        """Start the level"""
        self.active = True
        print("Level started - active state set to True")
    
    def reset(self):
        """Reset the level"""
        # Clear all sprites
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.hazard_sprites.empty()
        self.enemy_sprites.empty()
        self.powerup_sprites.empty()
        self.finish_sprites.empty()
        
        # Reset status
        self.active = False
        self.completed = False
        
        # Reset camera
        self.camera_offset = pygame.math.Vector2(0, 0)
        
        # Reload the level
        self.load_level()
        
        # Reload ghost data
        self.ghost = Ghost([self.all_sprites])
        self.ghost.load_ghost_data(self.level_name)
        
        print("Level reset complete")
    
    def get_player_position_history(self):
        """Get the player's position history for ghost replay"""
        if self.player:
            return self.player.position_history
        return []
    
    def get_player_position_history(self):
        """Get the player's position history for ghost replay"""
        return self.player.position_history
