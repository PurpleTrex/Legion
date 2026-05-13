from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QuitGame:
    pass


@dataclass(frozen=True)
class ChangeScene:
    scene_name: str
