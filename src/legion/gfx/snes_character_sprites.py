from __future__ import annotations

from dataclasses import dataclass

import pygame

from legion.gfx.pixel_sprite import Palette, PixelRows, PixelSprite, rgba


SPRITE_WIDTH = 16
SPRITE_HEIGHT = 24
RENDER_SCALE = 2
WALK_FRAME_COUNT = 2
TRANSPARENT = (0, 0, 0, 0)

FRONT_IDLE: PixelRows = (
    "................",
    "....OOOOOOOO....",
    "...OHHHHHHHHO...",
    "..OHHHHHHHHHHO..",
    "..OHHSSSSSSHHO..",
    ".OHSSSSSSSSSHO..",
    ".OSSESSSSESSSO..",
    ".OSSSSSSSSSSSO..",
    "..OSSSSSSSSSO...",
    "...OOSSMMSSOO...",
    ".....OOOOOO.....",
    "....OO1111OO....",
    "...O11111111O...",
    "..OA111AA111AO..",
    "..OA11222211AO..",
    "...O22222222O...",
    "....OO2222OO....",
    ".....O3333O.....",
    "....O33OO33O....",
    "....O3O..O3O....",
    "....O3O..O3O....",
    "...O44O..O44O...",
    "...O44O..O44O...",
    "....OO....OO....",
)

FRONT_WALK_LEFT: PixelRows = (
    "................",
    "....OOOOOOOO....",
    "...OHHHHHHHHO...",
    "..OHHHHHHHHHHO..",
    "..OHHSSSSSSHHO..",
    ".OHSSSSSSSSSHO..",
    ".OSSESSSSESSSO..",
    ".OSSSSSSSSSSSO..",
    "..OSSSSSSSSSO...",
    "...OOSSMMSSOO...",
    ".....OOOOOO.....",
    "....OO1111OO....",
    "...O11111111O...",
    "..OA111AA111O...",
    ".OA111222211AO..",
    "...O22222222O...",
    "....OO2222OO....",
    "....O33333O.....",
    "...O33OO33O.....",
    "...O3O...O3O....",
    "...O3O...O3O....",
    "..O44O...O44O...",
    "..O44O...O44O...",
    "...OO.....OO....",
)

FRONT_WALK_RIGHT: PixelRows = (
    "................",
    "....OOOOOOOO....",
    "...OHHHHHHHHO...",
    "..OHHHHHHHHHHO..",
    "..OHHSSSSSSHHO..",
    ".OHSSSSSSSSSHO..",
    ".OSSESSSSESSSO..",
    ".OSSSSSSSSSSSO..",
    "..OSSSSSSSSSO...",
    "...OOSSMMSSOO...",
    ".....OOOOOO.....",
    "....OO1111OO....",
    "...O11111111O...",
    "...O111AA111AO..",
    "..OA112222111AO.",
    "...O22222222O...",
    "....OO2222OO....",
    ".....O33333O....",
    ".....O3O..O3O...",
    "....O3O...O3O...",
    "....O3O...O3O...",
    "...O44O...O44O..",
    "...O44O...O44O..",
    "....OO.....OO...",
)

BACK_IDLE: PixelRows = (
    "................",
    "....OOOOOOOO....",
    "...OHHHHHHHHO...",
    "..OHHHHHHHHHHO..",
    "..OHHHHHHHHHHO..",
    ".OHHHHHHHHHHHHO.",
    ".OHHHHHHHHHHHHO.",
    ".OHHHHHHHHHHHHO.",
    "..OHHHHHHHHHHO..",
    "...OOHHHHHHOO...",
    ".....OOOOOO.....",
    "....OO1111OO....",
    "...O11111111O...",
    "..OA111AA111AO..",
    "..OA11222211AO..",
    "...O22222222O...",
    "....OO2222OO....",
    ".....O3333O.....",
    "....O33OO33O....",
    "....O3O..O3O....",
    "....O3O..O3O....",
    "...O44O..O44O...",
    "...O44O..O44O...",
    "....OO....OO....",
)

SIDE_IDLE: PixelRows = (
    "................",
    ".....OOOOOO.....",
    "...OOHHHHHHO....",
    "..OHHHHHHHHHO...",
    "..OHHHSSSSSHO...",
    ".OHHSSSSSSSSO...",
    ".OHSSSSSSEEO....",
    ".OHSSSSSSSSO....",
    "..OHSSMMMOO.....",
    "...OOSSSO.......",
    ".....OOOO.......",
    ".....O111O......",
    "....O11111O.....",
    "...OA11111O.....",
    "...OA12221O.....",
    "....O2222O......",
    ".....O33O.......",
    "....O3333O......",
    "....O33O3O......",
    "....O3O.O3O.....",
    "....O3O..O3O....",
    "...O44O..O44O...",
    "...O44O..O44O...",
    "....OO....OO....",
)

SIDE_WALK_A: PixelRows = (
    "................",
    ".....OOOOOO.....",
    "...OOHHHHHHO....",
    "..OHHHHHHHHHO...",
    "..OHHHSSSSSHO...",
    ".OHHSSSSSSSSO...",
    ".OHSSSSSSEEO....",
    ".OHSSSSSSSSO....",
    "..OHSSMMMOO.....",
    "...OOSSSO.......",
    ".....OOOO.......",
    ".....O111O......",
    "....O11111O.....",
    "...OA11111O.....",
    "...OA12221O.....",
    "....O2222O......",
    ".....O33O.......",
    "....O3333O......",
    "...O33O3O.......",
    "..O33O.O3O......",
    "..O3O...O3O.....",
    ".O44O...O44O....",
    ".O44O...O44O....",
    "..OO.....OO.....",
)

SIDE_WALK_B: PixelRows = (
    "................",
    ".....OOOOOO.....",
    "...OOHHHHHHO....",
    "..OHHHHHHHHHO...",
    "..OHHHSSSSSHO...",
    ".OHHSSSSSSSSO...",
    ".OHSSSSSSEEO....",
    ".OHSSSSSSSSO....",
    "..OHSSMMMOO.....",
    "...OOSSSO.......",
    ".....OOOO.......",
    ".....O111O......",
    "....O11111O.....",
    "...OA11111O.....",
    "...OA12221O.....",
    "....O2222O......",
    ".....O33O.......",
    "....O3333O......",
    "......O33O3O....",
    ".....O33O.O3O...",
    "....O3O...O3O...",
    "...O44O...O44O..",
    "...O44O...O44O..",
    "....OO.....OO...",
)


@dataclass(frozen=True)
class CharacterPalette:
    skin: tuple[int, int, int]
    skin_shadow: tuple[int, int, int]
    hair: tuple[int, int, int]
    shirt: tuple[int, int, int]
    shirt_shadow: tuple[int, int, int]
    pants: tuple[int, int, int]
    shoe: tuple[int, int, int]
    accent: tuple[int, int, int] = (229, 198, 91)
    outline: tuple[int, int, int] = (18, 18, 22)

    def to_pixel_palette(self) -> Palette:
        return {
            ".": TRANSPARENT,
            "O": rgba(self.outline),
            "H": rgba(self.hair),
            "S": rgba(self.skin),
            "M": rgba(self.skin_shadow),
            "E": rgba((14, 16, 20)),
            "1": rgba(self.shirt),
            "2": rgba(self.shirt_shadow),
            "3": rgba(self.pants),
            "4": rgba(self.shoe),
            "A": rgba(self.accent),
        }


CHARACTER_PALETTES: dict[str, CharacterPalette] = {
    "player": CharacterPalette(
        skin=(214, 154, 92),
        skin_shadow=(150, 91, 58),
        hair=(73, 44, 24),
        shirt=(61, 132, 205),
        shirt_shadow=(35, 79, 139),
        pants=(38, 55, 97),
        shoe=(20, 21, 28),
    ),
    "hollis": CharacterPalette(
        skin=(194, 135, 87),
        skin_shadow=(117, 70, 48),
        hair=(82, 78, 65),
        shirt=(156, 90, 54),
        shirt_shadow=(89, 53, 40),
        pants=(58, 58, 64),
        shoe=(22, 22, 24),
    ),
    "mara": CharacterPalette(
        skin=(179, 115, 78),
        skin_shadow=(121, 70, 54),
        hair=(30, 22, 29),
        shirt=(153, 61, 98),
        shirt_shadow=(91, 36, 68),
        pants=(44, 62, 74),
        shoe=(20, 22, 27),
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
            self.frames[(name, "down", 0)] = self._make_frame(FRONT_IDLE, palette)
            self.frames[(name, "down", 1)] = self._make_frame(FRONT_WALK_LEFT, palette)
            self.frames[(name, "down", 2)] = self._make_frame(FRONT_WALK_RIGHT, palette)
            self.frames[(name, "up", 0)] = self._make_frame(BACK_IDLE, palette)
            self.frames[(name, "up", 1)] = self._make_frame(BACK_IDLE, palette)
            self.frames[(name, "up", 2)] = self._make_frame(BACK_IDLE, palette)
            self.frames[(name, "right", 0)] = self._make_frame(SIDE_IDLE, palette)
            self.frames[(name, "right", 1)] = self._make_frame(SIDE_WALK_A, palette)
            self.frames[(name, "right", 2)] = self._make_frame(SIDE_WALK_B, palette)
            self.frames[(name, "left", 0)] = pygame.transform.flip(self.frames[(name, "right", 0)], True, False)
            self.frames[(name, "left", 1)] = pygame.transform.flip(self.frames[(name, "right", 1)], True, False)
            self.frames[(name, "left", 2)] = pygame.transform.flip(self.frames[(name, "right", 2)], True, False)

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
        pygame.draw.ellipse(surface, (6, 7, 8), pygame.Rect(feet_center[0] - 10, feet_center[1] - 4, 20, 5))
        surface.blit(frame, (x, y))

    def _make_frame(self, rows: PixelRows, palette: CharacterPalette) -> pygame.Surface:
        base = PixelSprite(rows, palette.to_pixel_palette()).to_surface()
        return pygame.transform.scale_by(base, RENDER_SCALE)
