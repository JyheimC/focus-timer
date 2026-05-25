import argparse
import sys
from datetime import datetime

from rich.console import Console
from rich.prompt import IntPrompt
from rich.rule import Rule

from display import TimerDisplay
from sound import play_alert
from stats import daily_summary, save_session
from timer import run_timer

console = Console()


def interactive_setup() -> tuple[int, int, int, int]:
    console.print()
    console.print(Rule("[bold cyan]Focus Timer Setup[/bold cyan]"))
    console.print()
    work = IntPrompt.ask("  Work duration (minutes)", default=25)
    short_break = IntPrompt.ask("  Short break (minutes)", default=5)
    long_break = IntPrompt.ask("  Long break (minutes)", default=15)
    sessions = IntPrompt.ask("  Sessions before long break", default=4)
    console.print()
    return work, short_break, long_break, sessions


def run_session(display: TimerDisplay, session_type: str, duration_min: float, session_num: int, total_sessions: int):
    total_seconds = duration_min * 60
    display.new_session(session_type, total_seconds)

    for elapsed, remaining in run_timer(total_seconds):
        display.update(elapsed, remaining, session_type, session_num, total_sessions)

    play_alert()
    time_str = datetime.now().strftime("%I:%M %p")
    display.add_log_row(time_str, session_type, duration_min)
    if session_type == "Work":
        save_session("Work", duration_min)
    else:
        save_session(session_type, duration_min)


def main():
    parser = argparse.ArgumentParser(description="Focus Timer — Pomodoro TUI")
    parser.add_argument("--work", type=float, default=None, help="Work session duration in minutes")
    parser.add_argument("--short-break", type=float, default=None, dest="short_break")
    parser.add_argument("--long-break", type=float, default=None, dest="long_break")
    parser.add_argument("--sessions", type=int, default=None, help="Sessions before a long break")
    args = parser.parse_args()

    using_cli = any(v is not None for v in [args.work, args.short_break, args.long_break, args.sessions])

    if using_cli:
        work = args.work or 25
        short_break = args.short_break or 5
        long_break = args.long_break or 15
        sessions_before_long = args.sessions or 4
    else:
        work, short_break, long_break, sessions_before_long = interactive_setup()

    display = TimerDisplay()
    display.start()

    session_num = 0
    try:
        while True:
            session_num += 1
            run_session(display, "Work", work, session_num, sessions_before_long)

            if session_num % sessions_before_long == 0:
                run_session(display, "Long Break", long_break, session_num, sessions_before_long)
                session_num = 0
            else:
                run_session(display, "Short Break", short_break, session_num, sessions_before_long)

    except KeyboardInterrupt:
        summary = daily_summary()
        display.show_summary(summary["count"], summary["total_min"], summary["streak"])
        sys.exit(0)


if __name__ == "__main__":
    main()
