import json
import os
from datetime import datetime, timedelta

_FILE = os.path.join(os.path.dirname(__file__), "sessions.json")


def load_sessions() -> list:
    if not os.path.exists(_FILE):
        return []
    with open(_FILE, "r") as f:
        return json.load(f)


def save_session(session_type: str, duration_min: float):
    sessions = load_sessions()
    sessions.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": session_type,
        "duration_min": round(duration_min, 1),
        "completed_at": datetime.now().strftime("%I:%M %p"),
    })
    with open(_FILE, "w") as f:
        json.dump(sessions, f, indent=2)


def daily_summary(date: str | None = None) -> dict:
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    sessions = load_sessions()
    today = [s for s in sessions if s["date"] == date and s["type"] == "Work"]
    streak = _compute_streak(sessions, date)
    return {
        "count": len(today),
        "total_min": sum(s["duration_min"] for s in today),
        "streak": streak,
    }


def _compute_streak(sessions: list, end_date: str) -> int:
    work_dates = sorted({s["date"] for s in sessions if s["type"] == "Work"})
    if not work_dates or end_date not in work_dates:
        return 0
    streak = 1
    current = datetime.strptime(end_date, "%Y-%m-%d")
    while True:
        prev = (current - timedelta(days=1)).strftime("%Y-%m-%d")
        if prev in work_dates:
            streak += 1
            current = current - timedelta(days=1)
        else:
            break
    return streak
