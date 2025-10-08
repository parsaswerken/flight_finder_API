from legacy.file_manager import load_appended
from legacy.filters import filter_by_city, filter_by_cost, filter_by_trip_type, filter_by_passenger_type
from http.server import BaseHTTPRequestHandler
import json


def handler(request, response):
    """
    Python serverless function for Vercel.
    reads query params, applies filters, and returns JSON.
    """
    return response.json({
        "status": "ok",
        "note": "Python flights API is live!"
    })
    def do_GET(self):
        # Mock data just for testing UI
        flights = [
            {"departure": "Dallas-Fort Worth", "destination": "Los Angeles", "cost": "$500", "tripType": "round", "passengerType": "adult"},
            {"departure": "Dallas-Fort Worth", "destination": "Los Angeles", "cost": "$750", "tripType": "round", "passengerType": "child"},
        ]

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"flights": flights}).encode())

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
