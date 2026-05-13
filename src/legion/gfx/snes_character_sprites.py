from __future__ import annotations

from dataclasses import dataclass

import pygame

from legion.gfx.pixel_sprite import Palette, PixelRows, PixelSprite, rgba


TRANSPARENT = (0, 0, 0, 0)

DOWN_FRAME: PixelRows = (
    "................",
    ".....KKKKKK.....",
    "....KHHHHHHK....",
    "...KHHHHHHHHK...",
    "...KHSSSSSSHK...",
    "...KSSSEEESSK...",
    "...KSSSEEESSK...",
    "...KSSSSSSSSK...",
    "....KssssssK....",
    ".....K1111K.....",
    "....K111111K....",
    "...K11111111K...",
    "...K12222211K...",
    "....K222222K....",
    "....K2PPPP2K....",
    ".....KPPPPK.....",
    ".....KPPPPK.....",
    ".....KP..PK.....",
    "....KD....DK....",
    "....KD....DK....",
    "....KK....KK....",
    "................",
    "................",
    "................",
)

UP_FRAME: PixelRows = (
    "................",
    ".....KKKKKK.....",
    "....KHHHHHHK....",
    "...KHHHHHHHHK...",
    "...KHHHHHHHHK...",
    "...KHHHHHHHHK...",
    "...KHHHHHHHHK...",
    "...KHHHHHHHHK...",
    "....KHHHHHHK....",
    ".....K1111K.....",
    "....K111111K....",
    "...K11111111K...",
    "...K12222211K...",
    "....K222222K....",
    "....K2PPPP2K....",
    ".....KPPPPK.....",
    ".....KPPPPK.....",
    ".....KP..PK.....",
    "....KD....DK....",
    "....KD....DK....",
    "....KK....KK....",
    "................",
    "................",
    "................",
)

RIGHT_FRAME: PixelRows = (
    "................",
    ".....KKKKK......",
    "....KHHHHHK.....",
    "...KHHHHHHHK....",
    "...KHHHSSSSK....",
    "...KHHSSSEEK....",
    "...KHHSSSESK....",
    "....KHSSSSK.....",
    ".....KsssK......",
    ".....K111K......",
    "....K11111K.....",
    "...K111111K.....",
    "...K122221K.....",
    "....K2222K......",
    "....K2PP2K......",
    ".....KPPK.......",
    ".....KPPK.......",
    ".....KP.K.......",
    "....KD..K.......",
    "....KD..K.......",
    "....KK..........",
    "................",
    "................",
    "................",
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
        }


CHARACTER_PALETTES: dict[str, CharacterPalette] = {
    "player": CharacterPalette(
        skin=(190, 134, 92),
        skin_shadow=(139, 86, 63),
        hair=(45, 31, 25),
        shirt=(70, 126, 166),
        shirt_shadow=(42, 75, 108),
        pants=(37, 47, 73),
        shoe=(25, 24, 30),
    ),
    "hollis": CharacterPalette(
        skin=(188, 132, 91),
        skin_shadow=(130, 82, 59),
        hair=(92, 87, 75),
        shirt=(138, 88, 58),
        shirt_shadow=(88, 56, 43),
        pants=(55, 59, 65),
        shoe=(31, 30, 29),
    ),
    "mara": CharacterPalette(
        skin=(174, 112, 82),
        skin_shadow=(118, 72, 59),
        hair=(27, 22, 26),
        shirt=(132, 58, 83),
        shirt_shadow=(82, 38, 58),
        pants=(44, 55, 62),
        shoe=(23, 24, 28),
    ),
    "quiet_customer": CharacterPalette(
        skin=(163, 151, 132),
        skin_shadow=(95, 91, 88),
        hair=(16, 17, 21),
        shirt=(74, 82, 96),
        shirt_shadow=(42, 48, 62),
        pants=(32, 36, 45),
        shoe=(18, 18, 22),
        outline=(10, 12, 16),
    ),
    "silas": CharacterPalette(
        skin=(180, 126, 84),
        skin_shadow=(117, 73, 51),
        hair=(62, 43, 30),
        shirt=(84, 101, 76),
        shirt_shadow=(52, 64, 49),
        pants=(48, 43, 40),
        shoe=(26, 24, 24),
    ),
}


class CharacterSpriteLibrary:
    def __init__(self) -> None:
        self.frames: dict[tuple[str, str], pygame.Surface] = {}
        for name, character_palette in CHARACTER_PALETTES.items():
            palette = character_palette.to_palette()
            self.frames[(name, "down")] = PixelSprite(DOWN_FRAME, palette).to_surface()
            self.frames[(name, "up")] = PixelSprite(UP_FRAME, palette).to_surface()
            self.frames[(name, "right")] = PixelSprite(RIGHT_FRAME, palette).to_surface()
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
            pygame.Rect(feet_center[0] - 7, feet_center[1] - 4, 14, 5),
        )
        surface.blit(frame, (x, y))
