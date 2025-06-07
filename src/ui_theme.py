"""
UI Theme module for SpeedRunner X.
Contains theme definitions for game menus.
"""
import pygame
import pygame_menu

def create_speedrunner_theme():
    """Create a modern theme for SpeedRunner X menus"""
    theme = pygame_menu.themes.Theme()
    
    # Colors that match the game's speed/action theme
    # Deep blue background with orange/yellow accents
    theme.background_color = (15, 25, 35, 220)  # Dark blue with transparency
    theme.title_background_color = (30, 50, 80, 255)
    theme.title_font_color = (255, 165, 0)  # Orange
    theme.widget_font_color = (220, 220, 255)  # Light blue-white
    
    # Font settings
    theme.title_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
    theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
    theme.title_font_size = 60
    theme.widget_font_size = 36
    
    # Widget styling
    theme.selection_color = (255, 140, 0)  # Bright orange for selection
    theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER
    theme.widget_margin = (0, 14)
    theme.widget_padding = 10
    
    # Effects
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
    theme.title_font_shadow = True
    theme.title_font_shadow_color = (0, 0, 0)
    theme.title_font_shadow_offset = 2
    theme.widget_font_shadow = True
    theme.widget_font_shadow_color = (0, 0, 0)
    theme.widget_font_shadow_offset = 2
    
    # Fix for pygame-menu 4.4.3
    theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()
    
    return theme

def create_pause_theme():
    """Create a theme for the pause menu"""
    theme = pygame_menu.themes.Theme()
    
    # Semi-transparent dark blue with light accents
    theme.background_color = (10, 20, 40, 200)
    theme.title_background_color = (30, 60, 100, 230)
    theme.title_font_color = (220, 220, 255)
    theme.widget_font_color = (220, 220, 255)
    
    # Font settings
    theme.title_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
    theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
    theme.title_font_size = 48
    theme.widget_font_size = 36
    
    # Widget styling
    theme.selection_color = (0, 150, 255)
    theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER
    theme.widget_margin = (0, 10)
    theme.widget_padding = 8
    
    # Effects
    theme.title_font_shadow = True
    theme.widget_font_shadow = True
    
    # Fix for pygame-menu 4.4.3
    theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()
    
    return theme

def create_game_over_theme():
    """Create a theme for the game over menu"""
    theme = pygame_menu.themes.Theme()
    
    # Red-tinted dark background
    theme.background_color = (40, 10, 10, 220)
    theme.title_background_color = (120, 20, 20, 255)
    theme.title_font_color = (255, 200, 200)
    theme.widget_font_color = (255, 220, 220)
    
    # Font settings
    theme.title_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
    theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
    theme.title_font_size = 55
    theme.widget_font_size = 36
    
    # Widget styling
    theme.selection_color = (255, 100, 100)
    theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER
    theme.widget_margin = (0, 12)
    theme.widget_padding = 10
    
    # Effects
    theme.title_font_shadow = True
    theme.widget_font_shadow = True
    
    # Fix for pygame-menu 4.4.3
    theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()
    
    return theme

def create_victory_theme():
    """Create a theme for the victory menu"""
    theme = pygame_menu.themes.Theme()
    
    # Green-tinted background
    theme.background_color = (10, 40, 20, 220)
    theme.title_background_color = (20, 80, 40, 255)
    theme.title_font_color = (220, 255, 220)
    theme.widget_font_color = (220, 255, 220)
    
    # Font settings
    theme.title_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
    theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
    theme.title_font_size = 55
    theme.widget_font_size = 36
    
    # Widget styling
    theme.selection_color = (100, 255, 100)
    theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER
    theme.widget_margin = (0, 12)
    theme.widget_padding = 10
    
    # Effects
    theme.title_font_shadow = True
    theme.widget_font_shadow = True
    
    # Fix for pygame-menu 4.4.3
    theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()
    
    return theme
