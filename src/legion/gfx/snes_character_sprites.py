from __future__ import annotations

from dataclasses import dataclass

import pygame


SPRITE_WIDTH = 24
SPRITE_HEIGHT = 32
WALK_FRAME_COUNT = 2


@dataclass(frozen=True)
class CharacterPalette:
    skin: tuple[int, int, int]
    skin_shadow: tuple[int, int, int]
    hair: tuple[int, int, int]
    shirt: tuple[int, int, int]
    shirt_shadow: tuple[int, int, int]
    pants: tuple[int, int, int]
    shoe: tuple[int, int, int]
    outline: tuple[int, int, int] = (18, 18, 22)


CHARACTER_PALETTES: dict[str, CharacterPalette] = {
    "player": CharacterPalette(
        skin=(198, 145, 98),
        skin_shadow=(142, 92, 66),
        hair=(42, 29, 24),
        shirt=(64, 126, 178),
        shirt_shadow=(35, 76, 120),
        pants=(34, 46, 78),
        shoe=(21, 22, 29),
    ),
    "hollis": CharacterPalette(
        skin=(190, 138, 94),
        skin_shadow=(132, 86, 61),
        hair=(97, 92, 78),
        shirt=(146, 91, 58),
        shirt_shadow=(89, 57, 42),
        pants=(58, 61, 67),
        shoe=(28, 28, 27),
    ),
    "mara": CharacterPalette(
        skin=(178, 117, 84),
        skin_shadow=(122, 76, 60),
        hair=(27, 22, 27),
        shirt=(145, 57, 91),
        shirt_shadow=(86, 34, 62),
        pants=(44, 58, 67),
        shoe=(22, 23, 28),
    ),
    "quiet_customer": CharacterPalette(
        skin=(166, 154, 132),
        skin_shadow=(96, 91, 86),
        hair=(14, 15, 20),
        shirt=(78, 87, 105),
        shirt_shadow=(42, 49, 66),
        pants=(31, 36, 48),
        shoe=(16, 17, 22),
        outline=(9, 10, 14),
    ),
    "silas": CharacterPalette(
        skin=(184, 130, 86),
        skin_shadow=(120, 76, 52),
        hair=(64, 43, 29),
        shirt=(88, 108, 78),
        shirt_shadow=(52, 66, 48),
        pants=(51, 45, 40),
        shoe=(25, 23, 23),
    ),
}


class CharacterSpriteLibrary:
    def __init__(self) -> None:
        self.frames: dict[tuple[str, str, int], pygame.Surface] = {}
        for name, palette in CHARACTER_PALETTES.items():
            for phase in range(WALK_FRAME_COUNT + 1):
                self.frames[(name, "down", phase)] = self._make_down_frame(palette, phase)
                self.frames[(name, "up", phase)] = self._make_up_frame(palette, phase)
                self.frames[(name, "right", phase)] = self._make_side_frame(palette, phase)
                self.frames[(name, "left", phase)] = pygame.transform.flip(
                    self.frames[(name, "right", phase)], True, False
                )

    def draw(
        self,
        surface: pygame.Surface,
        sprite_key: str,
        facing: str,
        feet_center: tuple[int, int],
        walk_frame: int = 0,
    ) -> None:
        frame = self.frames.get((sprite_key, facing, walk_frame), self.frames[(sprite_key, "down", 0)])
        x = feet_center[0] - frame.get_width() // 2
        y = feet_center[1] - frame.get_height()
        pygame.draw.ellipse(surface, (6, 7, 8), pygame.Rect(feet_center[0] - 8, feet_center[1] - 3, 16, 4))
        surface.blit(frame, (x, y))

    def _new_surface(self) -> pygame.Surface:
        return pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT), pygame.SRCALPHA)

    def _make_down_frame(self, palette: CharacterPalette, phase: int) -> pygame.Surface:
        surface = self._new_surface()
        left_step = -1 if phase == 1 else 0
        right_step = -1 if phase == 2 else 0
        arm_swing = 1 if phase == 1 else -1 if phase == 2 else 0

        self._draw_head_front(surface, palette, 0)
        self._draw_body_front(surface, palette)

        self._rect(surface, palette.outline, 4, 16 - arm_swing, 4, 9)
        self._rect(surface, palette.skin, 5, 17 - arm_swing, 2, 6)
        self._rect(surface, palette.outline, 17, 16 + arm_swing, 4, 9)
        self._rect(surface, palette.skin, 18, 17 + arm_swing, 2, 6)

        self._rect(surface, palette.outline, 7, 23 + left_step, 5, 8)
        self._rect(surface, palette.pants, 8, 23 + left_step, 3, 6)
        self._rect(surface, palette.outline, 12, 23 + right_step, 5, 8)
        self._rect(surface, palette.pants, 13, 23 + right_step, 3, 6)
        self._rect(surface, palette.shoe, 6, 29, 6, 3)
        self._rect(surface, palette.shoe, 13, 29, 6, 3)
        return surface

    def _make_up_frame(self, palette: CharacterPalette, phase: int) -> pygame.Surface:
        surface = self._new_surface()
        left_step = -1 if phase == 1 else 0
        right_step = -1 if phase == 2 else 0
        arm_swing = 1 if phase == 1 else -1 if phase == 2 else 0

        self._draw_head_back(surface, palette)
        self._draw_body_front(surface, palette)
        self._rect(surface, palette.outline, 4, 16 + arm_swing, 4, 9)
        self._rect(surface, palette.skin_shadow, 5, 17 + arm_swing, 2, 6)
        self._rect(surface, palette.outline, 17, 16 - arm_swing, 4, 9)
        self._rect(surface, palette.skin_shadow, 18, 17 - arm_swing, 2, 6)
        self._rect(surface, palette.outline, 7, 23 + left_step, 5, 8)
        self._rect(surface, palette.pants, 8, 23 + left_step, 3, 6)
        self._rect(surface, palette.outline, 12, 23 + right_step, 5, 8)
        self._rect(surface, palette.pants, 13, 23 + right_step, 3, 6)
        self._rect(surface, palette.shoe, 6, 29, 6, 3)
        self._rect(surface, palette.shoe, 13, 29, 6, 3)
        return surface

    def _make_side_frame(self, palette: CharacterPalette, phase: int) -> pygame.Surface:
        surface = self._new_surface()
        step = 1 if phase == 1 else -1 if phase == 2 else 0

        self._draw_head_side(surface, palette)
        self._rect(surface, palette.outline, 8, 14, 10, 11)
        self._rect(surface, palette.shirt, 9, 15, 8, 7)
        self._rect(surface, palette.shirt_shadow, 10, 21, 7, 3)
        self._rect(surface, palette.outline, 6, 16 - step, 4, 8)
        self._rect(surface, palette.skin, 7, 17 - step, 2, 5)
        self._rect(surface, palette.outline, 16, 16 + step, 4, 8)
        self._rect(surface, palette.skin_shadow, 17, 17 + step, 2, 5)

        self._rect(surface, palette.outline, 9, 23 + step, 5, 8)
        self._rect(surface, palette.pants, 10, 23 + step, 3, 6)
        self._rect(surface, palette.outline, 14, 23 - step, 5, 8)
        self._rect(surface, palette.pants, 15, 23 - step, 3, 6)
        self._rect(surface, palette.shoe, 8 + step, 29, 6, 3)
        self._rect(surface, palette.shoe, 14 - step, 29, 6, 3)
        return surface

    def _draw_head_front(self, surface: pygame.Surface, palette: CharacterPalette, y_offset: int) -> None:
        self._rect(surface, palette.outline, 6, 2 + y_offset, 12, 12)
        self._rect(surface, palette.skin, 7, 5 + y_offset, 10, 8)
        self._rect(surface, palette.skin_shadow, 8, 12 + y_offset, 8, 1)
        self._rect(surface, palette.hair, 7, 2 + y_offset, 10, 4)
        self._rect(surface, palette.hair, 6, 5 + y_offset, 2, 4)
        self._rect(surface, palette.hair, 16, 5 + y_offset, 2, 3)
        self._rect(surface, palette.outline, 9, 8 + y_offset, 2, 2)
        self._rect(surface, palette.outline, 14, 8 + y_offset, 2, 2)
        self._rect(surface, palette.skin_shadow, 11, 10 + y_offset, 3, 1)
        self._rect(surface, palette.outline, 11, 12 + y_offset, 4, 1)

    def _draw_head_back(self, surface: pygame.Surface, palette: CharacterPalette) -> None:
        self._rect(surface, palette.outline, 6, 2, 12, 12)
        self._rect(surface, palette.hair, 7, 3, 10, 10)
        self._rect(surface, palette.outline, 8, 2, 8, 2)
        self._rect(surface, palette.hair, 6, 6, 2, 5)
        self._rect(surface, palette.hair, 16, 6, 2, 5)

    def _draw_head_side(self, surface: pygame.Surface, palette: CharacterPalette) -> None:
        self._rect(surface, palette.outline, 6, 2, 12, 12)
        self._rect(surface, palette.skin, 8, 5, 9, 8)
        self._rect(surface, palette.skin, 17, 7, 2, 3)
        self._rect(surface, palette.skin_shadow, 12, 12, 5, 1)
        self._rect(surface, palette.hair, 6, 2, 11, 5)
        self._rect(surface, palette.hair, 6, 6, 3, 5)
        self._rect(surface, palette.outline, 15, 8, 2, 2)
        self._rect(surface, palette.outline, 16, 12, 3, 1)

    def _draw_body_front(self, surface: pygame.Surface, palette: CharacterPalette) -> None:
        self._rect(surface, palette.outline, 7, 14, 10, 11)
        self._rect(surface, palette.shirt, 8, 15, 8, 7)
        self._rect(surface, palette.shirt_shadow, 8, 21, 8, 3)
        self._rect(surface, palette.outline, 10, 15, 4, 1)

    def _rect(
        self,
        surface: pygame.Surface,
        color: tuple[int, int, int],
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        pygame.draw.rect(surface, color, pygame.Rect(x, y, width, height))
