from api_client import fetch_flights
from file_manager import is_cache_valid, save_appended, load_appended
from filters import filter_by_city, filter_by_cost, filter_by_trip_type, filter_by_passenger_type


def format_flights(raw_json: dict) -> list[dict]:
    """Convert SerpApi JSON into simplified dicts for flights_appended.txt"""
    flights = raw_json.get("best_flights", []) + raw_json.get("other_flights", [])
    formatted = []
    for f in flights:
        flights_data = f.get("flights", [])
        if not flights_data:
            continue
        departure_city = flights_data[0]["departure_airport"]["name"]
        arrival_city = flights_data[-1]["arrival_airport"]["name"]
        price = f.get("price", 0)
        total_minutes = f.get("total_duration", 0)
        hours, mins = divmod(total_minutes, 60)
        duration_str = f"{hours}h {mins}m"
        trip_type = f.get("type", "Unknown")
        passenger_type = "Adult"  # default
        formatted.append({
            "departure_city": departure_city,
            "arrival_city": arrival_city,
            "price": price,
            "duration": duration_str,
            "trip_type": trip_type,
            "passenger_type": passenger_type,
        })
    return formatted


def main():
    if not is_cache_valid():
        print("Fetching fresh flights from API...")
        data = fetch_flights(
            departure_id="DFW",
            arrival_id="LAX",
            outbound_date="2025-11-10",
            return_date="2025-11-17",
            trip_type="1",
            adults=1,
            max_price=600
        )
        formatted = format_flights(data)
        print(f"Formatted {len(formatted)} flights")
        save_appended(formatted)
    else:
        print("Using cached flights (flights_appended.txt)")

    flights = load_appended()
    print(f"Loaded {len(flights)} flights from flights_appended.txt")

    # Apply filters
    flights = filter_by_city(flights, departure="Dallas", arrival="Los Angeles")
    flights = filter_by_cost(flights, max_price=500)
    flights = filter_by_trip_type(flights, "Round trip")
    flights = filter_by_passenger_type(flights, "Adult")

    print("\nAvailable Flights:\n")
    if not flights:
        print("No flights matched your filters.")
    for line in flights[:10]:
        print(line)


if __name__ == "__main__":
    main()
