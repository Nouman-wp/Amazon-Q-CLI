"""
Settings module for SpeedRunner X.
Contains game constants and configuration.
"""

# Game window settings
TITLE = "SpeedRunner X"
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILE_SIZE = 32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
TRANSPARENT = (0, 0, 0, 128)

# Player settings
PLAYER_SPEED = 8
PLAYER_JUMP_STRENGTH = 16
PLAYER_GRAVITY = 0.8
PLAYER_FRICTION = 0.12
PLAYER_ACCELERATION = 0.5
PLAYER_WALL_SLIDE_SPEED = 2
PLAYER_WALL_JUMP_STRENGTH = 12
PLAYER_START_LIVES = 3

# Enemy settings
ENEMY_SPEED = 2

# Power-up settings
SPEED_BOOST_MULTIPLIER = 1.5
SPEED_BOOST_DURATION = 5000  # milliseconds
SLOW_TIME_FACTOR = 0.5
SLOW_TIME_DURATION = 3000  # milliseconds
INVINCIBILITY_DURATION = 5000  # milliseconds

# Physics settings
GRAVITY = 0.8
TERMINAL_VELOCITY = 20

# Game states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_GAME_OVER = 3
STATE_VICTORY = 4
STATE_LEADERBOARD = 5

# File paths
LEADERBOARD_PATH = "data/leaderboard.json"
GHOST_RUNS_PATH = "data/ghost_runs/"
MAPS_PATH = "assets/maps/"
IMAGES_PATH = "assets/images/"
AUDIO_PATH = "assets/audio/"

# Level settings
LEVEL_COUNT = 2  # Number of levels in the game
