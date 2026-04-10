# Guitar Chord Trainer

A Python app to help guitarists practice chord recognition and switching speed.

![Python](https://img.shields.io/badge/python-3.8+-blue)

## Features

- Practice chords in any of the 12 major keys
- Built-in metronome with adjustable BPM (20–300), beats per chord, and Tap Tempo
- Visual guitar fretboard diagrams for every chord (50+ fingerings, barre chord detection)
- Roman numeral display (I, ii, iii, IV, V, vi, vii°) to reinforce music theory
- Difficulty modes: Beginner, Intermediate, Advanced, Custom
- Custom chord selection — pick exactly which chords to practice
- Session timer (5–30 min), volume control, and multiple click track sounds
- Custom sound support via `sounds.json`
- Chord history, 3-second countdown, and session progress saved automatically
- Scrollable dark-themed GUI, launches fullscreen

## Requirements

- Python 3.8+
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)

```bash
pip install customtkinter
```

## Usage

```bash
python3 main/chord_trainer_gui.py
```

1. Select a **key** from the dropdown
2. Set your **BPM**, **beats per chord**, and **difficulty**
3. Hit **Start** — a random chord from that key will appear each cycle
4. Play the chord, watch the beat indicators, and keep up!

## Custom Sounds

Add a `main/sounds.json` file to map chords to your own audio files:

```json
{
  "C": "/path/to/c.aiff",
  "G": "/path/to/g.aiff"
}
```

Missing or invalid paths fall back to the selected click track.
