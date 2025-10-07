import os
import requests
from dotenv import load_dotenv
from typing import Optional

# Load .env file
load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY") or ""


def fetch_flights(departure_id: str,
                  arrival_id: str,
                  outbound_date: str,
                  return_date: Optional[str] = None,
                  trip_type: str = "1",
                  adults: int = 1,
                  children: int = 0,
                  infants: int = 0,
                  max_price: Optional[int] = None,
                  deep_search: bool = False) -> dict:
    """
    Call SerpApi Google Flights API and return JSON results.
    trip_type: "1" = round, "2" = one way, "3" = multi-city
    """
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "currency": "USD",
        "hl": "en",
        "api_key": API_KEY,
        "type": trip_type,
        "adults": adults,
        "children": children,
        "infants_in_seat": infants,
        "deep_search": str(deep_search).lower()
    }

    if return_date and trip_type == "1":
        params["return_date"] = return_date
    if max_price:
        params["max_price"] = max_price

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
