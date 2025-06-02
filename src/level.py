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
        # Create ground
        for x in range(0, WIDTH + TILE_SIZE, TILE_SIZE):
            Tile((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.collision_sprites], 'grass')
        
        # Create some platforms - make them more accessible for jumping
        for x in range(200, 400, TILE_SIZE):
            Tile((x, HEIGHT - 180), TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        for x in range(500, 700, TILE_SIZE):
            Tile((x, HEIGHT - 260), TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        # Create some hazards
        Hazard((300, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((600, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
        
        # Create some enemies
        Enemy((400, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'basic')
        Enemy((800, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'basic')
        
        # Create some power-ups
        PowerUp((250, HEIGHT - 250), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'speed')
        PowerUp((550, HEIGHT - 350), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'invincibility')
        
        # Create finish flag
        FinishFlag((WIDTH - 100, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.finish_sprites])
        
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
            return
        
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
        self.player.check_enemy_collisions(self.enemy_sprites)
        self.player.check_hazard_collisions(self.hazard_sprites)
        self.player.check_powerup_collisions(self.powerup_sprites)
        
        # Check level completion
        self.check_level_complete()
        
        # Update camera
        self.update_camera()
    
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
        return self.player.position_history
