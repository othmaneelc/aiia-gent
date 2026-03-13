from datetime import datetime
from dateutil import tz

TZ_NAME = "Africa/Casablanca"

def now_local():
    return datetime.now(tz=tz.gettz(TZ_NAME))

def today_local_str():
    return now_local().strftime("%Y-%m-%d")

def is_send_window(target_hour=8, target_minute=0, window_minutes=14):
    """
    Because GitHub Actions runs every 15 min, we allow a window:
    send if local time is between HH:MM and HH:MM+window_minutes inclusive.
    """
    n = now_local()
    if n.hour != target_hour:
        return False
    return target_minute <= n.minute <= (target_minute + window_minutes)
