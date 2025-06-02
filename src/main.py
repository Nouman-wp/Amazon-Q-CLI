"""
Main module for SpeedRunner X.
Entry point for the game.
"""
import pygame
import sys
import os

# Add the parent directory to the path so we can import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

def main():
    """Main function to start the game"""
    # Initialize pygame
    pygame.init()
    
    # Import here to avoid circular imports
    from src.game import Game
    
    # Create and run the game
    print("Creating game instance...")
    game = Game()
    print("Starting game loop...")
    game.run()

if __name__ == "__main__":
    main()
