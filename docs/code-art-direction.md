# Legion Code Art Direction

## Goal

`Legion` uses original code-generated pixel art inspired by the readability and charm of 16-bit top-down RPGs. We should not copy, trace, rip, or recreate copyrighted sprites or tiles from existing games. The target is a similar production language: compact characters, clear silhouettes, limited palettes, hard pixel edges, and tile-based environments.

## Sprite Construction Rules

- Define sprites as indexed pixel rows in code.
- Treat `.` as transparency.
- Keep character metasprites near `16x24` pixels at logical resolution.
- Build characters from a small palette: outline, skin, hair, shirt, shadow shirt, pants, shoes, and optional accent pixels.
- Use dark outlines around heads, bodies, and shoes.
- Favor oversized heads and short bodies for readable top-down RPG expression.
- Keep each character visually distinct through hair shape, shirt color, and posture rather than high detail.
- Add facing frames before adding many animation frames.

## Environment Construction Rules

- Think in `8x8` tiles first.
- Use repeated tile patterns with slight accent variation.
- Use hard outlines for interactable objects.
- Prefer simple, readable object silhouettes: counter, freezer, shelf, window, door, locker, register.
- Use stronger color contrast around exits, windows, counters, and NPC paths.
- Keep interiors denser than decorative backgrounds; the player should know where they can walk.

## Current Implementation

- `src/legion/gfx/pixel_sprite.py` converts indexed character rows into pygame surfaces.
- `src/legion/gfx/snes_character_sprites.py` defines the first character palettes and facing frames.
- `src/legion/scenes/market_scene.py` draws `Marlowe's Market` entirely with pygame primitives and code sprites.

## Next Improvements

- Add walk animation frames for each facing direction.
- Replace placeholder UI font rendering with a custom code-generated pixel font.
- Build tile helpers for floor, wall, shelf, freezer, window, and debris tiles.
- Add code-generated exterior tiles for `Ashbell Road`.
- Add palette swapping for crash lighting and infected effects.
