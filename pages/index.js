import { useState } from "react";

export default function Home() {
  const [departure, setDeparture] = useState("");
  const [arrival, setArrival] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [flights, setFlights] = useState([]);

  const searchFlights = async () => {
    const params = new URLSearchParams({
      departure,
      arrival,
      max_price: maxPrice
    });

    const res = await fetch(`/api/flights?${params.toString()}`);
    const data = await res.json();
    setFlights(data.flights || []);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>✈️ Flight Finder</h1>

      <div style={{ marginBottom: "1rem" }}>
        <input
          type="text"
          placeholder="Departure"
          value={departure}
          onChange={(e) => setDeparture(e.target.value)}
        />
        <input
          type="text"
          placeholder="Arrival"
          value={arrival}
          onChange={(e) => setArrival(e.target.value)}
        />
        <input
          type="number"
          placeholder="Max Price"
          value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
        />
        <button onClick={searchFlights}>Search Flights</button>
      </div>

      <h2>Results:</h2>
      <ul>
        {flights.map((f, i) => (
          <li key={i}>{f}</li>
        ))}
      </ul>
    </div>
  );
}
