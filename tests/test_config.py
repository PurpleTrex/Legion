from legion.core.config import GameConfig


def test_window_size_uses_logical_resolution_and_scale() -> None:
    config = GameConfig(logical_width=640, logical_height=360, window_scale=2)

    assert config.window_size == (1280, 720)


def test_default_config_uses_readable_pixel_art_canvas() -> None:
    config = GameConfig()

    assert config.logical_width == 640
    assert config.logical_height == 360
    assert config.window_scale == 2
