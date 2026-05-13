from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
ASSET_DIR = ROOT_DIR / "assets"


@dataclass(frozen=True)
class GameConfig:
    title: str = "Legion"
    logical_width: int = 320
    logical_height: int = 180
    window_scale: int = 4
    target_fps: int = 60
    background_color: tuple[int, int, int] = (12, 13, 18)

    @property
    def window_size(self) -> tuple[int, int]:
        return (self.logical_width * self.window_scale, self.logical_height * self.window_scale)
