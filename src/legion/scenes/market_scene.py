from __future__ import annotations

from dataclasses import dataclass

import pygame

from legion.core.config import GameConfig
from legion.core.events import QuitGame
from legion.gfx.snes_character_sprites import CharacterSpriteLibrary
from legion.scenes.scene import Scene
from legion.ui.text import draw_panel, wrap_text


INTERACT_KEYS = {pygame.K_SPACE, pygame.K_RETURN, pygame.K_e}
TILE = 8


@dataclass
class Character:
    name: str
    rect: pygame.Rect
    sprite_key: str
    facing: str = "down"
    visible: bool = True


@dataclass(frozen=True)
class Hotspot:
    name: str
    rect: pygame.Rect
    prompt: str


class MarketScene(Scene):
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.world_size = (320, 180)
        self.world_surface = pygame.Surface(self.world_size)
        self.world_scale = 2
        self.font = pygame.font.Font(None, 22)
        self.small_font = pygame.font.Font(None, 18)
        self.title_font = pygame.font.Font(None, 24)
        self.sprite_library = CharacterSpriteLibrary()
        self.elapsed = 0.0
        self.player = Character("You", pygame.Rect(154, 124, 12, 8), "player")
        self.npcs = {
            "hollis": Character("Hollis", pygame.Rect(72, 62, 12, 8), "hollis"),
            "mara": Character("Mara", pygame.Rect(206, 102, 12, 8), "mara"),
            "quiet_customer": Character("Quiet Customer", pygame.Rect(254, 58, 12, 8), "quiet_customer"),
            "silas": Character("Silas", pygame.Rect(116, 62, 12, 8), "silas"),
        }
        self.npcs["silas"].visible = False

        self.flags: set[str] = set()
        self.dialogue: list[str] = [
            "HOLLIS:\nIf that freezer starts screaming again, kick the panel twice.\nOnce makes it worse.",
            "MARA:\nThat is not how repairs work.",
            "HOLLIS:\nIt is how this store works.",
        ]
        self.dialogue_speaker = "Opening"
        self.current_line = 0
        self.phase = "closing"
        self.objective = "Finish closing tasks."
        self.notification = "11:43 PM  -  Marlowe's Market  -  Briarwake"
        self.notification_timer = 4.0
        self.crash_timer = 0.0
        self.flashlight_found = False
        self.collision_rects = self._build_collision_rects()
        self.hotspots = self._build_hotspots()

    def handle_events(self, events: list[pygame.event.Event]) -> list[object]:
        scene_events: list[object] = []
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in {pygame.K_ESCAPE, pygame.K_q}:
                scene_events.append(QuitGame())
            elif event.type == pygame.KEYDOWN and event.key in INTERACT_KEYS:
                if self.dialogue:
                    self._advance_dialogue()
                elif self.phase != "crashing":
                    self._interact()
        return scene_events

    def update(self, dt: float) -> None:
        self.elapsed += dt
        if self.notification_timer > 0:
            self.notification_timer = max(0.0, self.notification_timer - dt)

        if not self.dialogue and self.phase != "crashing":
            self._move_player(dt)
            self._update_story_progress()

        if self.phase == "crashing":
            self.crash_timer += dt
            if self.crash_timer >= 3.2 and "crash_done" not in self.flags:
                self.flags.add("crash_done")
                self.phase = "after_crash"
                self.objective = "Check on everyone."
                self.dialogue_speaker = "Aftershock"
                self.dialogue = [
                    "HOLLIS:\nEverybody still got the same number of limbs?",
                    "MARA:\nI am going to pretend that helped.",
                ]
                self.current_line = 0

    def draw(self, surface: pygame.Surface) -> None:
        self.world_surface.fill((0, 0, 0))
        self._draw_market(self.world_surface)
        self._draw_characters(self.world_surface)
        pygame.transform.scale_by(self.world_surface, self.world_scale, surface)
        self._draw_foreground(surface)
        self._draw_hud(surface)
        if self.dialogue:
            self._draw_dialogue(surface)
        if self.notification_timer > 0:
            self._draw_notification(surface)
        if self.phase == "crashing":
            self._draw_crash_overlay(surface)

    def _build_collision_rects(self) -> list[pygame.Rect]:
        return [
            pygame.Rect(0, 0, 320, 28),
            pygame.Rect(0, 0, 10, 180),
            pygame.Rect(310, 0, 10, 180),
            pygame.Rect(0, 168, 320, 12),
            pygame.Rect(24, 39, 89, 29),
            pygame.Rect(30, 88, 80, 14),
            pygame.Rect(30, 120, 80, 14),
            pygame.Rect(142, 76, 78, 14),
            pygame.Rect(142, 110, 78, 14),
            pygame.Rect(250, 80, 18, 48),
            pygame.Rect(284, 80, 18, 48),
            pygame.Rect(20, 146, 76, 20),
        ]

    def _build_hotspots(self) -> list[Hotspot]:
        return [
            Hotspot("radio", pygame.Rect(42, 35, 16, 10), "Check radio"),
            Hotspot("register", pygame.Rect(64, 36, 18, 12), "Use register"),
            Hotspot("freezer", pygame.Rect(248, 78, 56, 16), "Inspect freezer"),
            Hotspot("restock", pygame.Rect(146, 108, 68, 18), "Restock shelf"),
            Hotspot("community_board", pygame.Rect(284, 32, 18, 24), "Read board"),
            Hotspot("window", pygame.Rect(226, 30, 48, 10), "Look outside"),
            Hotspot("locker", pygame.Rect(24, 146, 24, 18), "Open locker"),
            Hotspot("flashlight", pygame.Rect(62, 146, 20, 16), "Search supplies"),
            Hotspot("phone", pygame.Rect(84, 36, 14, 10), "Use phone"),
            Hotspot("front_door", pygame.Rect(152, 28, 22, 12), "Exit"),
        ]

    def _move_player(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        dx = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
        if dx == 0 and dy == 0:
            return

        speed = 52
        if dx:
            self.player.facing = "right" if dx > 0 else "left"
        if dy:
            self.player.facing = "down" if dy > 0 else "up"

        movement = pygame.Vector2(dx, dy)
        if movement.length_squared() > 0:
            movement = movement.normalize() * speed * dt

        self._move_axis(int(round(movement.x)), 0)
        self._move_axis(0, int(round(movement.y)))

    def _move_axis(self, dx: int, dy: int) -> None:
        if dx == 0 and dy == 0:
            return
        self.player.rect.move_ip(dx, dy)
        blockers = [*self.collision_rects]
        blockers.extend(npc.rect for npc in self.npcs.values() if npc.visible)
        for rect in blockers:
            if self.player.rect.colliderect(rect):
                if dx > 0:
                    self.player.rect.right = rect.left
                elif dx < 0:
                    self.player.rect.left = rect.right
                elif dy > 0:
                    self.player.rect.bottom = rect.top
                elif dy < 0:
                    self.player.rect.top = rect.bottom

    def _update_story_progress(self) -> None:
        if self.phase == "closing" and self._pre_silas_task_count() >= 2 and "silas_arrived" not in self.flags:
            self.flags.add("silas_arrived")
            self.npcs["silas"].visible = True
            self.notification = "The front door chime rings."
            self.notification_timer = 3.0
            self.dialogue_speaker = "Silas"
            self.dialogue = ["SILAS:\nEvening. You keep the strong batteries up front?"]
            self.current_line = 0

        if self.phase == "closing" and self._ready_for_crash():
            self.phase = "crashing"
            self.crash_timer = 0.0
            self.flags.add("crash_triggered")

    def _pre_silas_task_count(self) -> int:
        task_flags = {
            "spoke_to_hollis",
            "spoke_to_mara",
            "inspected_radio",
            "restocked_shelf",
            "checked_freezer",
            "read_board",
        }
        return len(self.flags & task_flags)

    def _ready_for_crash(self) -> bool:
        required = {"spoke_to_hollis", "spoke_to_mara", "inspected_radio", "served_silas", "checked_window"}
        return required.issubset(self.flags) and "crash_triggered" not in self.flags

    def _advance_dialogue(self) -> None:
        self.current_line += 1
        if self.current_line >= len(self.dialogue):
            self.dialogue = []
            self.current_line = 0

    def _interact(self) -> None:
        npc = self._nearby_npc()
        if npc:
            self._talk_to_npc(npc)
            return

        hotspot = self._nearby_hotspot()
        if hotspot:
            self._use_hotspot(hotspot)

    def _nearby_npc(self) -> Character | None:
        reach = self.player.rect.inflate(14, 12)
        visible = [npc for npc in self.npcs.values() if npc.visible and reach.colliderect(npc.rect)]
        if not visible:
            return None
        return min(visible, key=lambda npc: self._distance_to(npc.rect.center))

    def _nearby_hotspot(self) -> Hotspot | None:
        reach = self.player.rect.inflate(14, 12)
        available = [hotspot for hotspot in self.hotspots if reach.colliderect(hotspot.rect)]
        if not available:
            return None
        return min(available, key=lambda hotspot: self._distance_to(hotspot.rect.center))

    def _distance_to(self, point: tuple[int, int]) -> float:
        px, py = self.player.rect.center
        return abs(px - point[0]) + abs(py - point[1])

    def _talk_to_npc(self, npc: Character) -> None:
        self.dialogue_speaker = npc.name
        if npc.name == "Hollis":
            self.flags.add("spoke_to_hollis")
            if self.phase == "after_crash":
                self.flags.add("checked_hollis")
                self.dialogue = ["HOLLIS:\nPresent. Bruised. Deeply annoyed.\nCheck Mara."]
            else:
                self.dialogue = [
                    "HOLLIS:\nCounter radio, Aisle Two, Mara, last customer, windows.",
                    "HOLLIS:\nThat gets us closed before Briarwake invents another problem.",
                ]
        elif npc.name == "Mara":
            self.flags.add("spoke_to_mara")
            if self.phase == "after_crash":
                self.flags.add("checked_mara")
                self.dialogue = ["MARA:\nHere. Not gracefully.\nI saw the window go white."]
            elif "inspected_radio" in self.flags:
                self.dialogue = ["MARA:\nThat sounded like three people using one mouth."]
            else:
                self.dialogue = [
                    "MARA:\nYou ever notice closing shift feels longer when the town is quiet?",
                    "MARA:\nTonight it keeps almost being quiet. That is worse.",
                ]
        elif npc.name == "Silas":
            self.flags.add("served_silas")
            self.npcs["silas"].visible = False
            self.dialogue = [
                "SILAS:\nYou ever seen rail lights turn on without power?",
                "MARA:\nIn Briarwake? Sure. Right before the bill arrives.",
                "SILAS:\nNo. All of them. One after another.\nLike something was walking down the line.",
                "SILAS:\nRook blinks red. This was under the ground.",
            ]
        else:
            if self.phase == "after_crash":
                self.flags.add("customer_left")
                self.npcs["quiet_customer"].visible = False
                self.dialogue = [
                    "PLAYER CHARACTER:\nAre you hurt?",
                    "QUIET CUSTOMER:\nNo.",
                    "QUIET CUSTOMER:\nIt missed the ground.",
                    "PLAYER CHARACTER:\nWhat did?",
                    "QUIET CUSTOMER:\nThe first part.",
                ]
            elif "checked_window" in self.flags:
                self.dialogue = [
                    "QUIET CUSTOMER:\nIt is closer now.",
                    "PLAYER CHARACTER:\nWhat is?",
                    "QUIET CUSTOMER:\nThe part that remembers.",
                ]
            elif "inspected_radio" in self.flags:
                self.dialogue = ["QUIET CUSTOMER:\nLong night.\nLong, long night."]
            else:
                self.dialogue = ["QUIET CUSTOMER:\nNo, thank you. I'm just looking."]
        self.current_line = 0

    def _use_hotspot(self, hotspot: Hotspot) -> None:
        self.dialogue_speaker = hotspot.prompt
        if hotspot.name == "radio":
            self.flags.add("inspected_radio")
            self.dialogue = [
                "KBRW HOST:\nStill no confirmation on the lights over Blackneedle.",
                "RADIO:\nalone alone alone",
                "KBRW HOST:\nHuh. Lost the board for a second there.",
            ]
        elif hotspot.name == "register":
            self.dialogue = ["The register drawer sticks, clicks, and gives up one receipt."]
        elif hotspot.name == "freezer":
            self.flags.add("checked_freezer")
            self.dialogue = [
                "The freezer buzzes like it is trying to remember a song.",
                "For a second, your teeth ache.",
            ]
        elif hotspot.name == "restock":
            self.flags.add("restocked_shelf")
            self.dialogue = [
                "You shelve bandages, batteries, and cheap flashlights.",
                "The kind of things people buy right before they pretend they are not worried.",
            ]
        elif hotspot.name == "community_board":
            self.flags.add("read_board")
            self.dialogue = [
                "The board is crowded with curled flyers.",
                "Vesper Clinic Blood Drive. Rook Signal Maintenance Road Closed.",
                "Calder Yard Redevelopment Meeting Postponed.",
            ]
        elif hotspot.name == "window":
            if self.phase == "after_crash":
                self.dialogue = [
                    "Ashbell Road is filling with porch lights and silhouettes.",
                    "Beyond them, Blackneedle Woods glows from below.",
                    "The light pulses like something breathing under the trees.",
                ]
            else:
                self.flags.add("checked_window")
                self.dialogue = [
                    "You look past Ashbell Road.",
                    "The tree line flickers.",
                    "Not lightning. Too low. Too steady.",
                ]
        elif hotspot.name == "locker":
            self.dialogue = [
                "A folded note sits inside your locker.",
                "You keep meaning to answer it.",
                "Not tonight.",
            ]
        elif hotspot.name == "flashlight":
            self.flags.add("found_flashlight")
            self.flashlight_found = True
            self.dialogue = ["You find a pocket flashlight.\nIt works after two hard shakes."]
        elif hotspot.name == "phone":
            self.flags.add("tried_phone")
            if self.phase == "after_crash":
                self.dialogue = [
                    "The line clicks open.",
                    "No dial tone.",
                    "Under the static, something breathes in time with the freezer.",
                ]
            else:
                self.dialogue = ["No missed calls.\nOne unsent message waits on the screen."]
        elif hotspot.name == "front_door":
            self._try_exit()
        self.current_line = 0

    def _try_exit(self) -> None:
        if self.phase != "after_crash":
            self.dialogue = ["HOLLIS:\nWe are not closed yet."]
            return

        needed = {"checked_hollis", "checked_mara", "customer_left", "found_flashlight", "tried_phone"}
        if not needed.issubset(self.flags):
            self.dialogue = ["You should check on everyone, find a light, and try calling out first."]
            return

        self.flags.add("exited_market")
        self.objective = "Find out what crashed beyond Blackneedle."
        self.dialogue = [
            "The door sticks against broken glass.",
            "Cold air pushes into the store.",
            "Outside, Briarwake is awake.",
        ]

    def _draw_market(self, surface: pygame.Surface) -> None:
        after_crash = self.phase in {"after_crash", "crashing"}
        wall = (38, 45, 52) if not after_crash else (25, 29, 36)
        floor_a = (46, 50, 45) if not after_crash else (31, 35, 34)
        floor_b = (54, 58, 52) if not after_crash else (37, 41, 40)
        surface.fill(wall)
        pygame.draw.rect(surface, (20, 23, 28), pygame.Rect(8, 27, 304, 141))

        for y in range(32, 168, TILE):
            for x in range(16, 304, TILE):
                color = floor_a if (x // TILE + y // TILE) % 2 == 0 else floor_b
                pygame.draw.rect(surface, color, pygame.Rect(x, y, TILE, TILE))

        self._draw_windows(surface, after_crash)
        self._draw_counter(surface)
        self._draw_shelves(surface)
        self._draw_freezers(surface)
        self._draw_back_room(surface)
        self._draw_details(surface, after_crash)

    def _draw_windows(self, surface: pygame.Surface, after_crash: bool) -> None:
        glow = (118, 198, 160) if after_crash else (32, 44, 62)
        for x in range(222, 278, 14):
            pygame.draw.rect(surface, (8, 12, 19), pygame.Rect(x, 27, 12, 13))
            pygame.draw.rect(surface, glow, pygame.Rect(x + 1, 29, 10, 9))
            if after_crash:
                pygame.draw.line(surface, (226, 244, 218), (x + 3, 29), (x + 9, 37))
        pygame.draw.rect(surface, (45, 30, 26), pygame.Rect(152, 28, 22, 8))
        pygame.draw.rect(surface, (95, 72, 48), pygame.Rect(158, 30, 10, 6))

    def _draw_counter(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (78, 47, 36), pygame.Rect(24, 39, 89, 29))
        pygame.draw.rect(surface, (132, 84, 53), pygame.Rect(26, 41, 85, 7))
        pygame.draw.rect(surface, (35, 38, 43), pygame.Rect(62, 35, 22, 12))
        pygame.draw.rect(surface, (13, 16, 20), pygame.Rect(43, 35, 14, 9))
        pygame.draw.circle(surface, (176, 72, 64), (50, 39), 2)
        pygame.draw.rect(surface, (201, 199, 159), pygame.Rect(88, 38, 9, 5))

    def _draw_shelves(self, surface: pygame.Surface) -> None:
        shelf_color = (72, 52, 42)
        edge = (128, 91, 57)
        for rect in [
            pygame.Rect(30, 88, 80, 14),
            pygame.Rect(30, 120, 80, 14),
            pygame.Rect(142, 76, 78, 14),
            pygame.Rect(142, 110, 78, 14),
        ]:
            pygame.draw.rect(surface, shelf_color, rect)
            pygame.draw.rect(surface, edge, rect, 1)
            for x in range(rect.left + 4, rect.right - 5, 9):
                pygame.draw.rect(surface, (154, 73, 51), pygame.Rect(x, rect.y + 3, 5, 8))
                pygame.draw.rect(surface, (197, 172, 86), pygame.Rect(x + 5, rect.y + 4, 3, 6))

    def _draw_freezers(self, surface: pygame.Surface) -> None:
        for rect in [pygame.Rect(250, 80, 18, 48), pygame.Rect(284, 80, 18, 48)]:
            pygame.draw.rect(surface, (33, 45, 55), rect)
            pygame.draw.rect(surface, (141, 202, 210), rect.inflate(-4, -6))
            pygame.draw.line(surface, (231, 250, 248), (rect.x + 4, rect.y + 8), (rect.x + 14, rect.y + 8))
            pygame.draw.rect(surface, (15, 24, 32), rect, 1)

    def _draw_back_room(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (28, 31, 34), pygame.Rect(18, 142, 84, 26))
        pygame.draw.rect(surface, (64, 72, 77), pygame.Rect(24, 146, 24, 18))
        pygame.draw.rect(surface, (98, 67, 45), pygame.Rect(54, 146, 36, 16))
        pygame.draw.rect(surface, (214, 197, 94), pygame.Rect(65, 149, 7, 5))

    def _draw_details(self, surface: pygame.Surface, after_crash: bool) -> None:
        pygame.draw.rect(surface, (70, 48, 30), pygame.Rect(282, 30, 23, 28))
        for y in range(34, 54, 5):
            pygame.draw.rect(surface, (190, 170, 108), pygame.Rect(286, y, 14, 3))

        if after_crash:
            pygame.draw.rect(surface, (82, 44, 36), pygame.Rect(50, 132, 26, 5))
            for x in range(52, 88, 7):
                pygame.draw.circle(surface, (122, 68, 50), (x, 139), 2)
            pygame.draw.line(surface, (210, 233, 220), (232, 31), (240, 38))
            pygame.draw.line(surface, (210, 233, 220), (250, 28), (245, 38))

    def _draw_characters(self, surface: pygame.Surface) -> None:
        characters = [npc for npc in self.npcs.values() if npc.visible]
        characters.append(self.player)
        for character in sorted(characters, key=lambda c: c.rect.bottom):
            self._draw_character(surface, character)

    def _draw_character(self, surface: pygame.Surface, character: Character) -> None:
        bob = int(self.elapsed * 8) % 2 if character is self.player else 0
        self.sprite_library.draw(
            surface,
            character.sprite_key,
            character.facing,
            character.rect.midbottom,
            bob=bob,
        )

    def _draw_foreground(self, surface: pygame.Surface) -> None:
        prompt = self._current_prompt()
        if prompt and not self.dialogue and self.phase != "crashing":
            rendered = self.small_font.render(prompt, False, (236, 236, 204))
            center = (
                self.player.rect.centerx * self.world_scale,
                self.player.rect.top * self.world_scale - 58,
            )
            rect = rendered.get_rect(center=center)
            pygame.draw.rect(surface, (12, 14, 18), rect.inflate(12, 8))
            surface.blit(rendered, rect)

    def _current_prompt(self) -> str | None:
        npc = self._nearby_npc()
        if npc:
            return f"Space: Talk to {npc.name}"
        hotspot = self._nearby_hotspot()
        if hotspot:
            return f"Space: {hotspot.prompt}"
        return None

    def _draw_hud(self, surface: pygame.Surface) -> None:
        draw_panel(surface, pygame.Rect(16, 16, 264, 48), fill=(16, 18, 24))
        objective = self.small_font.render(self.objective, False, (220, 225, 205))
        surface.blit(objective, (28, 31))

        draw_panel(surface, pygame.Rect(398, 16, 226, 90), fill=(16, 18, 24))
        tasks = self._task_lines()
        for index, line in enumerate(tasks[:4]):
            color = (132, 196, 126) if line.startswith("x") else (210, 210, 190)
            rendered = self.small_font.render(line, False, color)
            surface.blit(rendered, (410, 28 + index * 18))

    def _task_lines(self) -> list[str]:
        if self.phase == "after_crash":
            return [
                self._task("checked_hollis", "Hollis"),
                self._task("checked_mara", "Mara"),
                self._task("customer_left", "Customer"),
                self._task("found_flashlight", "Flashlight"),
            ]
        return [
            self._task("spoke_to_hollis", "Hollis"),
            self._task("spoke_to_mara", "Mara"),
            self._task("inspected_radio", "Radio"),
            self._task("served_silas", "Customer"),
        ]

    def _task(self, flag: str, label: str) -> str:
        return f"x {label}" if flag in self.flags else f"- {label}"

    def _draw_dialogue(self, surface: pygame.Surface) -> None:
        rect = pygame.Rect(20, 248, 600, 92)
        draw_panel(surface, rect)
        speaker = self.title_font.render(self.dialogue_speaker, False, (238, 224, 174))
        surface.blit(speaker, (36, 260))
        text = self.dialogue[self.current_line]
        lines = wrap_text(text, self.font, 552)
        for index, line in enumerate(lines[:4]):
            rendered = self.font.render(line, False, (232, 236, 218))
            surface.blit(rendered, (36, 286 + index * 18))
        hint = self.small_font.render("Space", False, (155, 164, 150))
        surface.blit(hint, (560, 316))

    def _draw_notification(self, surface: pygame.Surface) -> None:
        rendered = self.small_font.render(self.notification, False, (228, 231, 210))
        rect = rendered.get_rect(center=(self.config.logical_width // 2, 140))
        pygame.draw.rect(surface, (10, 12, 17), rect.inflate(16, 10))
        surface.blit(rendered, rect)

    def _draw_crash_overlay(self, surface: pygame.Surface) -> None:
        progress = min(1.0, self.crash_timer / 3.2)
        if progress < 0.35:
            alpha = int(90 * progress)
            color = (80, 220, 170)
        elif progress < 0.55:
            alpha = 180
            color = (228, 254, 218)
        else:
            alpha = int(150 * (1.0 - progress))
            color = (80, 220, 170)

        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((*color, max(0, min(220, alpha))))
        surface.blit(overlay, (0, 0))

        if progress > 0.18:
            text = "For one second, everything in the store listens."
            rendered = self.font.render(text, False, (10, 14, 12))
            surface.blit(rendered, rendered.get_rect(center=(320, 184)))
