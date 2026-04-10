# Guitar Chord Trainer

A Python app to help guitarists practice chord recognition and switching speed.

![Python](https://img.shields.io/badge/python-3.8+-blue)

## Features

- Practice chords in any of the 12 major keys
- Built-in metronome with adjustable BPM (20–300) and beats per chord
- Visual guitar fretboard diagrams for every chord
- Covers open chords and barre chords (50+ fingerings)
- Displays Roman numerals (I, ii, iii, IV, V, vi, vii°) to reinforce music theory
- Dark-themed GUI

## Requirements

- Python 3.8+
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)

```bash
pip install customtkinter
```

## Usage

```bash
python chord_trainer_gui.py
```

1. Select a **key** from the dropdown
2. Set your **BPM** and **beats per chord**
3. Hit **Start** — a random chord from that key will appear each cycle
4. Play the chord, watch the beat indicators, and keep up!
