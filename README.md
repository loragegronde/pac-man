*This project has been created as part of the 42 curriculum by acampion and eel-kerc.*

# Pac-Man

Here is our implementation of Pac-Man for the 42 curriculum. You move Pac-Man through a
procedurally generated maze, eat pac-gums, dodge (or eat) four ghosts, and try
to clear ten levels before the timer or your lives run out.

The game reads a JSON config, opens a fixed-size window, and moves through a
simple state machine: menu → playing → pause / cheats → victory or game over.
Mazes come from the A-Maze-ing package (`mazegenerator`) that we were assigned,
and everything is drawn with pygame, using only primitives that map cleanly to
MLX.

## Getting started

You'll need Python 3.13+ and [uv](https://github.com/astral-sh/uv).

```bash
make install   # runs uv sync, including the local mazegenerator wheel
make run       # starts the game with config.json
make lint      # flake8 + mypy
```

`make run` is just a shortcut for:

```bash
uv run python3 pac-man.py config.json
```

To use a different config, pass its path as the first argument:

```bash
uv run python3 pac-man.py path/to/config.json
```

### Controls

| Input | Action |
|-------|--------|
| Arrow keys | Move Pac-Man |
| `ENTER` / `SPACE` | Start / confirm |
| `ESC` | Pause in-game, go back from overlays, quit from the menu |
| Mouse | Click menu buttons, scroll the highscores |

## Configuration

The game is configured through a JSON file (`config.json` by default). Comments
work too, thanks to `commentjson`: use `#` for single lines and `//` for blocks.

| Key | Type | Default | What it does |
|-----|------|---------|--------------|
| `highscore_filename` | string ending in `.json` | `"highscore.json"` | Where highscores are saved |
| `lives` | positive int | `3` | Starting lives |
| `pacgum` | positive int | `42` | Normal pac-gums per level |
| `points_per_pacgum` | positive int | `10` | Points for a normal pac-gum |
| `points_per_super_pacgum` | positive int | `50` | Points for a super pac-gum |
| `points_per_ghost` | positive int | `200` | Base points for eating a ghost |
| `seed` | any, optional | `null` | Maze seed (see Maze generation) |
| `level_max_time` | positive int | `90` | Seconds per level |
| `fps` | positive int | `60` | Target frame rate |

If a key is missing or invalid, we fall back to the default and print a
warning. Unknown keys are ignored. The window size is hardcoded at 1900×1200.

Example:

```json
{
  "highscore_filename": "highscore.json",
  "lives": 3,
  "pacgum": 100,
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,
  "seed": 42,
  "level_max_time": 90,
  "fps": 120
}
```

## Highscores

Scores live in a plain JSON array of `{ "name": string, "score": int }` objects,
in the file set by `highscore_filename`.

When the game loads the file, it skips invalid entries, cuts names down to 10
characters, and only accepts non-negative integer scores. The list is then
sorted from highest to lowest. After a victory or game over, you type in your
name and the new entry is added, re-sorted, and saved. The main menu shows a
scrollable list and highlights your latest score when it can.

We went with a flat JSON file because it's easy to read and edit by hand, needs
no database, and matches how we handle config. It also means friends can
compete across sessions without touching the code.

## Maze generation

Mazes are built by `mazegenerator`, which we ship as the local wheel
`mazegenerator-2.1.0-py3-none-any.whl` (declared in `pyproject.toml`).

Our `Maze` class (`src/visual/maze.py`) creates a `MazeGenerator(size, seed=...)`
and reads its `.maze` grid. Each cell is an integer bitmask of its walls:
N = `1`, E = `2`, S = `4`, W = `8`. A value of `15` means the cell is solid
(like the "42" cells) and can't be walked on.

The generator can also braid the maze by removing dead ends, which keeps the
chase loops fair for Pac-Man. From there we draw the walls pixel by pixel,
corner joints included, onto a pygame surface, set solid cells back to `15` for
gameplay, and scatter pac-gums over the walkable cells.

There are ten levels, each a pre-built `GameMode` on a 15×15 grid with faster
ghosts as you go. The first level can be seeded so it's reproducible. Later
levels may use an unseeded generator to keep things fresh.

## How it works

- **Startup:** `pac-man.py` parses the config (`Parsing` + a pydantic `Config`)
  and hands it to `Graphics`.
- **Scenes:** `Graphics` switches between `menu`, `instructions`, `playing`,
  `pause`, `cheats`, `victory`, and `game_over`.
- **Levels:** `LevelHandler` owns the ten `GameMode` instances, plus lives,
  timer, score, HUD, and the transitions after a death or level clear.
- **Entities:** `Player` and the `Enemy` subclasses move on a 50-pixel grid.
  Their centres sit where `x % 50 == y % 50 == 7`.
- **Ghosts:**
  - Blinky chases Pac-Man, and runs to a far corner when scared.
  - Pinky aims for the cell behind Pac-Man.
  - Clyde aims for the cell ahead.
  - Inky just picks a random open direction.
  - Paths are found with the BFS helpers in `pathfinding.py`. Eaten ghosts head
    home by interpolating from cell to cell (`go_home`).
- **Scoring:** pac-gums, super pac-gums (which scare the ghosts), and ghost
  combos during the short freeze after you eat one.
- **UI:** pygame surfaces and fonts, with panels drawn using our own rounded
  rect outlines. Asset sizes are hardcoded to keep an MLX port simple.
- **Cheats:** available from the pause menu: invincibility, a single pac-gum,
  ghosts that always chase, frozen ghosts, and tweaks to level, lives, and
  speed.

### Project layout

```text
pac-man.py
    └── Graphics                    # window loop, input, scene state
            ├── Menu / Instructions / Pause / CheatMenu
            ├── Victory / GameOver / NameBox
            ├── Highscores
            ├── Assets              # images, fonts, layout constants
            └── LevelHandler        # the 10-level campaign
                    ├── Hud
                    └── GameMode[]  # one maze + entities per level
                            ├── Maze (+ MazeGenerator)
                            ├── Player
                            └── EnemyHandler
                                    ├── Blinky / Pinky / Clyde / Inky
                                    └── pathfinding helpers
```

| Module | What it does |
|--------|--------------|
| `src/parsing.py` | Loads and validates `config.json` |
| `src/graphics.py` | Main loop and scene routing |
| `src/menu.py`, `instructions.py`, `pause.py`, `cheat_menu.py` | Menus and overlays |
| `src/highscores.py` | Reads and writes the highscore JSON |
| `src/assets.py` | Sprites, fonts, layout |
| `src/visual/level_handler.py` | Level progression and HUD updates |
| `src/visual/game.py` | Simulation of a single level |
| `src/visual/maze.py` | Generator wrapper and wall drawing |
| `src/visual/player.py` | Pac-Man movement |
| `src/visual/enemy*.py` | Ghost base class and personalities |
| `src/visual/pathfinding.py` | BFS path helpers |

## Features

- Ten levels with increasingly fast ghosts
- Four ghosts with their own behaviour, plus scared, dead, and return-home states
- Configurable lives, pac-gum count, scoring, timer, and FPS
- Persistent highscores with name entry
- Pause menu and a debug cheat menu
- In-game instructions for controls and rules

## MLX equivalents in pygame

If we port this to MLX someday, here's how the calls line up:

| MLX | pygame |
|-----|--------|
| `mlx_init()` | `pygame.init()` |
| `mlx_release()` / `mlx_destroy_display()` | `pygame.quit()` |
| `mlx_new_window(w, h, title)` | `pygame.display.set_mode((w, h))` + `pygame.display.set_caption(title)` |
| `mlx_clear_window()` | `surface.fill((0, 0, 0))` |
| `mlx_destroy_window()` | `pygame.display.quit()` |
| `mlx_pixel_put(x, y, color)` | `surface.set_at((x, y), color_rgb)` |
| `mlx_string_put(x, y, color, text)` | `font.render(text, True, color_rgb)` + `screen.blit(surf, (x, y))` |
| `mlx_new_image(w, h)` | `pygame.Surface((w, h))` |
| `mlx_put_image_to_window(x, y)` | `screen.blit(surface, (x, y))` |
| `mlx_png_file_to_image(filename)` | `pygame.image.load(filename).convert_alpha()` |
| `mlx_loop()` | `while running: pygame.event.get()` |
| `mlx_key_hook(callback)` | handle `pygame.KEYDOWN` events |
| `mlx_mouse_hook(callback)` | handle `pygame.MOUSEBUTTONDOWN` events |
| `mlx_mouse_get_pos()` | `pygame.mouse.get_pos()` |
| `mlx_do_sync()` | `pygame.display.flip()` |

## Project management

There are two of us, **acampion** and **eel-kerc**. One focused on parsing,
UI nad made the ghosts, the other on gameplay and all maze related task. Tasks, owners, and status are tracked in
[project_management/](project_management/).

## Resources

- [Pac-Man on Wikipedia](https://en.wikipedia.org/wiki/Pac-Man) for the rules and history
- [The Pac-Man Dossier](https://www.gamedeveloper.com/design/the-pac-man-dossier) by Jamey Pittman, the go-to reference for ghost behaviour and timing
- [pygame docs](https://www.pygame.org/docs/) for display, events, surfaces, and fonts
- [pydantic docs](https://docs.pydantic.dev/) for config validation
- A-Maze-ing (`mazegenerator`), the maze package we were given, included as a local wheel
- 42's MiniLibX (MLX), which the table above maps to pygame

### How we used AI

**Acampion** used AI assistants to speed things
up, not to design the game. Specifically, they helped with:

- **UI polish:** menu buttons (Exit, Instructions), layout offsets, and text
  alignment on the highscore, victory, and game-over screens (the repeated and boring task).
- **Documentation:** a first draft of this README, based on the subject
  checklist and our code
- **Algorithms:** BFS pathfinding for ghost movement.

The core gameplay was designed and written by us: the maze bitmask logic, the
ghost personalities, and the movement maths. Ai was used to help with the boring parts, not to design the game.

**Eel-kerc** used AI for git (understanding rebase, merge and visualisation) and pygame usage understanding.   
No AI was used for any other part of the project.   

## Authors

- **acampion**: parsing, menus, highscores, ghost
- **eel-kerc**: maze and gameplay, project management