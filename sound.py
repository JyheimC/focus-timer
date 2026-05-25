import threading


def _beep():
    try:
        import winsound
        winsound.Beep(880, 300)
        winsound.Beep(1100, 400)
    except Exception:
        pass


def play_alert():
    threading.Thread(target=_beep, daemon=True).start()
