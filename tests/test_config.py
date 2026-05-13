from legion.core.config import GameConfig


def test_window_size_uses_logical_resolution_and_scale() -> None:
    config = GameConfig(logical_width=320, logical_height=180, window_scale=4)

    assert config.window_size == (1280, 720)
