import random
import time
import sys
import threading
import subprocess
import shutil
import tkinter as tk
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
    # ── Open chords ──
    'C':     [-1, 3, 2, 0, 1, 0],
    'Dm':    [-1, -1, 0, 2, 3, 1],
    'Em':    [0, 2, 2, 0, 0, 0],
    'F':     [1, 1, 2, 3, 3, 1],      # full barre fret 1
    'G':     [3, 2, 0, 0, 0, 3],
    'Am':    [-1, 0, 2, 2, 1, 0],
    'Bdim':  [-1, 2, 3, 4, 3, -1],
    'D':     [-1, -1, 0, 2, 3, 2],
    'A':     [-1, 0, 2, 2, 2, 0],
    'E':     [0, 2, 2, 1, 0, 0],
    # ── Barre chords ──
    'B':     [-1, 2, 4, 4, 4, 2],     # barre 2
    'Bm':    [-1, 2, 4, 4, 3, 2],     # barre 2
    'F#m':   [2, 4, 4, 2, 2, 2],      # barre 2
    'C#m':   [-1, 4, 6, 6, 5, 4],     # barre 4
    'G#m':   [4, 6, 6, 4, 4, 4],      # barre 4
    'D#m':   [-1, 6, 8, 8, 7, 6],     # barre 6
    'Ebm':   [-1, 6, 8, 8, 7, 6],     # = D#m
    'A#m':   [-1, 1, 3, 3, 2, 1],     # barre 1
    'Bbm':   [-1, 1, 3, 3, 2, 1],     # = A#m
    'F#':    [2, 4, 4, 3, 2, 2],      # barre 2
    'Gb':    [2, 4, 4, 3, 2, 2],      # = F#
    'C#':    [-1, 4, 6, 6, 6, 4],     # barre 4
    'Db':    [-1, 4, 6, 6, 6, 4],     # = C#
    'Bb':    [-1, 1, 3, 3, 3, 1],     # barre 1
    'Eb':    [-1, 6, 8, 8, 8, 6],     # barre 6
    'Gm':    [3, 5, 5, 3, 3, 3],      # barre 3
    'Cm':    [-1, 3, 5, 5, 4, 3],     # barre 3
    'Fm':    [1, 3, 3, 1, 1, 1],      # barre 1
    'Ab':    [4, 6, 6, 5, 4, 4],      # barre 4
    # ── Diminished ──
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

ACCENT_SOUND = '/System/Library/Sounds/Tink.aiff'
BEAT_SOUND   = '/System/Library/Sounds/Pop.aiff'
HAS_AFPLAY   = shutil.which('afplay') is not None

# ── Colours (dark theme) ─────────────────────────────────────────────────────
BG_CANVAS   = '#2b2b2b'   # matches CTkFrame dark bg
DOT_COLOUR  = '#4a9eff'
MUTE_COLOUR = '#cc4444'
OPEN_COLOUR = '#aaaaaa'
FRET_COLOUR = '#555555'
STR_COLOUR  = '#777777'
NUT_COLOUR  = '#cccccc'


# ── Audio ─────────────────────────────────────────────────────────────────────
def play_tick(accent=False):
    if HAS_AFPLAY:
        sound = ACCENT_SOUND if accent else BEAT_SOUND
        subprocess.Popen(['afplay', sound],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        sys.stdout.write('\a'); sys.stdout.flush()


# ── Chord diagram ─────────────────────────────────────────────────────────────
class ChordDiagram(tk.Canvas):
    SS = 30    # string spacing (px)
    FS = 30    # fret spacing (px)
    NF = 4     # frets shown
    NS = 6     # strings
    MT = 36    # top margin  (room for X / O)
    ML = 38    # left margin (room for fret label)
    MR = 16    # right margin
    MB = 12    # bottom margin
    DR = 9     # dot radius

    def __init__(self, parent, **kwargs):
        w = self.ML + (self.NS - 1) * self.SS + self.MR
        h = self.MT + self.NF * self.FS + self.MB
        super().__init__(parent, width=w, height=h,
                         bg=BG_CANVAS, highlightthickness=0, **kwargs)

    def draw(self, frets):
        self.delete('all')
        if frets is None:
            self._draw_placeholder()
            return

        played = [f for f in frets if f > 0]
        base_fret = 1 if (not played or min(played) <= 4) else min(played)

        ml, mt, ss, fs, dr = self.ML, self.MT, self.SS, self.FS, self.DR

        # ── Nut or fret number ──
        if base_fret == 1:
            self.create_rectangle(ml, mt, ml + (self.NS - 1) * ss, mt + 5,
                                  fill=NUT_COLOUR, outline='')
        else:
            self.create_text(ml - 6, mt + fs // 2,
                             text=f"{base_fret}fr",
                             fill='#aaaaaa', font=('Arial', 9), anchor='e')
            # thin top line instead of nut
            self.create_line(ml, mt, ml + (self.NS - 1) * ss, mt,
                             fill=FRET_COLOUR, width=1)

        # ── Fret lines ──
        for i in range(1, self.NF + 1):
            y = mt + i * fs
            self.create_line(ml, y, ml + (self.NS - 1) * ss, y,
                             fill=FRET_COLOUR, width=1)

        # ── String lines ──
        for s in range(self.NS):
            x = ml + s * ss
            self.create_line(x, mt, x, mt + self.NF * fs,
                             fill=STR_COLOUR, width=1)

        # ── Detect barre: min fret across strings with span ≥ 3 ──
        barre_fret = barre_x1 = barre_x2 = None
        if played:
            min_fret = min(played)
            barre_strings = [s for s, f in enumerate(frets) if f == min_fret]
            if len(barre_strings) >= 2:
                span = barre_strings[-1] - barre_strings[0]
                if span >= 3:
                    barre_fret = min_fret
                    barre_x1   = ml + barre_strings[0]  * ss
                    barre_x2   = ml + barre_strings[-1] * ss

        # ── Draw barre bar (underneath dots) ──
        if barre_fret is not None:
            rel = barre_fret - base_fret
            if 0 <= rel < self.NF:
                y = mt + rel * fs + fs // 2
                # pill shape
                self.create_rectangle(barre_x1, y - dr, barre_x2, y + dr,
                                      fill=DOT_COLOUR, outline='')
                self.create_oval(barre_x1 - dr, y - dr, barre_x1 + dr, y + dr,
                                 fill=DOT_COLOUR, outline='')
                self.create_oval(barre_x2 - dr, y - dr, barre_x2 + dr, y + dr,
                                 fill=DOT_COLOUR, outline='')

        # ── Per-string markers ──
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
        # Fret lines
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
    def __init__(self, bpm, beats_per_chord, on_beat):
        self.interval = 60.0 / bpm
        self.beats_per_chord = beats_per_chord
        self.on_beat = on_beat
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop.set()

    def update_bpm(self, bpm):
        """Update tempo live — takes effect after the current beat."""
        self.interval = 60.0 / bpm

    def update_beats(self, beats):
        """Update beats-per-chord live."""
        self.beats_per_chord = beats

    def _run(self):
        beat = 1
        next_tick = time.perf_counter()
        while not self._stop.is_set():
            now = time.perf_counter()
            if now >= next_tick:
                accent = (beat == 1)
                play_tick(accent)
                self.on_beat(beat, accent)
                beat = (beat % self.beats_per_chord) + 1
                next_tick += self.interval
            time.sleep(0.001)


# ── Main app ──────────────────────────────────────────────────────────────────
class ChordTrainerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Guitar Chord Trainer")
        self.geometry("480x760")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.metronome    = None
        self.running      = False
        self.last_index   = None
        self.chord_num    = 0
        self.current_beat = 1
        self._next_chord  = '—'
        self._next_numeral = ''

        self._build_ui()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(self, text="Guitar Chord Trainer",
                     font=ctk.CTkFont(size=22, weight="bold")
                     ).grid(row=0, column=0, pady=(22, 4))

        # Settings card
        settings = ctk.CTkFrame(self, corner_radius=14)
        settings.grid(row=1, column=0, padx=28, pady=8, sticky="ew")
        settings.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(settings, text="Key",
                     font=ctk.CTkFont(size=12)).grid(row=0, column=0, pady=(14, 2))
        self.key_var = ctk.StringVar(value='C')
        ctk.CTkOptionMenu(settings, values=list(KEYS.keys()),
                          variable=self.key_var, width=90
                          ).grid(row=1, column=0, padx=14, pady=(0, 14))

        ctk.CTkLabel(settings, text="BPM",
                     font=ctk.CTkFont(size=12)).grid(row=0, column=1, pady=(14, 2))
        self.bpm_var = ctk.IntVar(value=60)
        bpm_frame = ctk.CTkFrame(settings, fg_color="transparent")
        bpm_frame.grid(row=1, column=1, padx=8, pady=(0, 14))
        self.bpm_label = ctk.CTkLabel(bpm_frame, text="60",
                                      font=ctk.CTkFont(size=13, weight="bold"), width=32)
        self.bpm_label.pack()
        ctk.CTkSlider(bpm_frame, from_=20, to=220, number_of_steps=200,
                      variable=self.bpm_var, width=110,
                      command=self._on_bpm_change
                      ).pack(pady=(4, 0))

        ctk.CTkLabel(settings, text="Beats / Chord",
                     font=ctk.CTkFont(size=12)).grid(row=0, column=2, pady=(14, 2))
        self.beats_var = ctk.IntVar(value=4)
        ctk.CTkSegmentedButton(settings, values=["2", "3", "4", "8"],
                               command=self._on_beats_change, width=110
                               ).grid(row=1, column=2, padx=14, pady=(0, 14))

        # Chord name card
        chord_card = ctk.CTkFrame(self, corner_radius=14)
        chord_card.grid(row=2, column=0, padx=28, pady=8, sticky="ew")
        chord_card.grid_columnconfigure(0, weight=1)

        self.key_display = ctk.CTkLabel(chord_card,
                                        text="Select a key and press Start",
                                        font=ctk.CTkFont(size=12))
        self.key_display.grid(row=0, column=0, pady=(14, 0))

        self.chord_label = ctk.CTkLabel(chord_card, text="—",
                                        font=ctk.CTkFont(size=72, weight="bold"))
        self.chord_label.grid(row=1, column=0, pady=(2, 0))

        self.numeral_label = ctk.CTkLabel(chord_card, text="",
                                          font=ctk.CTkFont(size=20),
                                          text_color="gray70")
        self.numeral_label.grid(row=2, column=0, pady=(0, 14))

        # Chord diagram card
        diagram_card = ctk.CTkFrame(self, corner_radius=14)
        diagram_card.grid(row=3, column=0, padx=28, pady=8, sticky="ew")
        diagram_card.grid_columnconfigure(0, weight=1)

        self.diagram = ChordDiagram(diagram_card)
        self.diagram.grid(row=0, column=0, pady=14)
        self.diagram.draw(None)

        # Beat dots
        self.dot_label = ctk.CTkLabel(self, text="",
                                      font=ctk.CTkFont(size=26))
        self.dot_label.grid(row=4, column=0, pady=4)

        # Start / Stop
        self.start_btn = ctk.CTkButton(self, text="Start",
                                       font=ctk.CTkFont(size=16, weight="bold"),
                                       height=48, corner_radius=12,
                                       command=self._toggle)
        self.start_btn.grid(row=5, column=0, padx=28, pady=(4, 24), sticky="ew")

    # ── Callbacks ─────────────────────────────────────────────────────────────

    def _on_bpm_change(self, val):
        bpm = int(val)
        self.bpm_label.configure(text=str(bpm))
        if self.running and self.metronome:
            self.metronome.update_bpm(bpm)      # live update

    def _on_beats_change(self, val):
        beats = int(val)
        self.beats_var.set(beats)
        if self.running and self.metronome:
            self.metronome.update_beats(beats)   # live update
        self._update_dots(self.current_beat)

    def _toggle(self):
        if self.running:
            self._stop()
        else:
            self._start()

    # ── Start / Stop ──────────────────────────────────────────────────────────

    def _start(self):
        self.running      = True
        self.last_index   = None
        self.chord_num    = 0
        self.current_beat = 1
        self.start_btn.configure(text="Stop",
                                 fg_color="#c0392b", hover_color="#96281b")
        bpm   = self.bpm_var.get()
        beats = self.beats_var.get()
        self.metronome = Metronome(bpm, beats, self._on_beat)
        self.metronome.start()

    def _stop(self):
        self.running = False
        if self.metronome:
            self.metronome.stop()
            self.metronome = None
        self.start_btn.configure(text="Start",
                                 fg_color=("#3B8ED0", "#1F6AA5"),
                                 hover_color=("#36719F", "#144870"))
        self.chord_label.configure(text="—")
        self.numeral_label.configure(text="")
        self.dot_label.configure(text="")
        self.key_display.configure(text="Select a key and press Start")
        self.diagram.draw(None)

    # ── Metronome callbacks ───────────────────────────────────────────────────

    def _on_beat(self, beat, accent):
        if beat == 1:
            self._pick_next_chord()
        self.current_beat = beat
        self.after(0, self._refresh_display, beat)

    def _pick_next_chord(self):
        key    = self.key_var.get()
        chords = KEYS[key]
        available = [i for i in range(len(chords)) if i != self.last_index]
        idx = random.choice(available)
        self.last_index    = idx
        self.chord_num    += 1
        self._next_chord   = chords[idx]
        self._next_numeral = ROMAN_NUMERALS[idx]

    def _refresh_display(self, beat):
        if not self.running:
            return
        if beat == 1:
            self.chord_label.configure(text=self._next_chord)
            self.numeral_label.configure(text=f"({self._next_numeral})")
            self.key_display.configure(
                text=f"{self.key_var.get()} major  —  chord #{self.chord_num}")
            self.diagram.draw(CHORD_FINGERINGS.get(self._next_chord))
        self._update_dots(beat)

    def _update_dots(self, current_beat):
        beats = self.beats_var.get()
        dots = []
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
