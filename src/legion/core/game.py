from __future__ import annotations

import pygame

from legion.core.config import GameConfig
from legion.core.events import ChangeScene, QuitGame
from legion.scenes.boot_scene import BootScene
from legion.scenes.market_scene import MarketScene
from legion.scenes.scene import Scene


class Game:
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.screen = pygame.display.set_mode(config.window_size)
        self.surface = pygame.Surface((config.logical_width, config.logical_height))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption(config.title)

        self.scenes: dict[str, Scene] = {
            "boot": BootScene(config),
            "market": MarketScene(config),
        }
        self.current_scene: Scene = self.scenes["boot"]

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(self.config.target_fps) / 1000.0
            pygame_events = pygame.event.get()
            for event in pygame_events:
                if event.type == pygame.QUIT:
                    self.running = False

            scene_events = self.current_scene.handle_events(pygame_events)
            self._handle_scene_events(scene_events)

            self.current_scene.update(dt)
            self.surface.fill(self.config.background_color)
            self.current_scene.draw(self.surface)
            self._present()

    def _handle_scene_events(self, scene_events: list[object]) -> None:
        for event in scene_events:
            if isinstance(event, QuitGame):
                self.running = False
            elif isinstance(event, ChangeScene):
                self.current_scene = self.scenes[event.scene_name]

    def _present(self) -> None:
        scaled = pygame.transform.scale(self.surface, self.config.window_size)
        self.screen.blit(scaled, (0, 0))
        pygame.display.flip()
