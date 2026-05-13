from __future__ import annotations

import pygame


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue

        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_panel(
    surface: pygame.Surface,
    rect: pygame.Rect,
    fill: tuple[int, int, int] = (18, 20, 28),
    border: tuple[int, int, int] = (196, 206, 188),
) -> None:
    pygame.draw.rect(surface, (4, 5, 8), rect.move(2, 2))
    pygame.draw.rect(surface, fill, rect)
    pygame.draw.rect(surface, border, rect, 1)
    pygame.draw.rect(surface, (76, 86, 78), rect.inflate(-4, -4), 1)
