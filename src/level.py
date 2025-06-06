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

class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface((size, size * 2), pygame.SRCALPHA)
        
        # Create a checkpoint flag
        FLAG_COLOR = (0, 255, 255)    # Cyan
        POLE_COLOR = (200, 200, 200)  # Silver
        
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
        
        # Add a glowing effect
        glow_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (0, 255, 255, 50), (size, size), size)
        self.image.blit(glow_surf, (-size//2, 0))
        
        self.rect = self.image.get_rect(bottomleft=pos)
        self.activated = False
        self.position = pos
        
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
        
    def activate(self):
        self.activated = True
        # Change color to indicate activation
        if self.activated:
            # Redraw the flag in gold color
            size = self.rect.width
            FLAG_COLOR = (255, 215, 0)  # Gold
            
            # Clear the flag portion
            pygame.draw.rect(self.image, (0, 0, 0, 0), (size//2, size//4, size//2, size//2))
            
            # Redraw the flag
            flag_points = [
                (size//2, size//4),
                (size - 4, size//2),
                (size//2, size * 3//4)
            ]
            pygame.draw.polygon(self.image, FLAG_COLOR, flag_points)
            
            # Add some details to the flag
            pygame.draw.circle(self.image, (255, 255, 255), (size * 3//4, size//2), size//8)
            
            # Add a stronger glowing effect
            glow_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 215, 0, 80), (size, size), size)
            self.image.blit(glow_surf, (-size//2, 0))

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
        self.checkpoint_sprites = pygame.sprite.Group()
        
        # Player and ghost
        self.player = None
        self.ghost = Ghost([self.all_sprites])
        self.ghost.load_ghost_data(level_name)
        
        # Camera
        self.camera_offset = pygame.math.Vector2(0, 0)
        
        # UI reference for powerup notifications
        self.ui = None
        
        # Checkpoint system
        self.current_checkpoint = None
        self.checkpoint_positions = []
        
        # Load the level
        self.load_level()
    
    def load_level(self):
        """Load level from TMX file or create a simple test level"""
        # Skip TMX loading for now and just create a test level
        # This avoids the image format error
        if self.level_name == "level1":
            self.create_test_level()
        elif self.level_name == "level2":
            self.create_level2()
        else:
            self.create_test_level()  # Default to level 1
    
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
            elif obj.type == 'checkpoint':
                checkpoint = Checkpoint(pos, TILE_SIZE, [self.all_sprites, self.checkpoint_sprites])
                self.checkpoint_positions.append((pos[0], pos[1]))
    
    def create_test_level(self):
        """Create a simple test level if no TMX file is available"""
        # Create a much longer level (9x the screen width - 3 times longer than before)
        level_width = WIDTH * 9
        
        # Create a solid floor that extends beyond the screen
        # First create a boundary at the bottom to prevent anything from falling through
        for x in range(-TILE_SIZE * 10, level_width + TILE_SIZE * 10, TILE_SIZE):
            # Create invisible boundary at the very bottom
            boundary = Tile((x, HEIGHT), TILE_SIZE, [self.collision_sprites], 'invisible')
            boundary.rect.height = TILE_SIZE * 10  # Make it very tall to catch everything
        
        # Create ground for the entire level with gaps for jumping challenges
        for x in range(-TILE_SIZE * 10, level_width + TILE_SIZE * 10, TILE_SIZE):
            # Create gaps in the ground at specific intervals for jumping challenges
            if not (1000 <= x <= 1100 or 
                    2200 <= x <= 2350 or 
                    3500 <= x <= 3650 or 
                    4800 <= x <= 5000 or 
                    6200 <= x <= 6400 or 
                    7500 <= x <= 7700):
                # Create the top grass layer
                ground_tile = Tile((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.collision_sprites], 'grass')
                
                # Fill in dirt blocks below the grass to prevent void
                for y in range(HEIGHT, HEIGHT + TILE_SIZE * 10, TILE_SIZE):
                    Tile((x, y), TILE_SIZE, [self.all_sprites, self.collision_sprites], 'dirt')
        
        # SECTION 1 - First third of the level
        # Create platforms throughout the level
        platform1_y = HEIGHT - 180
        for x in range(200, 400, TILE_SIZE):
            Tile((x, platform1_y), TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        platform2_y = HEIGHT - 260
        for x in range(500, 700, TILE_SIZE):
            Tile((x, platform2_y), TILE_SIZE, [self.all_sprites, self.collision_sprites])
            
        # Add floating platforms for the first gap
        gap1_platforms = [
            (950, HEIGHT - 150),
            (1050, HEIGHT - 150),
            (1150, HEIGHT - 150)
        ]
        for pos in gap1_platforms:
            Tile(pos, TILE_SIZE, [self.all_sprites, self.collision_sprites])
            
        # Add staggered jumping platforms
        stair_y = HEIGHT - 200
        for i in range(5):
            Tile((1300 + i * 70, stair_y - i * 40), TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        # Add a moving platform
        MovingPlatform((1700, HEIGHT - 250), TILE_SIZE, [self.all_sprites, self.collision_sprites], 200, 2, 'horizontal')
        
        # SECTION 2 - Middle third of the level
        # Create more complex platform arrangements
        # Zigzag platforms
        zigzag_base_y = HEIGHT - 200
        for i in range(6):
            offset = 0 if i % 2 == 0 else 80
            platform_width = 3 * TILE_SIZE
            for j in range(platform_width // TILE_SIZE):
                Tile((WIDTH * 3 + 100 + i * 150 + j * TILE_SIZE + offset, zigzag_base_y - i * 50), 
                     TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        # Add floating single blocks for precise jumping
        air_blocks = [
            (WIDTH * 3 + 1100, HEIGHT - 300),
            (WIDTH * 3 + 1200, HEIGHT - 350),
            (WIDTH * 3 + 1300, HEIGHT - 400),
            (WIDTH * 3 + 1400, HEIGHT - 350),
            (WIDTH * 3 + 1500, HEIGHT - 300)
        ]
        for pos in air_blocks:
            Tile(pos, TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        # Add a series of moving platforms
        MovingPlatform((WIDTH * 3 + 1700, HEIGHT - 250), TILE_SIZE, [self.all_sprites, self.collision_sprites], 150, 3, 'vertical')
        MovingPlatform((WIDTH * 3 + 1900, HEIGHT - 300), TILE_SIZE, [self.all_sprites, self.collision_sprites], 200, 2, 'horizontal')
        MovingPlatform((WIDTH * 3 + 2200, HEIGHT - 350), TILE_SIZE, [self.all_sprites, self.collision_sprites], 150, 3, 'vertical')
        
        # SECTION 3 - Final third of the level
        # Create an advanced obstacle course
        # Alternating platforms at different heights
        for i in range(8):
            height_offset = 250 if i % 2 == 0 else 350
            platform_width = 2 * TILE_SIZE
            for j in range(platform_width // TILE_SIZE):
                Tile((WIDTH * 6 + 300 + i * 200 + j * TILE_SIZE, HEIGHT - height_offset), 
                     TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        # Create a challenging jumping section with small platforms
        jump_challenge = [
            (WIDTH * 6 + 2000, HEIGHT - 200),
            (WIDTH * 6 + 2100, HEIGHT - 250),
            (WIDTH * 6 + 2200, HEIGHT - 300),
            (WIDTH * 6 + 2300, HEIGHT - 350),
            (WIDTH * 6 + 2400, HEIGHT - 400),
            (WIDTH * 6 + 2500, HEIGHT - 350),
            (WIDTH * 6 + 2600, HEIGHT - 300),
            (WIDTH * 6 + 2700, HEIGHT - 250),
            (WIDTH * 6 + 2800, HEIGHT - 200)
        ]
        for pos in jump_challenge:
            Tile(pos, TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        # Final approach with moving platforms and hazards
        MovingPlatform((WIDTH * 8, HEIGHT - 250), TILE_SIZE, [self.all_sprites, self.collision_sprites], 100, 4, 'vertical')
        MovingPlatform((WIDTH * 8 + 200, HEIGHT - 300), TILE_SIZE, [self.all_sprites, self.collision_sprites], 150, 3, 'horizontal')
        MovingPlatform((WIDTH * 8 + 400, HEIGHT - 350), TILE_SIZE, [self.all_sprites, self.collision_sprites], 100, 5, 'vertical')
        
        # Create hazards throughout the level
        # Section 1 hazards
        Hazard((300, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((600, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((900, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        
        # Add lava hazards in the gaps - properly positioned at ground level
        for x in range(1000, 1100, TILE_SIZE):
            Hazard((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
        
        for x in range(2200, 2350, TILE_SIZE):
            Hazard((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
            
        # Section 2 hazards
        Hazard((WIDTH * 3 + 300, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((WIDTH * 3 + 600, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((WIDTH * 3 + 900, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        
        # Add lava hazards below air blocks to punish missed jumps - fixed to have no gaps
        for x in range(WIDTH * 3 + 1100, WIDTH * 3 + 1600, TILE_SIZE):
            Hazard((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
            
        # Section 3 hazards
        Hazard((WIDTH * 6 + 500, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((WIDTH * 6 + 800, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((WIDTH * 6 + 1100, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        
        # Add lava hazards in the final gaps
        for x in range(6200, 6400, TILE_SIZE):
            Hazard((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
            
        for x in range(7500, 7700, TILE_SIZE):
            Hazard((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
        
        # Create enemies throughout the level
        # Section 1 enemies
        Enemy((400, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'basic')
        Enemy((800, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'basic')
        Enemy((1500, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 150, 'jumping')
        Enemy((1800, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'flying')
        
        # Section 2 enemies
        Enemy((WIDTH * 3 + 300, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'basic')
        Enemy((WIDTH * 3 + 700, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 150, 'jumping')
        Enemy((WIDTH * 3 + 1000, HEIGHT - 350), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'flying')
        Enemy((WIDTH * 3 + 1600, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'basic')
        Enemy((WIDTH * 3 + 2000, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 150, 'jumping')
        
        # Section 3 enemies
        Enemy((WIDTH * 6 + 400, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'basic')
        Enemy((WIDTH * 6 + 900, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 150, 'jumping')
        Enemy((WIDTH * 6 + 1300, HEIGHT - 300), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'flying')
        Enemy((WIDTH * 6 + 1800, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'basic')
        Enemy((WIDTH * 6 + 2200, HEIGHT - 400), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'flying')
        Enemy((WIDTH * 6 + 2600, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 150, 'jumping')
        
        # Create power-ups throughout the level
        # Section 1 powerups
        PowerUp((250, platform1_y - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'speed', self.collision_sprites)
        PowerUp((550, platform2_y - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'invincibility', self.collision_sprites)
        PowerUp((1050, HEIGHT - 180), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'extra_life', self.collision_sprites)
        PowerUp((1500, stair_y - 200), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'speed', self.collision_sprites)
        
        # Section 2 powerups
        PowerUp((WIDTH * 3 + 250, zigzag_base_y - 50), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'speed', self.collision_sprites)
        PowerUp((WIDTH * 3 + 1300, HEIGHT - 430), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'invincibility', self.collision_sprites)
        PowerUp((WIDTH * 3 + 1900, HEIGHT - 330), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'extra_life', self.collision_sprites)
        
        # Section 3 powerups
        PowerUp((WIDTH * 6 + 400, HEIGHT - 280), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'speed', self.collision_sprites)
        PowerUp((WIDTH * 6 + 2400, HEIGHT - 430), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'invincibility', self.collision_sprites)
        PowerUp((WIDTH * 8 + 200, HEIGHT - 330), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'extra_life', self.collision_sprites)
        
        # Add checkpoints at strategic locations
        # First checkpoint - after the first section
        checkpoint1 = Checkpoint((WIDTH * 2, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.checkpoint_sprites])
        self.checkpoint_positions.append((WIDTH * 2, HEIGHT - TILE_SIZE * 2))
        
        # Second checkpoint - after the second section (moved back to safe ground)
        checkpoint2 = Checkpoint((WIDTH * 5 + 800, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.checkpoint_sprites])
        self.checkpoint_positions.append((WIDTH * 5 + 800, HEIGHT - TILE_SIZE * 2))
        
        # Create finish flag at the end of the extended level - properly positioned on the ground
        FinishFlag((WIDTH * 9 - 100, HEIGHT - TILE_SIZE * 3), TILE_SIZE, [self.all_sprites, self.finish_sprites])
        
        # Create player - fixed the argument order to match Player.__init__
        self.player = Player(100, HEIGHT - 200, [self.all_sprites], self.collision_sprites)
    def create_level2(self):
        """Create a more difficult second level"""
        # Create a much longer level (9x the screen width - same as level 1)
        level_width = WIDTH * 9
        
        # Create a solid floor that extends beyond the screen
        # First create a boundary at the bottom to prevent anything from falling through
        for x in range(-TILE_SIZE * 10, level_width + TILE_SIZE * 10, TILE_SIZE):
            # Create invisible boundary at the very bottom
            boundary = Tile((x, HEIGHT), TILE_SIZE, [self.collision_sprites], 'invisible')
            boundary.rect.height = TILE_SIZE * 10  # Make it very tall to catch everything
        
        # Create ground for the entire level with MORE gaps for jumping challenges
        for x in range(-TILE_SIZE * 10, level_width + TILE_SIZE * 10, TILE_SIZE):
            # Create more gaps in the ground for increased difficulty
            if not (800 <= x <= 950 or 
                    1500 <= x <= 1700 or 
                    2400 <= x <= 2600 or 
                    3300 <= x <= 3500 or 
                    4200 <= x <= 4500 or 
                    5100 <= x <= 5400 or 
                    6000 <= x <= 6300 or 
                    7000 <= x <= 7400):
                # Create the top grass layer
                ground_tile = Tile((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.collision_sprites], 'grass')
                
                # Fill in dirt blocks below the grass to prevent void
                for y in range(HEIGHT, HEIGHT + TILE_SIZE * 10, TILE_SIZE):
                    Tile((x, y), TILE_SIZE, [self.all_sprites, self.collision_sprites], 'dirt')
        
        # SECTION 1 - First third of the level (more challenging)
        # Create narrower platforms throughout the level
        platform1_y = HEIGHT - 180
        for x in range(200, 300, TILE_SIZE):  # Shorter platform
            Tile((x, platform1_y), TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        platform2_y = HEIGHT - 260
        for x in range(500, 550, TILE_SIZE):  # Even shorter platform
            Tile((x, platform2_y), TILE_SIZE, [self.all_sprites, self.collision_sprites])
            
        # Add floating platforms for the first gap - more spaced out
        gap1_platforms = [
            (850, HEIGHT - 150),
            (1000, HEIGHT - 180),
            (1150, HEIGHT - 210)
        ]
        for pos in gap1_platforms:
            Tile(pos, TILE_SIZE, [self.all_sprites, self.collision_sprites])
            
        # Add steeper staggered jumping platforms
        stair_y = HEIGHT - 200
        for i in range(5):
            Tile((1300 + i * 60, stair_y - i * 50), TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        # Add more moving platforms
        MovingPlatform((1700, HEIGHT - 250), TILE_SIZE, [self.all_sprites, self.collision_sprites], 200, 3, 'horizontal')
        MovingPlatform((2000, HEIGHT - 300), TILE_SIZE, [self.all_sprites, self.collision_sprites], 150, 4, 'vertical')
        
        # SECTION 2 - Middle third of the level (more complex)
        # Create more complex platform arrangements
        # Zigzag platforms with bigger height differences
        zigzag_base_y = HEIGHT - 200
        for i in range(6):
            offset = 0 if i % 2 == 0 else 100  # Bigger offset
            platform_width = 2 * TILE_SIZE  # Narrower platforms
            for j in range(platform_width // TILE_SIZE):
                Tile((WIDTH * 3 + 100 + i * 180 + j * TILE_SIZE + offset, zigzag_base_y - i * 60), 
                     TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        # Add floating single blocks for precise jumping - more challenging arrangement
        air_blocks = [
            (WIDTH * 3 + 1100, HEIGHT - 300),
            (WIDTH * 3 + 1200, HEIGHT - 380),  # Higher
            (WIDTH * 3 + 1300, HEIGHT - 450),  # Even higher
            (WIDTH * 3 + 1400, HEIGHT - 380),
            (WIDTH * 3 + 1500, HEIGHT - 300)
        ]
        for pos in air_blocks:
            Tile(pos, TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        # Add a series of moving platforms - faster and more challenging
        MovingPlatform((WIDTH * 3 + 1700, HEIGHT - 250), TILE_SIZE, [self.all_sprites, self.collision_sprites], 180, 4, 'vertical')
        MovingPlatform((WIDTH * 3 + 1900, HEIGHT - 300), TILE_SIZE, [self.all_sprites, self.collision_sprites], 250, 3, 'horizontal')
        MovingPlatform((WIDTH * 3 + 2200, HEIGHT - 350), TILE_SIZE, [self.all_sprites, self.collision_sprites], 200, 5, 'vertical')
        
        # SECTION 3 - Final third of the level (most challenging)
        # Create an advanced obstacle course
        # Alternating platforms at different heights - more extreme
        for i in range(8):
            height_offset = 250 if i % 2 == 0 else 400  # Bigger difference
            platform_width = 1 * TILE_SIZE  # Single tile platforms
            for j in range(platform_width // TILE_SIZE):
                Tile((WIDTH * 6 + 300 + i * 220 + j * TILE_SIZE, HEIGHT - height_offset), 
                     TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        # Create a challenging jumping section with small platforms - more extreme
        jump_challenge = [
            (WIDTH * 6 + 2000, HEIGHT - 200),
            (WIDTH * 6 + 2100, HEIGHT - 270),
            (WIDTH * 6 + 2200, HEIGHT - 340),
            (WIDTH * 6 + 2300, HEIGHT - 410),  # Higher
            (WIDTH * 6 + 2400, HEIGHT - 480),  # Even higher
            (WIDTH * 6 + 2500, HEIGHT - 410),
            (WIDTH * 6 + 2600, HEIGHT - 340),
            (WIDTH * 6 + 2700, HEIGHT - 270),
            (WIDTH * 6 + 2800, HEIGHT - 200)
        ]
        for pos in jump_challenge:
            Tile(pos, TILE_SIZE, [self.all_sprites, self.collision_sprites])
        
        # Final approach with moving platforms and hazards - faster and more challenging
        MovingPlatform((WIDTH * 8, HEIGHT - 250), TILE_SIZE, [self.all_sprites, self.collision_sprites], 120, 5, 'vertical')
        MovingPlatform((WIDTH * 8 + 200, HEIGHT - 300), TILE_SIZE, [self.all_sprites, self.collision_sprites], 180, 4, 'horizontal')
        MovingPlatform((WIDTH * 8 + 400, HEIGHT - 350), TILE_SIZE, [self.all_sprites, self.collision_sprites], 150, 6, 'vertical')
        
        # Create hazards throughout the level - more of them
        # Section 1 hazards
        Hazard((300, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((500, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((700, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((1200, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        
        # Add lava hazards in the gaps - properly positioned at ground level with no gaps
        for x in range(800, 950, TILE_SIZE):
            Hazard((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
        
        for x in range(1500, 1700, TILE_SIZE):
            Hazard((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
            
        for x in range(2400, 2600, TILE_SIZE):
            Hazard((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
            
        # Section 2 hazards
        Hazard((WIDTH * 3 + 300, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((WIDTH * 3 + 500, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((WIDTH * 3 + 700, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((WIDTH * 3 + 900, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        
        # Add lava hazards below air blocks to punish missed jumps - fixed to have no gaps
        for x in range(WIDTH * 3 + 1100, WIDTH * 3 + 1600, TILE_SIZE):
            Hazard((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
            
        for x in range(3300, 3500, TILE_SIZE):
            Hazard((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
            
        for x in range(4200, 4500, TILE_SIZE):
            Hazard((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
            
        # Section 3 hazards
        Hazard((WIDTH * 6 + 400, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((WIDTH * 6 + 600, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((WIDTH * 6 + 800, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((WIDTH * 6 + 1000, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        Hazard((WIDTH * 6 + 1200, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'spike')
        
        # Add lava hazards in the final gaps - fixed to have no gaps
        for x in range(5100, 5400, TILE_SIZE):
            Hazard((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
            
        for x in range(6000, 6300, TILE_SIZE):
            Hazard((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
            
        for x in range(7000, 7400, TILE_SIZE):
            Hazard((x, HEIGHT - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.hazard_sprites], 'lava')
        
        # Create enemies throughout the level - more of them and more challenging types
        # Section 1 enemies
        Enemy((400, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 120, 'basic')
        Enemy((600, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 120, 'basic')
        Enemy((1000, HEIGHT - 210), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 0, 'flying')  # Stationary flying enemy
        Enemy((1300, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 180, 'jumping')
        Enemy((1600, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 150, 'jumping')
        Enemy((1900, HEIGHT - 300), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'flying')
        
        # Section 2 enemies
        Enemy((WIDTH * 3 + 200, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 150, 'basic')
        Enemy((WIDTH * 3 + 400, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 150, 'basic')
        Enemy((WIDTH * 3 + 600, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 180, 'jumping')
        Enemy((WIDTH * 3 + 800, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 180, 'jumping')
        Enemy((WIDTH * 3 + 1000, HEIGHT - 380), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 100, 'flying')
        Enemy((WIDTH * 3 + 1300, HEIGHT - 450), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 0, 'flying')  # Stationary flying enemy
        Enemy((WIDTH * 3 + 1600, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 150, 'basic')
        Enemy((WIDTH * 3 + 1800, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 180, 'jumping')
        Enemy((WIDTH * 3 + 2000, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 180, 'jumping')
        
        # Section 3 enemies
        Enemy((WIDTH * 6 + 300, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 150, 'basic')
        Enemy((WIDTH * 6 + 500, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 150, 'basic')
        Enemy((WIDTH * 6 + 700, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 180, 'jumping')
        Enemy((WIDTH * 6 + 900, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 180, 'jumping')
        Enemy((WIDTH * 6 + 1100, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 150, 'basic')
        Enemy((WIDTH * 6 + 1300, HEIGHT - 300), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 120, 'flying')
        Enemy((WIDTH * 6 + 1500, HEIGHT - 350), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 120, 'flying')
        Enemy((WIDTH * 6 + 1800, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 150, 'basic')
        Enemy((WIDTH * 6 + 2000, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 180, 'jumping')
        Enemy((WIDTH * 6 + 2200, HEIGHT - 410), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 0, 'flying')  # Stationary flying enemy
        Enemy((WIDTH * 6 + 2400, HEIGHT - 480), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 0, 'flying')  # Stationary flying enemy
        Enemy((WIDTH * 6 + 2600, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.enemy_sprites], 180, 'jumping')
        
        # Create power-ups throughout the level - fewer of them for increased difficulty
        # Section 1 powerups
        PowerUp((250, platform1_y - TILE_SIZE), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'speed', self.collision_sprites)
        PowerUp((1150, HEIGHT - 240), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'invincibility', self.collision_sprites)
        
        # Section 2 powerups
        PowerUp((WIDTH * 3 + 1300, HEIGHT - 480), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'extra_life', self.collision_sprites)
        PowerUp((WIDTH * 3 + 1900, HEIGHT - 330), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'speed', self.collision_sprites)
        
        # Section 3 powerups
        PowerUp((WIDTH * 6 + 2400, HEIGHT - 510), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'invincibility', self.collision_sprites)
        PowerUp((WIDTH * 8 + 200, HEIGHT - 330), TILE_SIZE, [self.all_sprites, self.powerup_sprites], 'extra_life', self.collision_sprites)
        
        # Add checkpoints at strategic locations
        # First checkpoint - after the first section
        checkpoint1 = Checkpoint((WIDTH * 2, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.checkpoint_sprites])
        self.checkpoint_positions.append((WIDTH * 2, HEIGHT - TILE_SIZE * 2))
        
        # Second checkpoint - after the second section (on safe ground)
        checkpoint2 = Checkpoint((WIDTH * 5 + 800, HEIGHT - TILE_SIZE * 2), TILE_SIZE, [self.all_sprites, self.checkpoint_sprites])
        self.checkpoint_positions.append((WIDTH * 5 + 800, HEIGHT - TILE_SIZE * 2))
        
        # Create finish flag at the end of the extended level - properly positioned on the ground
        FinishFlag((WIDTH * 9 - 100, HEIGHT - TILE_SIZE * 3), TILE_SIZE, [self.all_sprites, self.finish_sprites])
        
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
            # Removed debug print to improve performance
            return
        
        # Removed debug print to improve performance
        
        # Update player
        self.player.update(elapsed_time)
        
        # Update ghost - disable ghost shadow
        # self.ghost.update(elapsed_time)
        
        # Update enemies
        for enemy in self.enemy_sprites:
            enemy.update(self.collision_sprites)
        
        # Update power-ups
        for powerup in self.powerup_sprites:
            powerup.update()
        
        # Update hazards (for animation)
        for hazard in self.hazard_sprites:
            if hasattr(hazard, 'update'):
                hazard.update()
        
        # Update checkpoints
        for checkpoint in self.checkpoint_sprites:
            checkpoint.update()
            # Check if player has reached this checkpoint
            if self.player.rect.colliderect(checkpoint.rect) and not checkpoint.activated:
                checkpoint.activate()
                self.current_checkpoint = checkpoint
                print(f"Checkpoint activated at {checkpoint.position}")
                # Show notification on UI
                if self.ui:
                    self.ui.show_powerup_notification("Checkpoint Reached!")
        
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
                    # Reset player position to last checkpoint or start
                    self.respawn_player()
                break
        
        # Check hazard collisions
        for hazard in self.hazard_sprites:
            if self.player.rect.colliderect(hazard.rect):
                if not self.player.invincible:
                    # Player takes damage
                    self.player.lives -= 1
                    print(f"Player hit by hazard! Lives left: {self.player.lives}")
                    # Reset player position to last checkpoint or start
                    self.respawn_player()
                break
        
        # Check powerup collisions
        for powerup in list(self.powerup_sprites):
            if self.player.rect.colliderect(powerup.rect):
                # Apply powerup effect
                if powerup.type == 'speed':
                    self.player.activate_speed_boost(powerup.duration)
                    print("Speed boost activated!")
                    # Show notification on UI
                    if self.ui:
                        self.ui.show_powerup_notification("Speed Boost")
                elif powerup.type == 'invincibility':
                    self.player.activate_invincibility(powerup.duration)
                    print("Invincibility activated!")
                    # Show notification on UI
                    if self.ui:
                        self.ui.show_powerup_notification("Invincibility")
                elif powerup.type == 'extra_life':
                    self.player.lives += 1
                    print("Extra life collected! Lives:", self.player.lives)
                    # Show notification on UI
                    if self.ui:
                        self.ui.show_powerup_notification("Extra Life")
                
                # Remove powerup
                powerup.kill()
                break
    
    def respawn_player(self):
        """Respawn the player at the last checkpoint or start position"""
        if self.current_checkpoint:
            # Respawn at checkpoint
            self.player.rect.x = self.current_checkpoint.position[0]
            self.player.rect.y = self.current_checkpoint.position[1] - TILE_SIZE * 2  # Adjust height to be above the ground
            print(f"Player respawned at checkpoint: {self.current_checkpoint.position}")
        else:
            # Respawn at start
            self.player.rect.x = 100
            self.player.rect.y = HEIGHT - 200
            print("Player respawned at start position")
        
        # Reset player velocity
        self.player.direction.x = 0
        self.player.direction.y = 0
    
    def draw_background(self):
        """Draw a gradient background with clouds that fills the entire screen"""
        # Create a gradient from blue to light blue
        height = self.display_surface.get_height()
        width = self.display_surface.get_width()
        
        # Fill the entire screen with sky gradient - ensure it covers everything
        for y in range(0, height):
            # Calculate color based on height
            # Top is darker blue, gradually becoming lighter
            r = int(80 + (y / height) * 100)
            g = int(120 + (y / height) * 80)
            b = int(235)
            
            pygame.draw.line(self.display_surface, (r, g, b), (0, y), (width, y))
        
        # Draw clouds
        # Use a deterministic approach based on game time to create moving clouds
        cloud_time = pygame.time.get_ticks() // 50  # Slow cloud movement
        
        # Draw several clouds at different heights and sizes
        for i in range(12):  # More clouds for better coverage
            x_pos = (width * (i * 0.12) - (cloud_time % (width * 2)) * 0.01) % (width * 1.2) - width * 0.1
            y_pos = height * (0.05 + (i % 5) * 0.08)
            cloud_size = 60 + (i % 5) * 20
            self.draw_cloud(x_pos, y_pos, cloud_size, cloud_size / 2)
        
        # Draw sun with improved glow effect
        sun_x = width * 0.85
        sun_y = height * 0.15
        sun_radius = 45
        
        # Draw sun glow with more layers for better effect
        for i in range(8, 0, -1):
            alpha = 120 - i * 12
            color = (255, 255, 200, alpha)
            glow_surf = pygame.Surface((sun_radius * 2 * i, sun_radius * 2 * i), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, color, (sun_radius * i, sun_radius * i), sun_radius * i)
            self.display_surface.blit(glow_surf, (sun_x - sun_radius * i, sun_y - sun_radius * i))
        
        # Draw sun body with gradient effect
        pygame.draw.circle(self.display_surface, (255, 255, 200), (sun_x, sun_y), sun_radius)
        pygame.draw.circle(self.display_surface, (255, 255, 100), (sun_x, sun_y), sun_radius - 5)
        pygame.draw.circle(self.display_surface, (255, 255, 50), (sun_x, sun_y), sun_radius - 15)
    
    def draw_cloud(self, x, y, width, height):
        """Draw a fluffy cloud"""
        cloud_color = (255, 255, 255, 180)  # Semi-transparent white
        
        # Create a surface for the cloud
        cloud_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw several overlapping circles to create a cloud shape
        circle_radius = height // 2
        positions = [
            (circle_radius, circle_radius),
            (width // 3, circle_radius // 2),
            (width // 2, circle_radius),
            (2 * width // 3, circle_radius // 2),
            (width - circle_radius, circle_radius)
        ]
        
        for pos in positions:
            pygame.draw.circle(cloud_surf, cloud_color, pos, circle_radius)
        
        # Blit the cloud to the display surface
        self.display_surface.blit(cloud_surf, (x, y))
    
    def draw(self):
        """Draw all level elements with camera offset"""
        # Fill background with a gradient sky - draw this first to cover everything
        self.draw_background()
        
        # Draw all sprites with camera offset
        for sprite in sorted(self.all_sprites, key=lambda s: 1 if isinstance(s, Player) else 0):
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
        self.checkpoint_sprites.empty()
        
        # Reset status
        self.active = False
        self.completed = False
        self.current_checkpoint = None
        self.checkpoint_positions = []
        
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
