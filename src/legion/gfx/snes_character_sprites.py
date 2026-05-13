from __future__ import annotations

from dataclasses import dataclass

import pygame

from legion.gfx.pixel_sprite import Palette, PixelRows, PixelSprite, rgba


TRANSPARENT = (0, 0, 0, 0)
SPRITE_SCALE = 1

DOWN_FRAME: PixelRows = (
    "........................",
    "........KKKKKKKK........",
    "......KKHHHHHHHHKK......",
    ".....KHHHHHHHHHHHHK.....",
    "....KHHHHHHHHHHHHHHK....",
    "....KHHHSSSSSSSSHHHK....",
    "....KHHSSSSSSSSSSHHK....",
    "...KHSSSEESSSEESSSHK....",
    "...KHSSSEESSSEESSSHK....",
    "...KHSSSSSSSSSSSSSHK....",
    "....KSSSSsSSsSSSSK......",
    ".....KSSSSssssSSK.......",
    "......KKSSSSSSKK........",
    ".......K111111K.........",
    "......K11111111K........",
    ".....K1111111111K.......",
    "....KS1111111111SK......",
    "....KS1122222111SK......",
    ".....K122222221K........",
    "......KK222222KK........",
    ".......KPPPPPPK.........",
    "......KPPPPPPPPK........",
    ".....KPPP....PPPK.......",
    ".....KPP......PPK.......",
    ".....KP........PK.......",
    "....KD..........DK......",
    "....KD..........DK......",
    "....KDD........DDK......",
    ".....KK........KK.......",
    "........................",
    "........................",
    "........................",
)

UP_FRAME: PixelRows = (
    "........................",
    "........KKKKKKKK........",
    "......KKHHHHHHHHKK......",
    ".....KHHHHHHHHHHHHK.....",
    "....KHHHHHHHHHHHHHHK....",
    "....KHHHHHHHHHHHHHHK....",
    "....KHHHHHHHHHHHHHHK....",
    "...KHHHHHHHHHHHHHHHHK...",
    "...KHHHHHHHHHHHHHHHHK...",
    "...KHHHHHHHHHHHHHHHHK...",
    "....KHHHHHHHHHHHHHHK....",
    ".....KHHHHHHHHHHHHK.....",
    "......KKHHHHHHHHKK......",
    ".......K111111K.........",
    "......K11111111K........",
    ".....K1111111111K.......",
    "....KS1111111111SK......",
    "....KS1122222111SK......",
    ".....K122222221K........",
    "......KK222222KK........",
    ".......KPPPPPPK.........",
    "......KPPPPPPPPK........",
    ".....KPPP....PPPK.......",
    ".....KPP......PPK.......",
    ".....KP........PK.......",
    "....KD..........DK......",
    "....KD..........DK......",
    "....KDD........DDK......",
    ".....KK........KK.......",
    "........................",
    "........................",
    "........................",
)

RIGHT_FRAME: PixelRows = (
    "........................",
    ".........KKKKKKK........",
    ".......KKHHHHHHHK.......",
    "......KHHHHHHHHHHK......",
    ".....KHHHHHHHHHHHHK.....",
    ".....KHHHHHSSSSSSHK.....",
    ".....KHHHSSSSSSSSSK.....",
    ".....KHHSSSSSEEESK......",
    ".....KHHSSSSSEEESK......",
    "......KHSSSSSSSSK.......",
    ".......KSSSssssK........",
    "........KSSSSSK.........",
    ".........KKSSK..........",
    ".........K111K..........",
    "........K11111K.........",
    ".......K111111K.........",
    "......KS1111111K........",
    "......KS1122211K........",
    ".......K122222K.........",
    "........K2222K..........",
    "........KPPPPK..........",
    ".......KPPPPPPK.........",
    ".......KPPP..PK.........",
    ".......KPP...PK.........",
    ".......KP....PK.........",
    "......KD.....DK.........",
    "......KD.....DK.........",
    "......KDD....K..........",
    ".......KK...............",
    "........................",
    "........................",
    "........................",
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
    accent: tuple[int, int, int] = (235, 214, 122)
    outline: tuple[int, int, int] = (18, 18, 22)

    def to_palette(self) -> Palette:
        return {
            ".": TRANSPARENT,
            "K": rgba(self.outline),
            "S": rgba(self.skin),
            "s": rgba(self.skin_shadow),
            "E": rgba((18, 18, 22)),
            "H": rgba(self.hair),
            "1": rgba(self.shirt),
            "2": rgba(self.shirt_shadow),
            "P": rgba(self.pants),
            "D": rgba(self.shoe),
            "A": rgba(self.accent),
        }


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
        self.frames: dict[tuple[str, str], pygame.Surface] = {}
        for name, character_palette in CHARACTER_PALETTES.items():
            palette = character_palette.to_palette()
            self.frames[(name, "down")] = self._scaled_surface(DOWN_FRAME, palette)
            self.frames[(name, "up")] = self._scaled_surface(UP_FRAME, palette)
            self.frames[(name, "right")] = self._scaled_surface(RIGHT_FRAME, palette)
            self.frames[(name, "left")] = pygame.transform.flip(self.frames[(name, "right")], True, False)

    def draw(
        self,
        surface: pygame.Surface,
        sprite_key: str,
        facing: str,
        feet_center: tuple[int, int],
        bob: int = 0,
    ) -> None:
        frame = self.frames.get((sprite_key, facing), self.frames[(sprite_key, "down")])
        x = feet_center[0] - frame.get_width() // 2
        y = feet_center[1] - frame.get_height() + bob
        pygame.draw.ellipse(
            surface,
            (4, 5, 6),
            pygame.Rect(feet_center[0] - 14, feet_center[1] - 7, 28, 8),
        )
        surface.blit(frame, (x, y))

    def _scaled_surface(self, rows: PixelRows, palette: Palette) -> pygame.Surface:
        base = PixelSprite(rows, palette).to_surface()
        if SPRITE_SCALE == 1:
            return base
        return pygame.transform.scale_by(base, SPRITE_SCALE)
