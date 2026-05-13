import pygame
import pytest

from legion.gfx.pixel_sprite import PixelSprite, rgba
from legion.gfx.snes_character_sprites import (
    FRONT_IDLE,
    CharacterSpriteLibrary,
    RENDER_SCALE,
    SPRITE_HEIGHT,
    SPRITE_WIDTH,
    WALK_FRAME_COUNT,
)


def test_pixel_sprite_requires_consistent_row_width() -> None:
    palette = {".": (0, 0, 0, 0), "K": rgba((1, 2, 3))}

    with pytest.raises(ValueError, match="same width"):
        PixelSprite(("..", "..."), palette)


def test_character_library_builds_idle_and_walk_frames() -> None:
    pygame.init()
    try:
        library = CharacterSpriteLibrary()
    finally:
        pygame.quit()

    expected_size = (SPRITE_WIDTH * RENDER_SCALE, SPRITE_HEIGHT * RENDER_SCALE)

    assert library.frames[("player", "down", 0)].get_size() == expected_size
    assert library.frames[("player", "down", 1)].get_size() == expected_size
    assert library.frames[("player", "down", 2)].get_size() == expected_size
    assert WALK_FRAME_COUNT == 2


def test_hand_authored_player_frame_uses_chibi_base_size() -> None:
    sprite = PixelSprite(FRONT_IDLE, {
        ".": (0, 0, 0, 0),
        "O": rgba((1, 1, 1)),
        "H": rgba((1, 1, 1)),
        "S": rgba((1, 1, 1)),
        "M": rgba((1, 1, 1)),
        "E": rgba((1, 1, 1)),
        "1": rgba((1, 1, 1)),
        "2": rgba((1, 1, 1)),
        "3": rgba((1, 1, 1)),
        "4": rgba((1, 1, 1)),
        "A": rgba((1, 1, 1)),
    })

    assert sprite.width == SPRITE_WIDTH
    assert sprite.height == SPRITE_HEIGHT


def test_character_sprite_feet_touch_bottom_row() -> None:
    pygame.init()
    try:
        library = CharacterSpriteLibrary()
        frame = library.frames[("player", "down", 0)]
    finally:
        pygame.quit()

    bottom_y = (SPRITE_HEIGHT * RENDER_SCALE) - 1
    bottom_pixels = [frame.get_at((x, bottom_y)).a for x in range(frame.get_width())]

    assert any(alpha > 0 for alpha in bottom_pixels)


def test_character_walk_frames_differ_from_idle() -> None:
    pygame.init()
    try:
        library = CharacterSpriteLibrary()
        idle = library.frames[("player", "down", 0)]
        walk = library.frames[("player", "down", 1)]
    finally:
        pygame.quit()

    assert any(
        idle.get_at((x, y)) != walk.get_at((x, y))
        for x in range(idle.get_width())
        for y in range(idle.get_height())
    )
