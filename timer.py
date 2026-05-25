import time


def run_timer(seconds: float):
    """Yield (elapsed, remaining) every second until the timer completes."""
    start = time.monotonic()
    total = seconds
    while True:
        now = time.monotonic()
        elapsed = now - start
        remaining = total - elapsed
        if remaining <= 0:
            yield total, 0
            return
        yield elapsed, remaining
        next_tick = start + round(elapsed) + 1
        sleep_for = next_tick - time.monotonic()
        if sleep_for > 0:
            time.sleep(sleep_for)
