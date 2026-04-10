# Claude Task Execution Protocol - Guitar Practice Tool

## SYSTEM ROLE

You are an autonomous coding agent working on an existing Python guitar
chord practice tool.

You MUST: - Follow tasks in order - Update task tracking file
continuously - Avoid breaking existing functionality - Work within the
existing project structure (do NOT enforce new structure)

------------------------------------------------------------------------

## TASK TRACKING (MANDATORY)

Maintain `todo.md` at all times.

### Format:

# Task Tracker

## TODO

-   [ ] Task name

## IN PROGRESS

-   [ ] Task name

## DONE

-   [x] Task name (Completed: YYYY-MM-DD)

------------------------------------------------------------------------

### RULES

1.  Before starting a task:
    -   Move it from TODO → IN PROGRESS
2.  While working:
    -   Add notes under the task
3.  When finished:
    -   Move it to DONE
    -   Add completion date
4.  Only ONE task may be IN PROGRESS at a time

------------------------------------------------------------------------

## EXECUTION ORDER

You MUST complete tasks in this order:

1.  Volume Control System
2.  Screen Responsiveness Fix
3.  Custom Sound Support

Do NOT skip ahead.

------------------------------------------------------------------------

## TASK 1: VOLUME CONTROL

### Requirements

-   Centralize audio logic (refactor existing code if needed)

-   Implement:

    volume = 1.0

    def set_volume(level: float): \# clamp between 0.0 and 1.0

    def play_sound(file_path: str): \# apply volume

-   Integrate with existing playback system

### UI Controls

-   '+' → increase volume
-   '-' → decrease volume

### Display

-   Show current volume in UI

### Optional

-   Persist volume setting in config

------------------------------------------------------------------------

## TASK 2: SCREEN RESPONSIVENESS

### Requirements

-   Detect terminal/window size dynamically
-   Prevent all out-of-bounds drawing

### Implementation

-   Use dynamic width/height values
-   Replace fixed coordinates with relative ones

### Safeguards

-   Clamp all draw calls
-   Handle resize if possible

------------------------------------------------------------------------

## TASK 3: CUSTOM SOUND SUPPORT

### Requirements

-   Support user-provided sound files
-   Use a mapping file (e.g. sounds.json)

Example:

{ "C": "sounds/c.wav", "G": "sounds/g.wav" }

### Implementation

-   Load mapping at startup
-   Validate file existence
-   Fallback to default sounds if missing

------------------------------------------------------------------------

## CODE QUALITY RULES

-   No hardcoded paths
-   Functions must be single-responsibility
-   Avoid duplication
-   Keep code readable

------------------------------------------------------------------------

## TESTING RULES

After EACH task:

1.  Run the program
2.  Verify:
    -   No crashes
    -   Feature works as expected
3.  Only then mark task as DONE

------------------------------------------------------------------------

## FAILURE HANDLING

If something breaks:

1.  Stop
2.  Fix issue
3.  Re-test
4.  Continue

Do NOT continue with broken functionality

------------------------------------------------------------------------

## DEFINITION OF DONE

All tasks are in DONE section AND:

-   Volume works globally
-   UI never exceeds screen bounds
-   Custom sounds load correctly
-   Program runs without errors

------------------------------------------------------------------------

## FINAL STEP

Provide a summary of: - Changes made - Files modified - Any known
limitations
