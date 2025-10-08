import os
import requests

API_KEY = os.getenv("SERPAPI_KEY")  # Make sure this is set in Vercel!

BASE_URL = "https://serpapi.com/search.json"


def fetch_all_us_flights(
    departure="JFK", 
    arrival="LAX",
    outbound_date=None,
    return_date=None,
    trip_type="1",   # 1 = round-trip, 2 = one-way
    adults=1,
    children=0,
    infants=0,
    max_price=None
):
    """
    Fetch flights from SerpAPI Google Flights engine.
    Allows specifying outbound_date and return_date.
    """

    params = {
        "engine": "google_flights",
        "departure_id": departure,
        "arrival_id": arrival,
        "currency": "USD",
        "hl": "en",
        "api_key": API_KEY,
        "type": trip_type,
        "adults": adults,
        "children": children,
        "infants_in_seat": infants,
    }

    if outbound_date:
        params["outbound_date"] = outbound_date
    if return_date and trip_type == "1":  # only for round trip
        params["return_date"] = return_date
    if max_price:
        params["max_price"] = max_price

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"API request failed: {response.text}")

    return response.json()
