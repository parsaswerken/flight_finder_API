from file_manager import load_appended
from filters import filter_by_city, filter_by_cost, filter_by_trip_type, filter_by_passenger_type


def handler(request, response):
    """
    Python serverless function for Vercel.
    reads query params, applies filters, and returns JSON.
    """
    return response.json({
        "status": "ok",
        "note": "Python flights API is live!"
    })

    try:
        # Extract query params
        params = request.get("query", {})
        departure = params.get("departure", "")
        arrival = params.get("arrival", "")
        max_price = int(params.get("max_price", "0")) if "max_price" in params else None
        trip_type = params.get("trip_type", "")
        passenger_type = params.get("passenger_type", "")

        # Load cached/appended flights
        flights = load_appended()

        # Apply filters
        if departure or arrival:
            flights = filter_by_city(flights, departure, arrival)
        if max_price:
            flights = filter_by_cost(flights, max_price)
        if trip_type:
            flights = filter_by_trip_type(flights, trip_type)
        if passenger_type:
            flights = filter_by_passenger_type(flights, passenger_type)

        # Always return JSON
        return response.json({"flights": flights})

    except Exception as e:
        return response.json({"error": str(e)}, status=500)
