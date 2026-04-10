# Task Tracker

## TODO

## IN PROGRESS

## DONE

- [x] Task 1: Volume Control System (Completed: 2026-04-10)
  - Added _volume global, set_volume(), afplay -v flag, +/- UI buttons, % display in session card
- [x] Task 2: Screen Responsiveness Fix (Completed: 2026-04-10)
  - Window auto-sizes to content; height clamped to screen height minus taskbar margin
  - ChordDiagram already uses relative coordinates throughout — no fixed screen positions
- [x] Task 3: Custom Sound Support (Completed: 2026-04-10)
  - _load_custom_sounds() reads main/sounds.json at startup, validates file existence
  - Invalid/missing paths silently skipped; falls back to default click track
  - Custom chord sounds play on beat 1 when chord changes
  - Example sounds.json included in main/
