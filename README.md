# Colosseum Fighters

## Files

- `main.py`, game loop, setup, spawning, win logic
- `settings.py`, constants (window size, colors, speeds, asset folder)
- `assets.py`, loads images, sounds, fonts, and sprite lists
- `entities.py`, `Fighter` and `Arrow` classes
- `ui.py`, drawing helpers (background, text, health bars)

## How to run

1. Install pygame:
   ```bash
   pip install pygame
   ```

2. Put your asset folder under:
   ```
   colosseum_fighters_refactor/
     assets/
       Colosseum Fighters Assets/
         ...
   ```

   If your assets live somewhere else, change `ASSETS_DIR` in `settings.py`.

3. Run:
   ```bash
   python main.py
   ```
