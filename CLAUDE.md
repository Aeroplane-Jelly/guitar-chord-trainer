# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
python chord_trainer_gui.py
```

**External dependency:** `customtkinter` (not in a requirements file, install via `pip install customtkinter`)

## Architecture

Single Python script — no build system.

### `chord_trainer_gui.py`
Three classes:
- **`ChordDiagram`** — `tkinter.Canvas` subclass that renders a guitar fretboard. Reads a 6-element list of fret positions (`-1`=muted, `0`=open, `N`=fret number), auto-detects barre chords, and draws fingering dots.
- **`Metronome`** — Background thread. Fires a callback on each beat; accent on beat 1. BPM and beats-per-chord are adjustable live.
- **`ChordTrainerApp`** — `customtkinter` root window. Owns the settings card (key, BPM, beats), display card (chord name + Roman numeral), diagram card (`ChordDiagram`), and beat indicator row.

### Key data
- **`KEYS`** — dict mapping 12 major key names → list of 7 diatonic chord names.
- **`CHORD_FINGERINGS`** — dict mapping chord name → 6-int list of fret positions (50+ chords).
- **`ROMAN_NUMERALS`** — `["I", "ii", "iii", "IV", "V", "vi", "vii°"]`

Audio uses `afplay` (macOS) via `subprocess`; falls back to terminal bell.
