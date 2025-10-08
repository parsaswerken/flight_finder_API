# api/api_client.py
import os
import requests
from datetime import datetime, timedelta

API_KEY = os.getenv("SERPAPI_KEY")  # Load from .env
BASE_URL = "https://serpapi.com/search.json"

# Default airports (you can expand later or use your airports.json)
US_AIRPORTS = ["JFK", "LAX", "ORD", "ATL", "DFW", "DEN", "SFO", "MIA", "SEA", "BOS"]


def fetch_all_us_flights(days_ahead: int = 14, window: int = 14):
    """
    Fetches flights between major US airports within a given time frame.
    Example: From today+days_ahead until today+days_ahead+window
    """

    flights = []

    outbound_date = (datetime.today() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
    return_date = (datetime.today() + timedelta(days=days_ahead + window)).strftime("%Y-%m-%d")

    for i, dep in enumerate(US_AIRPORTS):
        for j, arr in enumerate(US_AIRPORTS):
            if i == j:
                continue  # skip same airport
            params = {
                "engine": "google_flights",
                "departure_id": dep,
                "arrival_id": arr,
                "outbound_date": outbound_date,
                "return_date": return_date,
                "type": "2",  # round trip
                "adults": "1",
                "currency": "USD",
                "hl": "en",
                "api_key": API_KEY,
            }

            print(f"Fetching {dep} -> {arr} ...")
            response = requests.get(BASE_URL, params=params)

            if response.status_code == 200:
                data = response.json()
                flights.append(data)
            else:
                print(f"❌ Failed to fetch {dep}->{arr}: {response.status_code}")

    return flights
