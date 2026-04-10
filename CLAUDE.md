# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project structure

```
V1.0.0/chord_trainer_gui.py   ← stable release, do not modify
UAT/chord_trainer_gui.py      ← active development version
```

## Running the app

```bash
python3 UAT/chord_trainer_gui.py
```

**External dependency:** `customtkinter` — `pip install customtkinter`

## UAT version — features & architecture

### Classes

| Class | Purpose |
|---|---|
| `ChordDiagram` | `tkinter.Canvas` subclass. Draws a 6-string fretboard from a fret list. Auto-detects and renders barre chords as a pill shape. |
| `Metronome` | Daemon thread. Fires `on_beat(beat, accent)` callback; accent on beat 1. Supports live updates to BPM, beats-per-chord, and sound set. |
| `TapTempo` | Stateful tap calculator. Call `.tap()` on each button press; returns BPM or `None` if only one tap so far. Clears stale taps after 3s. |
| `ChordTrainerApp` | Main `customtkinter` window. Owns all UI and session state. |

### UI layout (rows, top to bottom)

0. Title  
1. **Settings card** — Key dropdown, BPM slider + Tap Tempo button, Beats segmented button  
2. **Session card** — Difficulty, Timer, Sound dropdown  
3. **Custom chord frame** — 7 checkboxes, shown only when Difficulty = Custom  
4. **Chord display card** — key info label, large chord name, Roman numeral, history row (last 3 chords)  
5. **Diagram card** — `ChordDiagram` canvas  
6. Beat dot indicator  
7. Start / Stop button  

### Key data (module-level constants)

- **`KEYS`** — 12 major keys → 7 diatonic chord names each
- **`CHORD_FINGERINGS`** — chord name → `[E2,A2,D3,G3,B3,e4]` fret list (`-1`=muted, `0`=open)
- **`ROMAN_NUMERALS`** — `["I","ii","iii","IV","V","vi","vii°"]`
- **`OPEN_CHORDS`** / **`BARRE_CHORDS`** — sets used to filter chords by difficulty
- **`SOUND_SETS`** — dict of 4 named click-track options, each a `(accent_path, beat_path)` tuple

### Session flow

1. User hits Start → 3-second countdown in chord label → `_do_start()`
2. `Metronome` thread fires `_on_beat()` → beat 1 calls `_pick_next_chord()`, then schedules `_refresh_display()` on main thread via `after(0, ...)`
3. `_pick_next_chord()` respects difficulty filter (`_get_available_indices()`), avoids repeating the last chord, and tracks `session_chord_counts`
4. On Stop (manual or timer expiry) → session data saved silently to `~/guitar_trainer_progress.json`

### Audio

`afplay` (macOS) via `subprocess.Popen`; falls back to terminal bell. Sound set swappable live.

### Progress file

`~/guitar_trainer_progress.json` — JSON array of session objects:
`date, key, difficulty, duration_secs, chords_played, avg_bpm, chord_counts`
