from __future__ import annotations

import pygame

from legion.core.config import GameConfig
from legion.core.game import Game


def main() -> int:
    config = GameConfig()
    pygame.init()
    try:
        game = Game(config)
        game.run()
    finally:
        pygame.quit()
    return 0
