#!/usr/bin/env python3
"""
Launcher script for SpeedRunner X.
"""
import os
import sys

if __name__ == "__main__":
    # Change working directory to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory set to: {script_dir}")
    
    # Add the current directory to the path
    sys.path.insert(0, script_dir)
    
    # Import and run the game
    from src.main import main
    main()
