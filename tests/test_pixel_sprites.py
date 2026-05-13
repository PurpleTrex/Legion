import pygame
import pytest

from legion.gfx.pixel_sprite import PixelSprite, rgba
from legion.gfx.snes_character_sprites import (
    CHARACTER_PALETTES,
    DOWN_FRAME,
    SPRITE_SCALE,
    CharacterSpriteLibrary,
)


def test_pixel_sprite_requires_consistent_row_width() -> None:
    palette = {".": (0, 0, 0, 0), "K": rgba((1, 2, 3))}

    with pytest.raises(ValueError, match="same width"):
        PixelSprite(("..", "..."), palette)


def test_character_down_frame_is_24_by_32() -> None:
    sprite = PixelSprite(DOWN_FRAME, CHARACTER_PALETTES["player"].to_palette())

    assert sprite.width == 24
    assert sprite.height == 32


def test_character_sprite_renders_to_alpha_surface() -> None:
    pygame.init()
    try:
        sprite = PixelSprite(DOWN_FRAME, CHARACTER_PALETTES["player"].to_palette())
        surface = sprite.to_surface()
    finally:
        pygame.quit()

    assert surface.get_size() == (24, 32)
    assert surface.get_at((0, 0)).a == 0


def test_character_library_scales_sprites_for_readable_details() -> None:
    pygame.init()
    try:
        library = CharacterSpriteLibrary()
        frame = library.frames[("player", "down")]
    finally:
        pygame.quit()

    assert frame.get_size() == (24 * SPRITE_SCALE, 32 * SPRITE_SCALE)
