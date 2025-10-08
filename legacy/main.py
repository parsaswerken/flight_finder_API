from api_client import fetch_all_us_flights
from api.file_manager import is_cache_valid, save_appended, load_appended
from api.filters import filter_by_city, filter_by_cost, filter_by_trip_type, filter_by_passenger_type


def main():
    # Step 1: Ensure cache is fresh
    if not is_cache_valid():
        print(" Fetching fresh flights from API...")
        flights = fetch_all_us_flights()  # already returns list of flights
        print(f" Retrieved {len(flights)} flights")
        save_appended(flights)
    else:
        print(" Using cached flights (flights_appended.txt)")

    # Step 2: Load flights
    flights = load_appended()
    print(f" Loaded {len(flights)} flights from cache")

    # Step 3: Interactive filters
    departure = input("Enter departure city (or press Enter to skip): ").strip()
    arrival = input("Enter arrival city (or press Enter to skip): ").strip()
    max_price = input("Enter maximum price (or press Enter to skip): ").strip()
    trip_type = input("Enter trip type (Round trip / One way) [or skip]: ").strip()
    passenger_type = input("Passenger type (Adult/Child/Infant) [default Adult]: ").strip()

    # Step 4: Apply filters
    if departure or arrival:
        flights = filter_by_city(flights, departure=departure, arrival=arrival)
    if max_price:
        flights = filter_by_cost(flights, max_price=int(max_price))
    if trip_type:
        flights = filter_by_trip_type(flights, trip_type)
    if passenger_type:
        flights = filter_by_passenger_type(flights, passenger_type)

    # Step 5: Display results
    print("\n Available Flights:\n")
    if not flights:
        print(" No flights matched your filters.")
    else:
        for line in flights[:10]:  # limit to first 10
            print(line)


if __name__ == "__main__":
    main()
