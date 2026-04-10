# CLAUDE.md

## Project structure

```
main/chord_trainer_gui.py   ← active development version
main/sounds.json            ← optional custom chord sounds mapping
```

## Running the app

```bash
python3 main/chord_trainer_gui.py
```

**Dependency:** `pip install customtkinter`

## Key facts

- Progress saved to `~/guitar_trainer_progress.json` (JSON array of session objects)
- Audio via `afplay` (macOS), falls back to terminal bell
- Architecture, constants, and session flow are self-documented in `main/chord_trainer_gui.py`
