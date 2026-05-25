from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

SESSION_COLORS = {
    "Work": "bold red",
    "Short Break": "bold green",
    "Long Break": "bold cyan",
}


class TimerDisplay:
    def __init__(self):
        self._progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        self._task_id = None
        self._live = Live(console=console, refresh_per_second=4)
        self._log_rows: list[tuple[str, str, str]] = []

    def start(self):
        self._live.start()

    def stop(self):
        self._live.stop()

    def new_session(self, session_type: str, total_seconds: float):
        self._progress = Progress(
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        self._task_id = self._progress.add_task("", total=total_seconds)

    def update(self, elapsed: float, remaining: float, session_type: str, session_num: int, total_sessions: int):
        self._progress.update(self._task_id, completed=elapsed)
        mins, secs = divmod(int(remaining), 60)
        clock = Text(f"{mins:02d}:{secs:02d}", style="bold white", justify="center")
        color = SESSION_COLORS.get(session_type, "white")
        label = Text(f"  {session_type}  •  #{session_num} / {total_sessions}", style=color, justify="center")

        clock_panel = Panel(
            Text.assemble("\n", clock, "\n", label, "\n"),
            box=box.ROUNDED,
            padding=(0, 4),
        )

        log_table = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
        log_table.add_column("Time", style="dim", width=10)
        log_table.add_column("Type", width=14)
        log_table.add_column("Duration", justify="right", width=10)
        for row in self._log_rows[-8:]:
            log_table.add_row(*row)

        layout = Layout()
        layout.split_column(
            Layout(clock_panel, name="clock", size=8),
            Layout(self._progress, name="bar", size=3),
            Layout(log_table, name="log"),
        )
        self._live.update(layout)

    def add_log_row(self, time_str: str, session_type: str, duration_min: float):
        self._log_rows.append((time_str, session_type, f"{duration_min:.0f} min"))

    def show_summary(self, count: int, total_min: float, streak: int):
        self._live.stop()
        streak_label = f"  {streak}-day streak" if streak > 1 else ""
        summary = Text.assemble(
            "\nToday: ",
            (f"{count}", "bold yellow"),
            f" session{'s' if count != 1 else ''} · ",
            (f"{total_min:.0f} min", "bold green"),
            " focused",
            ("" if not streak_label else f" · {streak_label}"),
            "\n",
        )
        console.print(Panel(summary, title="[bold]Session Summary[/bold]", box=box.ROUNDED))
