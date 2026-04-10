# CLAUDE.md

## Project structure

```
V1.0.0/chord_trainer_gui.py   ← stable release, do not modify
UAT/chord_trainer_gui.py      ← active development version
```

## Running the app

```bash
python3 UAT/chord_trainer_gui.py
```

**Dependency:** `pip install customtkinter`

## Key facts

- Progress saved to `~/guitar_trainer_progress.json` (JSON array of session objects)
- Audio via `afplay` (macOS), falls back to terminal bell
- Architecture, constants, and session flow are self-documented in `UAT/chord_trainer_gui.py`
