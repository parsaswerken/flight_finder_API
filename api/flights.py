# api/flights.py
import json
import os
import time
from api_client import fetch_all_us_flights  # new function to fetch ALL US flights

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "..", "flights_retrieved.txt")
APPENDED_FILE = os.path.join(BASE_DIR, "..", "flights_appended.txt")
AIRPORTS_FILE = os.path.join(BASE_DIR, "..", "Data", "airports.json")

# refresh every 24h
REFRESH_INTERVAL = 24 * 60 * 60  

# Load airports.json once
with open(AIRPORTS_FILE, "r", encoding="utf-8") as f:
    AIRPORTS = json.load(f)

def get_airports_by_city(city_name: str):
    """Return all IATA codes for a city (case-insensitive)."""
    return [
        airport["IATA"]
        for airport in AIRPORTS
        if airport["CITY"].lower() == city_name.lower()
    ]

def is_stale(file_path):
    if not os.path.exists(file_path):
        return True
    last_modified = os.path.getmtime(file_path)
    return (time.time() - last_modified) > REFRESH_INTERVAL

def refresh_cache():
    """Fetch ALL US flights for next 30 days and save to cache files."""
    flights = fetch_all_us_flights()  # <-- NEW: full universe
    # Save raw data
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(flights, f, indent=2)
    # Save simplified format
    with open(APPENDED_FILE, "w", encoding="utf-8") as f:
        for flight in flights:
            line = " || ".join([
                flight.get("departure", ""),
                flight.get("destination", ""),
                flight.get("cost", ""),
                flight.get("duration", ""),
                flight.get("tripType", ""),
                flight.get("passengerType", "")
            ])
            f.write(line + "\n")

def load_appended():
    flights = []
    if os.path.exists(APPENDED_FILE):
        with open(APPENDED_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = [p.strip() for p in line.split("||")]
                if len(parts) >= 6:
                    flights.append({
                        "departure": parts[0],
                        "destination": parts[1],
                        "cost": parts[2],
                        "duration": parts[3],
                        "tripType": parts[4],
                        "passengerType": parts[5],
                    })
    return flights

def handler(request):
    from_city = request.args.get("from", "")
    to_city = request.args.get("to", "")
    trip_type = request.args.get("tripType", "round")
    max_cost = request.args.get("maxCost")

    # refresh cache if stale
    if is_stale(CACHE_FILE):
        refresh_cache()

    # Load cached flights
    flights = load_appended()

    # Expand cities → airports
    from_airports = get_airports_by_city(from_city) if from_city else []
    to_airports = get_airports_by_city(to_city) if to_city else []

    # Apply user filters
    filtered = [
        f for f in flights
        if (not from_airports or f["departure"] in from_airports)
        and (not to_airports or f["destination"] in to_airports)
        and (not max_cost or int(f["cost"].replace("$", "").split()[0]) <= int(max_cost))
        and (not trip_type or f["tripType"].lower() == trip_type.lower())
    ]

    return {"flights": filtered}
