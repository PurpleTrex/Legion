from __future__ import annotations

import pygame

from legion.core.config import GameConfig
from legion.core.events import ChangeScene, QuitGame
from legion.scenes.scene import Scene


class BootScene(Scene):
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.elapsed = 0.0
        self.title_font = pygame.font.Font(None, 32)
        self.body_font = pygame.font.Font(None, 12)
        self.small_font = pygame.font.Font(None, 10)

    def handle_events(self, events: list[pygame.event.Event]) -> list[object]:
        scene_events: list[object] = []
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in {pygame.K_ESCAPE, pygame.K_q}:
                scene_events.append(QuitGame())
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                scene_events.append(ChangeScene("market"))
        return scene_events

    def update(self, dt: float) -> None:
        self.elapsed += dt

    def draw(self, surface: pygame.Surface) -> None:
        width, height = surface.get_size()
        self._draw_scanline_background(surface)
        self._draw_title(surface, width)
        self._draw_status(surface, width, height)

    def _draw_scanline_background(self, surface: pygame.Surface) -> None:
        for y in range(0, self.config.logical_height, 2):
            color = (14, 16, 24) if y % 4 == 0 else (10, 11, 16)
            pygame.draw.line(surface, color, (0, y), (self.config.logical_width, y))

        glow = 18 + int((pygame.math.Vector2(1, 0).rotate(self.elapsed * 80).x + 1) * 10)
        pygame.draw.rect(surface, (glow, 34, 30), pygame.Rect(0, 126, self.config.logical_width, 54))
        pygame.draw.rect(surface, (42, 60, 52), pygame.Rect(0, 124, self.config.logical_width, 2))

    def _draw_title(self, surface: pygame.Surface, width: int) -> None:
        title = self.title_font.render("LEGION", False, (226, 232, 220))
        subtitle = self.body_font.render("pygame project scaffold", False, (156, 166, 154))
        surface.blit(title, title.get_rect(center=(width // 2, 62)))
        surface.blit(subtitle, subtitle.get_rect(center=(width // 2, 84)))

    def _draw_status(self, surface: pygame.Surface, width: int, height: int) -> None:
        lines = [
            "Press Space to start Scene 01",
            "Press Esc or Q to quit",
        ]
        for index, line in enumerate(lines):
            rendered = self.small_font.render(line, False, (190, 198, 184))
            surface.blit(rendered, rendered.get_rect(center=(width // 2, height - 30 + index * 12)))
