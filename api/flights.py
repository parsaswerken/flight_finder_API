import os
import json
import time
from api_client import fetch_all_us_flights

CACHE_FILE = os.path.join(os.path.dirname(__file__), "flights_cache.json")
CACHE_TTL = 24 * 3600  # 24 hours


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return None


def save_cache(data):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"timestamp": time.time(), "flights": data}, f)


def is_cache_valid():
    if not os.path.exists(CACHE_FILE):
        return False
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return time.time() - data["timestamp"] < CACHE_TTL
    except Exception:
        return False


def handler(request):
    """Vercel API handler for /api/flights"""

    params = request.args

    # Read user filters from frontend (results.js)
    departure = params.get("from")
    arrival = params.get("to")
    outbound = params.get("outbound")
    inbound = params.get("inbound")
    trip_type = params.get("tripType", "1")  # 1=round, 2=oneway
    max_price = params.get("maxCost")
    adults = int(params.get("adults", 1))
    children = int(params.get("children", 0))
    infants = int(params.get("infants", 0))

    flights = None

    # Decide whether to use cache or fetch fresh
    if is_cache_valid():
        print("✅ Using cached flights")
        cached = load_cache()
        if cached and "flights" in cached:
            flights = cached["flights"]

    if flights is None:
        print("🌍 Fetching fresh flights from SerpAPI...")
        flights = fetch_all_us_flights(
            departure=departure,
            arrival=arrival,
            outbound_date=outbound,
            return_date=inbound,
            trip_type=trip_type,
            adults=adults,
            children=children,
            infants=infants,
            max_price=max_price,
        )
        save_cache(flights)

    # Flatten response to best + other flights
    all_flights = flights.get("best_flights", []) + flights.get("other_flights", [])

    return {
        "statusCode": 200,
        "body": json.dumps({"flights": all_flights}),
        "headers": {"Content-Type": "application/json"},
    }
