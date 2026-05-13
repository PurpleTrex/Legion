from __future__ import annotations

from dataclasses import dataclass

import pygame


PixelRows = tuple[str, ...]
Palette = dict[str, tuple[int, int, int, int]]


@dataclass(frozen=True)
class PixelSprite:
    rows: PixelRows
    palette: Palette

    def __post_init__(self) -> None:
        if not self.rows:
            raise ValueError("pixel sprite must contain rows")

        width = len(self.rows[0])
        if width == 0:
            raise ValueError("pixel sprite rows must not be empty")

        for row in self.rows:
            if len(row) != width:
                raise ValueError("all pixel sprite rows must have the same width")

            missing = {char for char in row if char not in self.palette}
            if missing:
                missing_chars = ", ".join(sorted(missing))
                raise ValueError(f"pixel sprite uses undefined palette entries: {missing_chars}")

    @property
    def width(self) -> int:
        return len(self.rows[0])

    @property
    def height(self) -> int:
        return len(self.rows)

    def to_surface(self) -> pygame.Surface:
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for y, row in enumerate(self.rows):
            for x, char in enumerate(row):
                surface.set_at((x, y), self.palette[char])
        return surface


def rgba(color: tuple[int, int, int]) -> tuple[int, int, int, int]:
    return (*color, 255)
