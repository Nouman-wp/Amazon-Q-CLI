# SpeedRunner X

A 2D single-player speedrunning platformer game built with Python and Pygame.

## Game Description

SpeedRunner X is a fast-paced platformer focused on competitive time-based levels. Players control a character who must navigate through challenging levels as quickly as possible, with their best runs saved as ghost replays to compete against.

## Features

- Pixel-art graphics and smooth platforming mechanics
- Time trial gameplay with persistent leaderboards
- Ghost replay system showing your best runs
- Multiple levels with increasing difficulty
- Power-ups and hazards to navigate
- Wall-sliding, enemy bouncing, and other advanced movement mechanics

## Installation

1. Ensure you have Python 3.8+ installed
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the game:
   ```
   python run_game.py
   ```
   
   Or directly:
   ```
   python src/main.py
   ```

## Controls

- Arrow keys: Move left/right
- Space: Jump
- Escape: Pause game
- R: Restart level

## Development

This game was created using:
- Python 3.8+
- Pygame for rendering and game logic
- PyTMX for loading Tiled map files (optional)
- Pygame-menu for UI elements

## Folder Structure

- `assets/`: Contains all game assets (images, audio, maps)
- `data/`: Stores leaderboard and ghost run data
- `src/`: Source code for the game
