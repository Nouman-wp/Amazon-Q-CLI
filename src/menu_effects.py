"""
Menu Effects module for SpeedRunner X.
Contains animated effects for game menus.
"""
import pygame
import math
import random

class MenuEffects:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        
        # Particles for main menu
        self.particles = []
        self.create_particles(50)  # Create 50 particles
        
        # Speed lines for main menu
        self.speed_lines = []
        self.create_speed_lines(20)  # Create 20 speed lines
    
    def create_particles(self, count):
        """Create floating particles for menu background"""
        for _ in range(count):
            particle = {
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'size': random.randint(2, 5),
                'speed': random.uniform(0.5, 2.0),
                'color': (
                    random.randint(100, 200),  # R
                    random.randint(150, 255),  # G
                    random.randint(200, 255),  # B
                    random.randint(50, 150)    # Alpha
                ),
                'angle': random.uniform(0, 2 * math.pi)
            }
            self.particles.append(particle)
    
    def create_speed_lines(self, count):
        """Create speed lines for dynamic background effect"""
        for _ in range(count):
            line = {
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'length': random.randint(50, 200),
                'speed': random.uniform(5, 15),
                'color': (
                    random.randint(100, 200),  # R
                    random.randint(150, 255),  # G
                    random.randint(200, 255),  # B
                    random.randint(30, 100)    # Alpha
                ),
                'angle': random.uniform(-0.2, 0.2)  # Mostly horizontal
            }
            self.speed_lines.append(line)
    
    def update_particles(self):
        """Update particle positions"""
        for particle in self.particles:
            # Move particles in their direction
            particle['x'] += math.cos(particle['angle']) * particle['speed']
            particle['y'] += math.sin(particle['angle']) * particle['speed']
            
            # Wrap around screen edges
            if particle['x'] < 0:
                particle['x'] = self.width
            elif particle['x'] > self.width:
                particle['x'] = 0
                
            if particle['y'] < 0:
                particle['y'] = self.height
            elif particle['y'] > self.height:
                particle['y'] = 0
    
    def update_speed_lines(self):
        """Update speed lines positions"""
        for line in self.speed_lines:
            # Move lines from right to left (for racing effect)
            line['x'] -= line['speed']
            
            # Reset when off screen
            if line['x'] + line['length'] < 0:
                line['x'] = self.width + random.randint(0, 100)
                line['y'] = random.randint(0, self.height)
                line['length'] = random.randint(50, 200)
                line['speed'] = random.uniform(5, 15)
    
    def draw_particles(self):
        """Draw particles on screen"""
        for particle in self.particles:
            # Create a surface for the particle with alpha
            particle_surf = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            pygame.draw.circle(
                particle_surf, 
                particle['color'], 
                (particle['size']//2, particle['size']//2), 
                particle['size']//2
            )
            self.screen.blit(particle_surf, (int(particle['x']), int(particle['y'])))
    
    def draw_speed_lines(self):
        """Draw speed lines on screen"""
        for line in self.speed_lines:
            # Calculate end point based on angle and length
            end_x = line['x'] + line['length'] * math.cos(line['angle'])
            end_y = line['y'] + line['length'] * math.sin(line['angle'])
            
            # Draw the line with alpha
            line_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.line(
                line_surf,
                line['color'],
                (int(line['x']), int(line['y'])),
                (int(end_x), int(end_y)),
                2
            )
            self.screen.blit(line_surf, (0, 0))
    
    def draw_animated_title(self, text, pos, font_size=60, base_color=(255, 165, 0)):
        """Draw an animated title with wave effect"""
        font = pygame.font.Font(None, font_size)
        
        # Get current time for animation
        t = pygame.time.get_ticks() / 1000
        
        # Draw each character with a wave effect
        x, y = pos
        for i, char in enumerate(text):
            # Calculate vertical offset using sine wave
            offset = math.sin(t * 3 + i * 0.2) * 5
            
            # Calculate color variation
            r = min(255, base_color[0] + int(math.sin(t + i * 0.1) * 30))
            g = min(255, base_color[1] + int(math.sin(t + i * 0.2) * 30))
            b = min(255, base_color[2] + int(math.sin(t + i * 0.3) * 30))
            
            # Render character
            char_surf = font.render(char, True, (r, g, b))
            
            # Draw shadow
            shadow_surf = font.render(char, True, (0, 0, 0))
            self.screen.blit(shadow_surf, (x + 2, y + 2 + offset))
            
            # Draw character
            self.screen.blit(char_surf, (x, y + offset))
            
            # Move x position for next character
            x += char_surf.get_width()
    
    def update(self):
        """Update all effects"""
        self.update_particles()
        self.update_speed_lines()
    
    def draw_main_menu_effects(self):
        """Draw all effects for main menu"""
        # Draw a gradient background
        self.draw_gradient_background((20, 30, 60), (5, 10, 30))
        
        # Draw animated effects
        self.draw_speed_lines()
        self.draw_particles()
    
    def draw_gradient_background(self, color1, color2):
        """Draw a gradient background"""
        for y in range(self.height):
            # Calculate color for this line
            r = int(color1[0] + (color2[0] - color1[0]) * y / self.height)
            g = int(color1[1] + (color2[1] - color1[1]) * y / self.height)
            b = int(color1[2] + (color2[2] - color1[2]) * y / self.height)
            
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))
