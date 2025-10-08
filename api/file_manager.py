import os
from datetime import datetime, timedelta

APPENDED_FILE = "flights_appended.txt"
CACHE_EXPIRY_HOURS = 24


def is_cache_valid() -> bool:
    """Check if appended file exists and is <24h old."""
    if not os.path.exists(APPENDED_FILE):
        return False
    mtime = datetime.fromtimestamp(os.path.getmtime(APPENDED_FILE))
    return datetime.now() - mtime < timedelta(hours=CACHE_EXPIRY_HOURS)


def save_appended(formatted: list[dict]):
    """Save formatted flights to file in human-readable format."""
    with open(APPENDED_FILE, "w", encoding="utf-8") as f:
        for flight in formatted:
            f.write(
                f"{flight['departure_city']} || "
                f"{flight['arrival_city']} || "
                f"${flight['price']} + tax || "
                f"{flight['duration']} || "
                f"{flight['trip_type']} || "
                f"{flight['passenger_type']}\n"
            )


def load_appended() -> list[str]:
    """Read formatted flights file."""
    if not os.path.exists(APPENDED_FILE):
        return []
    with open(APPENDED_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]
