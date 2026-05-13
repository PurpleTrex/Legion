from __future__ import annotations

from abc import ABC, abstractmethod

import pygame


class Scene(ABC):
    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> list[object]:
        raise NotImplementedError

    @abstractmethod
    def update(self, dt: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        raise NotImplementedError
