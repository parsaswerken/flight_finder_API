from typing import Optional

def filter_by_city(lines: list[str], departure: Optional[str] = None, arrival: Optional[str] = None) -> list[str]:
    """Filter flights by departure and/or arrival city."""
    result = []
    for line in lines:
        parts = line.split("||")
        if len(parts) < 2:
            continue
        dep_city, arr_city = parts[0].strip(), parts[1].strip()
        if departure and departure.lower() not in dep_city.lower():
            continue
        if arrival and arrival.lower() not in arr_city.lower():
            continue
        result.append(line)
    return result


def filter_by_cost(lines: list[str], max_price: Optional[int] = None) -> list[str]:
    """Filter flights by maximum cost in USD."""
    if not max_price:
        return lines
    result = []
    for line in lines:
        parts = line.split("||")
        if len(parts) < 3:
            continue
        cost_str = parts[2].strip().replace("$", "").split()[0]
        try:
            cost = int(cost_str)
            if cost <= max_price:
                result.append(line)
        except ValueError:
            continue
    return result


def filter_by_trip_type(lines: list[str], trip_type: Optional[str] = None) -> list[str]:
    """Filter flights by type (Round trip, One way, Multi-city)."""
    if not trip_type:
        return lines
    return [line for line in lines if trip_type.lower() in line.lower()]


def filter_by_passenger_type(lines: list[str], passenger_type: Optional[str] = None) -> list[str]:
    """Filter flights by passenger type (Adult, Child, Infant)."""
    if not passenger_type:
        return lines
    return [line for line in lines if passenger_type.lower() in line.lower()]
