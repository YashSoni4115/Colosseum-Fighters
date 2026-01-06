"""Game-wide constants and configuration."""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

# Window
WIDTH = 1224
HEIGHT = 544
FPS = 60
CAPTION = "Colosseum Fighters"

# Player properties
PLAYER_W = 100
PLAYER_H = 175
SPEED = 10
STARTING_HEALTH = 100

PLAYER_1_START_X = 200
PLAYER_1_START_Y = 325
PLAYER_2_START_X = 900
PLAYER_2_START_Y = PLAYER_1_START_Y

GROUND_HEIGHT = PLAYER_1_START_Y + PLAYER_H

# Colors (RGB)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Assets location
# Adjust this to match your folder structure.
# Example:
#   project/
#     main.py
#     assets/
#       Colosseum Fighters Assets/
#         ...
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
