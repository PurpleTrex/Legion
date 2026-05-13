# Legion

`Legion` is a 16-bit inspired open-world RPG built with pygame.

## Run Locally

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
python -m legion
```

On Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
python -m legion
```

## Project Layout

```text
assets/                 Game assets created for Legion
  audio/
  fonts/
  maps/
  sprites/
src/legion/             Game source
  core/                 Engine-level systems
  scenes/               Game scenes and scene flow
  ui/                   UI widgets and text helpers
storyboards/            Narrative and scene design documents
tests/                  Lightweight tests for non-rendering logic
tools/                  Asset/build helper scripts
```

## Current State

The project boots into a placeholder pygame scene. The next implementation target is Scene 01:

`storyboards/ACT I/scene-01-closing-shift.md`
