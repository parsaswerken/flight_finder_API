import os
import json
import time
from api_client import fetch_all_us_flights  # your SerpAPI client

# File to cache API results
CACHE_FILE = os.path.join(os.path.dirname(__file__), "flights_cache.json")
CACHE_TTL = 24 * 3600  # 24 hours


def is_cache_valid() -> bool:
    """Check if the cache file exists and is younger than 24h."""
    if not os.path.exists(CACHE_FILE):
        return False
    age = time.time() - os.path.getmtime(CACHE_FILE)
    return age < CACHE_TTL


def load_cached_flights() -> list:
    """Load flights from cache file."""
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cached_flights(data: list):
    """Save flights to cache file."""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_flights() -> list:
    """
    Return flights:
    - from cache if fresh (<24h),
    - otherwise fetch from API and update cache.
    """
    if is_cache_valid():
        print("✅ Using cached flights")
        return load_cached_flights()
    else:
        print("🌍 Fetching new flights from API...")
        # You may want to pass date ranges here (e.g., 2 weeks window)
        flights = fetch_all_us_flights()
        save_cached_flights(flights)
        return flights


# ---------------------------
# For local testing
# ---------------------------
if __name__ == "__main__":
    flights = get_flights()
    print(f"Loaded {len(flights)} flights")
    # Show first 3 flights for sanity check
    for f in flights[:3]:
        print(f)
