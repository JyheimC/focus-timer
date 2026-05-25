# Focus Timer

A Pomodoro-style productivity timer for the terminal, built with Python and [Rich](https://github.com/Textualize/rich).

## Features

- Interactive TUI with a live countdown, progress bar, and session log
- Configurable work, short break, and long break durations
- Audible alert (Windows) when each session ends
- Tracks completed sessions and daily streaks in `sessions.json`

## Requirements

- Python 3.10+
- [Rich](https://pypi.org/project/rich/) (`pip install rich`)

## Installation

```bash
git clone https://github.com/JyheimC/focus-timer.git
cd focus-timer
pip install -r requirements.txt
```

## Usage

Run interactively (prompts for durations):

```bash
python main.py
```

Or pass options directly:

```bash
python main.py --work 25 --short-break 5 --long-break 15 --sessions 4
```

| Flag | Default | Description |
|------|---------|-------------|
| `--work` | 25 | Work session length (minutes) |
| `--short-break` | 5 | Short break length (minutes) |
| `--long-break` | 15 | Long break length (minutes) |
| `--sessions` | 4 | Work sessions before a long break |

Press `Ctrl+C` at any time to stop and see your daily summary.
