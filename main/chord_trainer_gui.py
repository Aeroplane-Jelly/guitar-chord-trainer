import random
import time
import sys
import json
import os
import threading
import subprocess
import shutil
import tkinter as tk
from datetime import datetime
import customtkinter as ctk

# ── Diatonic chords for each major key (I ii iii IV V vi vii°) ─────────────
KEYS = {
    'C':  ['C',  'Dm',  'Em',  'F',  'G',  'Am',  'Bdim'],
    'G':  ['G',  'Am',  'Bm',  'C',  'D',  'Em',  'F#dim'],
    'D':  ['D',  'Em',  'F#m', 'G',  'A',  'Bm',  'C#dim'],
    'A':  ['A',  'Bm',  'C#m', 'D',  'E',  'F#m', 'G#dim'],
    'E':  ['E',  'F#m', 'G#m', 'A',  'B',  'C#m', 'D#dim'],
    'B':  ['B',  'C#m', 'D#m', 'E',  'F#', 'G#m', 'A#dim'],
    'F#': ['F#', 'G#m', 'A#m', 'B',  'C#', 'D#m', 'E#dim'],
    'F':  ['F',  'Gm',  'Am',  'Bb', 'C',  'Dm',  'Edim'],
    'Bb': ['Bb', 'Cm',  'Dm',  'Eb', 'F',  'Gm',  'Adim'],
    'Eb': ['Eb', 'Fm',  'Gm',  'Ab', 'Bb', 'Cm',  'Ddim'],
    'Ab': ['Ab', 'Bbm', 'Cm',  'Db', 'Eb', 'Fm',  'Gdim'],
    'Db': ['Db', 'Ebm', 'Fm',  'Gb', 'Ab', 'Bbm', 'Cdim'],
}

ROMAN_NUMERALS = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°']

# ── Chord fingerings ─────────────────────────────────────────────────────────
# [E2, A2, D3, G3, B3, e4]  |  -1 = muted (X)  |  0 = open (O)  |  N = fret N
CHORD_FINGERINGS = {
    'C':     [-1, 3, 2, 0, 1, 0],
    'Dm':    [-1, -1, 0, 2, 3, 1],
    'Em':    [0, 2, 2, 0, 0, 0],
    'F':     [1, 1, 2, 3, 3, 1],
    'G':     [3, 2, 0, 0, 0, 3],
    'Am':    [-1, 0, 2, 2, 1, 0],
    'Bdim':  [-1, 2, 3, 4, 3, -1],
    'D':     [-1, -1, 0, 2, 3, 2],
    'A':     [-1, 0, 2, 2, 2, 0],
    'E':     [0, 2, 2, 1, 0, 0],
    'B':     [-1, 2, 4, 4, 4, 2],
    'Bm':    [-1, 2, 4, 4, 3, 2],
    'F#m':   [2, 4, 4, 2, 2, 2],
    'C#m':   [-1, 4, 6, 6, 5, 4],
    'G#m':   [4, 6, 6, 4, 4, 4],
    'D#m':   [-1, 6, 8, 8, 7, 6],
    'Ebm':   [-1, 6, 8, 8, 7, 6],
    'A#m':   [-1, 1, 3, 3, 2, 1],
    'Bbm':   [-1, 1, 3, 3, 2, 1],
    'F#':    [2, 4, 4, 3, 2, 2],
    'Gb':    [2, 4, 4, 3, 2, 2],
    'C#':    [-1, 4, 6, 6, 6, 4],
    'Db':    [-1, 4, 6, 6, 6, 4],
    'Bb':    [-1, 1, 3, 3, 3, 1],
    'Eb':    [-1, 6, 8, 8, 8, 6],
    'Gm':    [3, 5, 5, 3, 3, 3],
    'Cm':    [-1, 3, 5, 5, 4, 3],
    'Fm':    [1, 3, 3, 1, 1, 1],
    'Ab':    [4, 6, 6, 5, 4, 4],
    'F#dim': [-1, -1, 4, 5, 4, 5],
    'C#dim': [-1, -1, 2, 3, 2, 3],
    'G#dim': [-1, -1, 5, 6, 5, 6],
    'D#dim': [-1, -1, 1, 2, 1, 2],
    'A#dim': [-1, -1, 3, 4, 3, 4],
    'E#dim': [-1, -1, 3, 4, 3, 4],
    'Edim':  [-1, -1, 2, 3, 2, 3],
    'Adim':  [-1, 0, 1, 2, 1, -1],
    'Gdim':  [-1, -1, 5, 6, 5, 6],
    'Ddim':  [-1, -1, 0, 1, 0, 1],
    'Cdim':  [-1, -1, 1, 2, 1, 2],
}

# ── Difficulty chord sets ────────────────────────────────────────────────────
OPEN_CHORDS  = {'C', 'Dm', 'Em', 'F', 'G', 'Am', 'D', 'A', 'E'}
BARRE_CHORDS = {'B', 'Bm', 'F#m', 'C#m', 'G#m', 'D#m', 'Ebm', 'A#m', 'Bbm',
                'F#', 'Gb', 'C#', 'Db', 'Bb', 'Eb', 'Gm', 'Cm', 'Fm', 'Ab',
                'Bdim'}
# Advanced = all including diminished

# ── Sound sets (accent, beat) ────────────────────────────────────────────────
SOUND_SETS = {
    'Default':    ('/System/Library/Sounds/Tink.aiff',  '/System/Library/Sounds/Pop.aiff'),
    'Wood Block': ('/System/Library/Sounds/Basso.aiff', '/System/Library/Sounds/Funk.aiff'),
    'Click':      ('/System/Library/Sounds/Morse.aiff', '/System/Library/Sounds/Ping.aiff'),
    'Bell':       ('/System/Library/Sounds/Glass.aiff', '/System/Library/Sounds/Hero.aiff'),
}
PROGRESS_FILE  = os.path.expanduser('~/guitar_trainer_progress.json')
SOUNDS_MAP_FILE = os.path.join(os.path.dirname(__file__), 'sounds.json')
HAS_AFPLAY     = shutil.which('afplay') is not None


def _load_custom_sounds() -> dict:
    """Load sounds.json if present; return validated {chord: path} mapping."""
    if not os.path.exists(SOUNDS_MAP_FILE):
        return {}
    try:
        with open(SOUNDS_MAP_FILE) as f:
            raw = json.load(f)
        return {k: v for k, v in raw.items() if isinstance(v, str) and os.path.exists(v)}
    except (json.JSONDecodeError, OSError):
        return {}

CUSTOM_SOUNDS = _load_custom_sounds()

# ── Colours ──────────────────────────────────────────────────────────────────
BG_CANVAS   = '#2b2b2b'
DOT_COLOUR  = '#4a9eff'
MUTE_COLOUR = '#cc4444'
OPEN_COLOUR = '#aaaaaa'
FRET_COLOUR = '#555555'
STR_COLOUR  = '#777777'
NUT_COLOUR  = '#cccccc'


# ── Volume ────────────────────────────────────────────────────────────────────
_volume = 1.0

def set_volume(level: float):
    global _volume
    _volume = max(0.0, min(1.0, level))

def play_sound(path, chord=None):
    resolved = CUSTOM_SOUNDS.get(chord, path) if chord else path
    if HAS_AFPLAY:
        subprocess.Popen(['afplay', '-v', str(round(_volume, 2)), resolved],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        sys.stdout.write('\a'); sys.stdout.flush()


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_session(data):
    sessions = load_progress()
    sessions.append(data)
    try:
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(sessions, f, indent=2)
    except OSError:
        pass


# ── Tap Tempo ─────────────────────────────────────────────────────────────────
class TapTempo:
    def __init__(self, max_taps=8, timeout=3.0):
        self.taps     = []
        self.max_taps = max_taps
        self.timeout  = timeout

    def tap(self):
        now = time.time()
        self.taps = [t for t in self.taps if now - t < self.timeout]
        self.taps.append(now)
        if len(self.taps) < 2:
            return None
        intervals = [self.taps[i + 1] - self.taps[i]
                     for i in range(len(self.taps) - 1)]
        bpm = round(60.0 / (sum(intervals) / len(intervals)))
        return max(20, min(300, bpm))


# ── Chord Diagram ─────────────────────────────────────────────────────────────
class ChordDiagram(tk.Canvas):
    SS = 30;  FS = 30;  NF = 4;  NS = 6
    MT = 36;  ML = 38;  MR = 16; MB = 12;  DR = 9

    def __init__(self, parent, **kwargs):
        w = self.ML + (self.NS - 1) * self.SS + self.MR
        h = self.MT + self.NF * self.FS + self.MB
        super().__init__(parent, width=w, height=h,
                         bg=BG_CANVAS, highlightthickness=0, **kwargs)

    def draw(self, frets):
        self.delete('all')
        if frets is None:
            self._draw_placeholder(); return

        played    = [f for f in frets if f > 0]
        base_fret = 1 if (not played or min(played) <= 4) else min(played)
        ml, mt, ss, fs, dr = self.ML, self.MT, self.SS, self.FS, self.DR

        if base_fret == 1:
            self.create_rectangle(ml, mt, ml + (self.NS - 1) * ss, mt + 5,
                                  fill=NUT_COLOUR, outline='')
        else:
            self.create_text(ml - 6, mt + fs // 2, text=f"{base_fret}fr",
                             fill='#aaaaaa', font=('Arial', 9), anchor='e')
            self.create_line(ml, mt, ml + (self.NS - 1) * ss, mt,
                             fill=FRET_COLOUR, width=1)

        for i in range(1, self.NF + 1):
            y = mt + i * fs
            self.create_line(ml, y, ml + (self.NS - 1) * ss, y,
                             fill=FRET_COLOUR, width=1)
        for s in range(self.NS):
            x = ml + s * ss
            self.create_line(x, mt, x, mt + self.NF * fs, fill=STR_COLOUR, width=1)

        barre_fret = barre_x1 = barre_x2 = None
        if played:
            min_fret      = min(played)
            barre_strings = [s for s, f in enumerate(frets) if f == min_fret]
            if len(barre_strings) >= 2 and barre_strings[-1] - barre_strings[0] >= 3:
                barre_fret = min_fret
                barre_x1   = ml + barre_strings[0]  * ss
                barre_x2   = ml + barre_strings[-1] * ss

        if barre_fret is not None:
            rel = barre_fret - base_fret
            if 0 <= rel < self.NF:
                y = mt + rel * fs + fs // 2
                self.create_rectangle(barre_x1, y - dr, barre_x2, y + dr,
                                      fill=DOT_COLOUR, outline='')
                self.create_oval(barre_x1 - dr, y - dr, barre_x1 + dr, y + dr,
                                 fill=DOT_COLOUR, outline='')
                self.create_oval(barre_x2 - dr, y - dr, barre_x2 + dr, y + dr,
                                 fill=DOT_COLOUR, outline='')

        for s, fret in enumerate(frets):
            x = ml + s * ss
            if fret == -1:
                self.create_text(x, mt - 20, text='✕',
                                 fill=MUTE_COLOUR, font=('Arial', 13, 'bold'))
            elif fret == 0:
                r = 7
                self.create_oval(x - r, mt - 30, x + r, mt - 16,
                                 outline=OPEN_COLOUR, width=2)
            else:
                rel = fret - base_fret
                if 0 <= rel < self.NF:
                    y = mt + rel * fs + fs // 2
                    self.create_oval(x - dr, y - dr, x + dr, y + dr,
                                     fill=DOT_COLOUR, outline='')

    def _draw_placeholder(self):
        ml, mt, ss, fs = self.ML, self.MT, self.SS, self.FS
        self.create_rectangle(ml, mt, ml + (self.NS - 1) * ss, mt + 5,
                              fill='#444444', outline='')
        for i in range(1, self.NF + 1):
            self.create_line(ml, mt + i * fs, ml + (self.NS - 1) * ss,
                             mt + i * fs, fill='#3a3a3a', width=1)
        for s in range(self.NS):
            x = ml + s * ss
            self.create_line(x, mt, x, mt + self.NF * fs, fill='#3a3a3a', width=1)


# ── Metronome ─────────────────────────────────────────────────────────────────
class Metronome:
    def __init__(self, bpm, beats_per_chord, on_beat, sound_set='Default'):
        self.interval        = 60.0 / bpm
        self.beats_per_chord = beats_per_chord
        self.on_beat         = on_beat
        self.sound_set       = sound_set
        self._stop           = threading.Event()
        self._thread         = threading.Thread(target=self._run, daemon=True)

    def start(self):   self._thread.start()
    def stop(self):    self._stop.set()

    def update_bpm(self, bpm):       self.interval        = 60.0 / bpm
    def update_beats(self, beats):   self.beats_per_chord = beats
    def update_sound(self, s):       self.sound_set       = s

    def _run(self):
        beat      = 1
        next_tick = time.perf_counter()
        while not self._stop.is_set():
            now = time.perf_counter()
            if now >= next_tick:
                accent = (beat == 1)
                acc_snd, beat_snd = SOUND_SETS.get(self.sound_set, SOUND_SETS['Default'])
                play_sound(acc_snd if accent else beat_snd)
                self.on_beat(beat, accent)
                beat      = (beat % self.beats_per_chord) + 1
                next_tick += self.interval
            time.sleep(0.001)


# ── Main App ──────────────────────────────────────────────────────────────────
class ChordTrainerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Guitar Chord Trainer")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.metronome          = None
        self.running            = False
        self.last_index         = None
        self.chord_num          = 0
        self.current_beat       = 1
        self._next_chord        = '—'
        self._next_numeral      = ''
        self.chord_history      = []   # list of (chord, numeral)
        self.session_start      = None
        self.session_bpms       = []
        self.session_chord_counts = {}
        self._timer_job         = None
        self._countdown_n       = 0
        self.tap_tempo         = TapTempo()
        self._custom_vars      = {}   # chord name -> tk.BooleanVar
        self._custom_checks    = {}   # chord name -> CTkCheckBox

        self._build_ui()
        self.update_idletasks()
        w = self.winfo_reqwidth()
        h = min(self.winfo_reqheight(), self.winfo_screenheight() - 80)
        self.geometry(f"{w}x{h}")

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(self, text="Guitar Chord Trainer",
                     font=ctk.CTkFont(size=22, weight="bold")
                     ).grid(row=0, column=0, pady=(18, 4))

        # ── Settings card ──
        settings = ctk.CTkFrame(self, corner_radius=14)
        settings.grid(row=1, column=0, padx=24, pady=6, sticky="ew")
        settings.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(settings, text="Key",
                     font=ctk.CTkFont(size=12)).grid(row=0, column=0, pady=(12, 2))
        self.key_var = ctk.StringVar(value='C')
        ctk.CTkOptionMenu(settings, values=list(KEYS.keys()),
                          variable=self.key_var, width=90,
                          command=self._on_key_change
                          ).grid(row=1, column=0, padx=12, pady=(0, 12))

        ctk.CTkLabel(settings, text="BPM",
                     font=ctk.CTkFont(size=12)).grid(row=0, column=1, pady=(12, 2))
        self.bpm_var = ctk.IntVar(value=60)
        bpm_frame = ctk.CTkFrame(settings, fg_color="transparent")
        bpm_frame.grid(row=1, column=1, padx=8, pady=(0, 4))
        self.bpm_label = ctk.CTkLabel(bpm_frame, text="60",
                                      font=ctk.CTkFont(size=13, weight="bold"), width=32)
        self.bpm_label.pack()
        ctk.CTkSlider(bpm_frame, from_=20, to=220, number_of_steps=200,
                      variable=self.bpm_var, width=110,
                      command=self._on_bpm_change).pack(pady=(2, 4))
        ctk.CTkButton(bpm_frame, text="Tap Tempo", height=26,
                      font=ctk.CTkFont(size=11), corner_radius=8,
                      command=self._on_tap_tempo).pack(pady=(0, 8))

        ctk.CTkLabel(settings, text="Beats / Chord",
                     font=ctk.CTkFont(size=12)).grid(row=0, column=2, pady=(12, 2))
        self.beats_var = ctk.IntVar(value=4)
        ctk.CTkSegmentedButton(settings, values=["2", "3", "4", "8"],
                               command=self._on_beats_change, width=110
                               ).grid(row=1, column=2, padx=12, pady=(0, 12))

        # ── Session options card ──
        sess = ctk.CTkFrame(self, corner_radius=14)
        sess.grid(row=2, column=0, padx=24, pady=6, sticky="ew")
        sess.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(sess, text="Difficulty",
                     font=ctk.CTkFont(size=12)).grid(row=0, column=0, pady=(12, 2))
        self.difficulty_var = ctk.StringVar(value='Advanced')
        ctk.CTkOptionMenu(sess, values=['Beginner', 'Intermediate', 'Advanced', 'Custom'],
                          variable=self.difficulty_var, width=110,
                          command=self._on_difficulty_change
                          ).grid(row=1, column=0, padx=8, pady=(0, 12))

        ctk.CTkLabel(sess, text="Timer",
                     font=ctk.CTkFont(size=12)).grid(row=0, column=1, pady=(12, 2))
        self.timer_var = ctk.StringVar(value='Off')
        ctk.CTkOptionMenu(sess, values=['Off', '5 min', '10 min', '15 min', '20 min', '30 min'],
                          variable=self.timer_var, width=90
                          ).grid(row=1, column=1, padx=8, pady=(0, 12))

        ctk.CTkLabel(sess, text="Sound",
                     font=ctk.CTkFont(size=12)).grid(row=0, column=2, pady=(12, 2))
        self.sound_var = ctk.StringVar(value='Default')
        ctk.CTkOptionMenu(sess, values=list(SOUND_SETS.keys()),
                          variable=self.sound_var, width=100,
                          command=self._on_sound_change
                          ).grid(row=1, column=2, padx=8, pady=(0, 12))

        # Volume row
        sess.grid_columnconfigure((0, 1, 2), weight=1)
        ctk.CTkLabel(sess, text="Volume",
                     font=ctk.CTkFont(size=12)).grid(row=2, column=0, columnspan=3, pady=(4, 2))
        vol_frame = ctk.CTkFrame(sess, fg_color="transparent")
        vol_frame.grid(row=3, column=0, columnspan=3, pady=(0, 12))
        ctk.CTkButton(vol_frame, text="−", width=32, height=28,
                      font=ctk.CTkFont(size=16), corner_radius=8,
                      command=self._volume_down).pack(side="left", padx=4)
        self.volume_label = ctk.CTkLabel(vol_frame, text="100%",
                                         font=ctk.CTkFont(size=13, weight="bold"), width=48)
        self.volume_label.pack(side="left", padx=4)
        ctk.CTkButton(vol_frame, text="+", width=32, height=28,
                      font=ctk.CTkFont(size=16), corner_radius=8,
                      command=self._volume_up).pack(side="left", padx=4)

# ── Custom chord selection (hidden until difficulty = Custom) ──
        self.custom_frame = ctk.CTkFrame(self, corner_radius=14)
        self._build_custom_frame()

        # ── Chord display card ──
        chord_card = ctk.CTkFrame(self, corner_radius=14)
        chord_card.grid(row=4, column=0, padx=24, pady=6, sticky="ew")
        chord_card.grid_columnconfigure(0, weight=1)

        self.key_display = ctk.CTkLabel(chord_card,
                                        text="Select a key and press Start",
                                        font=ctk.CTkFont(size=12))
        self.key_display.grid(row=0, column=0, pady=(12, 0))

        self.chord_label = ctk.CTkLabel(chord_card, text="—",
                                        font=ctk.CTkFont(size=72, weight="bold"))
        self.chord_label.grid(row=1, column=0, pady=(0, 0))

        self.numeral_label = ctk.CTkLabel(chord_card, text="",
                                          font=ctk.CTkFont(size=20),
                                          text_color="gray70")
        self.numeral_label.grid(row=2, column=0, pady=(0, 6))

        self.history_label = ctk.CTkLabel(chord_card, text="",
                                          font=ctk.CTkFont(size=12),
                                          text_color="gray50")
        self.history_label.grid(row=3, column=0, pady=(0, 12))

        # ── Diagram card ──
        diagram_card = ctk.CTkFrame(self, corner_radius=14)
        diagram_card.grid(row=5, column=0, padx=24, pady=6, sticky="ew")
        diagram_card.grid_columnconfigure(0, weight=1)

        self.diagram = ChordDiagram(diagram_card)
        self.diagram.grid(row=0, column=0, pady=12)
        self.diagram.draw(None)

        # ── Beat dots ──
        self.dot_label = ctk.CTkLabel(self, text="",
                                      font=ctk.CTkFont(size=26))
        self.dot_label.grid(row=6, column=0, pady=4)

        # ── Start / Stop ──
        self.start_btn = ctk.CTkButton(self, text="Start",
                                       font=ctk.CTkFont(size=16, weight="bold"),
                                       height=48, corner_radius=12,
                                       command=self._toggle)
        self.start_btn.grid(row=7, column=0, padx=24, pady=(4, 20), sticky="ew")

    def _build_custom_frame(self):
        for widget in self.custom_frame.winfo_children():
            widget.destroy()
        self._custom_vars.clear()
        self._custom_checks.clear()

        key    = self.key_var.get()
        chords = KEYS[key]

        ctk.CTkLabel(self.custom_frame, text=f"Chords in {key} major — select which to practice",
                     font=ctk.CTkFont(size=12), text_color="gray60"
                     ).grid(row=0, column=0, columnspan=7, pady=(10, 4))

        for i, chord in enumerate(chords):
            cb = ctk.CTkCheckBox(self.custom_frame, text=chord,
                                 font=ctk.CTkFont(size=12), width=70)
            cb.select()
            cb.grid(row=1, column=i, padx=6, pady=(0, 10))
            self._custom_checks[chord] = cb

    # ── Callbacks ─────────────────────────────────────────────────────────────

    def _on_key_change(self, _=None):
        self._build_custom_frame()

    def _on_difficulty_change(self, val):
        if val == 'Custom':
            self.custom_frame.grid(row=3, column=0, padx=24, pady=4, sticky="ew")
        else:
            self.custom_frame.grid_remove()

    def _on_bpm_change(self, val):
        bpm = int(val)
        self.bpm_label.configure(text=str(bpm))
        if self.running and self.metronome:
            self.metronome.update_bpm(bpm)
            self.session_bpms.append(bpm)

    def _on_beats_change(self, val):
        self.beats_var.set(int(val))
        if self.running and self.metronome:
            self.metronome.update_beats(int(val))
        self._update_dots(self.current_beat)

    def _on_sound_change(self, val):
        if self.running and self.metronome:
            self.metronome.update_sound(val)

    def _on_tap_tempo(self):
        bpm = self.tap_tempo.tap()
        if bpm is not None:
            self.bpm_var.set(bpm)
            self.bpm_label.configure(text=str(bpm))
            if self.running and self.metronome:
                self.metronome.update_bpm(bpm)
                self.session_bpms.append(bpm)

    def _volume_up(self):
        set_volume(_volume + 0.1)
        self.volume_label.configure(text=f"{round(_volume * 100)}%")

    def _volume_down(self):
        set_volume(_volume - 0.1)
        self.volume_label.configure(text=f"{round(_volume * 100)}%")

    def _toggle(self):
        if self.running:
            self._stop()
        else:
            self._start_countdown()

    # ── Countdown ─────────────────────────────────────────────────────────────

    def _start_countdown(self):
        self._countdown_n = 3
        self.start_btn.configure(state="disabled")
        self.chord_label.configure(font=ctk.CTkFont(size=72, weight="bold"))
        self._tick_countdown()

    def _tick_countdown(self):
        if self._countdown_n > 0:
            self.chord_label.configure(text=str(self._countdown_n))
            self._countdown_n -= 1
            self.after(1000, self._tick_countdown)
        else:
            self.chord_label.configure(text="—")
            self.start_btn.configure(state="normal")
            self._do_start()

    # ── Start / Stop ──────────────────────────────────────────────────────────

    def _do_start(self):
        self.running            = True
        self.last_index         = None
        self.chord_num          = 0
        self.current_beat       = 1
        self.chord_history      = []
        self.session_start      = time.time()
        self.session_bpms       = [self.bpm_var.get()]
        self.session_chord_counts = {}

        self.start_btn.configure(text="Stop",
                                 fg_color="#c0392b", hover_color="#96281b")

        self.metronome = Metronome(self.bpm_var.get(), self.beats_var.get(),
                                   self._on_beat, self.sound_var.get())
        self.metronome.start()

        limit = self.timer_var.get()
        if limit != 'Off':
            ms = int(limit.split()[0]) * 60 * 1000
            self._timer_job = self.after(ms, self._timer_expired)

    def _timer_expired(self):
        if self.running:
            self._stop()

    def _stop(self):
        self.running = False
        if self._timer_job:
            self.after_cancel(self._timer_job)
            self._timer_job = None
        if self.metronome:
            self.metronome.stop()
            self.metronome = None

        if self.session_start and self.chord_num > 0:
            save_session({
                'date':           datetime.now().strftime('%Y-%m-%d %H:%M'),
                'key':            self.key_var.get(),
                'difficulty':     self.difficulty_var.get(),
                'duration_secs':  round(time.time() - self.session_start),
                'chords_played':  self.chord_num,
                'avg_bpm':        round(sum(self.session_bpms) / len(self.session_bpms)),
                'chord_counts':   self.session_chord_counts,
            })

        self.start_btn.configure(text="Start",
                                 fg_color=("#3B8ED0", "#1F6AA5"),
                                 hover_color=("#36719F", "#144870"))
        self.chord_label.configure(text="—",
                                   font=ctk.CTkFont(size=72, weight="bold"))
        self.numeral_label.configure(text="")
        self.dot_label.configure(text="")
        self.history_label.configure(text="")
        self.key_display.configure(text="Select a key and press Start")
        self.diagram.draw(None)

    # ── Beat / Chord logic ────────────────────────────────────────────────────

    def _on_beat(self, beat, accent):
        if beat == 1:
            self._pick_next_chord()
        self.current_beat = beat
        self.after(0, self._refresh_display, beat)

    def _get_available_indices(self):
        key    = self.key_var.get()
        chords = KEYS[key]
        diff   = self.difficulty_var.get()

        if diff == 'Beginner':
            idxs = [i for i, c in enumerate(chords) if c in OPEN_CHORDS]
        elif diff == 'Intermediate':
            idxs = [i for i, c in enumerate(chords)
                    if c in OPEN_CHORDS or c in BARRE_CHORDS]
        elif diff == 'Custom':
            idxs = [i for i, c in enumerate(chords)
                    if self._custom_checks.get(c) and self._custom_checks[c].get()]
        else:
            idxs = list(range(len(chords)))

        return idxs if idxs else list(range(len(chords)))

    def _pick_next_chord(self):
        key       = self.key_var.get()
        chords    = KEYS[key]
        available = [i for i in self._get_available_indices()
                     if i != self.last_index]
        if not available:
            available = self._get_available_indices()

        idx = random.choice(available)
        chord   = chords[idx]
        numeral = ROMAN_NUMERALS[idx]

        if self._next_chord != '—':
            self.chord_history.append((self._next_chord, self._next_numeral))
            if len(self.chord_history) > 3:
                self.chord_history.pop(0)

        self.last_index    = idx
        self.chord_num    += 1
        self._next_chord   = chord
        self._next_numeral = numeral
        self.session_chord_counts[chord] = \
            self.session_chord_counts.get(chord, 0) + 1

    def _refresh_display(self, beat):
        if not self.running:
            return
        if beat == 1:
            if self._next_chord in CUSTOM_SOUNDS:
                play_sound(CUSTOM_SOUNDS[self._next_chord], chord=self._next_chord)
            self.chord_label.configure(text=self._next_chord,
                                       font=ctk.CTkFont(size=72, weight="bold"))
            self.numeral_label.configure(text=f"({self._next_numeral})")
            self.key_display.configure(
                text=f"{self.key_var.get()} major  —  chord #{self.chord_num}")
            self.diagram.draw(CHORD_FINGERINGS.get(self._next_chord))

            if self.chord_history:
                hist = "  →  ".join(c for c, _ in self.chord_history)
                self.history_label.configure(text=f"↑  {hist}")
            else:
                self.history_label.configure(text="")

        self._update_dots(beat)

    def _update_dots(self, current_beat):
        beats = self.beats_var.get()
        dots  = []
        for b in range(1, beats + 1):
            if b == current_beat:
                dots.append('●')
            elif b < current_beat:
                dots.append('○')
            else:
                dots.append('·')
        self.dot_label.configure(text='  '.join(dots))


if __name__ == '__main__':
    app = ChordTrainerApp()
    app.mainloop()
