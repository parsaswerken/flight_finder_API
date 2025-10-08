# api_client.py
import os
import requests
from datetime import datetime, timedelta

# Load SerpAPI key from environment
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def fetch_all_us_flights():
    """
    Fetch all domestic US flights for a rolling 2-week window.
    Returns a list of dicts with standard fields.
    """
    if not SERPAPI_KEY:
        raise ValueError("SERPAPI_KEY not set in environment")

    today = datetime.today()
    start_date = today.strftime("%Y-%m-%d")
    end_date = (today + timedelta(days=14)).strftime("%Y-%m-%d")

    url = "https://serpapi.com/search"
    params = {
        "engine": "google_flights",
        "departure_id": "United States",   # all US departures
        "arrival_id": "United States",     # all US arrivals
        "currency": "USD",
        "hl": "en",
        "outbound_date": f"{start_date}:{end_date}",  # rolling 2 weeks
        "return_date": f"{start_date}:{end_date}",
        "api_key": SERPAPI_KEY,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    flights = []
    for flight in data.get("flights", []):
        flights.append({
            "departure": flight.get("departure_airport", {}).get("id", ""),
            "destination": flight.get("arrival_airport", {}).get("id", ""),
            "cost": flight.get("price", ""),
            "duration": flight.get("duration", ""),
            "tripType": "round" if flight.get("return") else "oneway",
            "passengerType": "adult",  # default for now
        })

    return flights

# Simple test runner
if __name__ == "__main__":
    try:
        flights = fetch_all_us_flights()
        print(f"Retrieved {len(flights)} flights")
        print(flights[:5])  # print first 5 sample flights
    except Exception as e:
        print("Error fetching flights:", e)
