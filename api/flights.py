import os
import json
import time
from api_client import fetch_all_us_flights

# Cache file (stored in the same directory as flights.py)
CACHE_FILE = os.path.join(os.path.dirname(__file__), "flights_cache.json")
CACHE_TTL = 24 * 3600  # 24 hours in seconds


def is_cache_valid():
    """Check if cache exists and is younger than 24h"""
    return os.path.exists(CACHE_FILE) and (time.time() - os.path.getmtime(CACHE_FILE)) < CACHE_TTL


def load_cached_flights():
    """Load cached flights from file"""
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cached_flights(data):
    """Save flights to cache"""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_flights():
    """Return flights (from cache or API if expired)"""
    if is_cache_valid():
        print("Using cached flights")
        return load_cached_flights()

    print("🌍 Fetching fresh flights from SerpAPI...")
    flights = fetch_all_us_flights(
        # Example: fetch all flights in a 2-week window
        outbound_date="2025-10-15",
        return_date="2025-10-29"
    )
    save_cached_flights(flights)
    return flights


# 🔹 This is the entrypoint Vercel calls for /api/flights
def handler(request):
    try:
        flights = get_flights()
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"flights": flights})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


# 🔹 Run locally with: python api/flights.py
if __name__ == "__main__":
    result = get_flights()
    print(json.dumps(result[:3], indent=2))  # show first 3 results
