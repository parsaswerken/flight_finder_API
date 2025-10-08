import { useState, useEffect } from "react";
import { useRouter } from "next/router";

export default function Home() {
  const router = useRouter();
  const [airports, setAirports] = useState([]);
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const [tripType, setTripType] = useState("round");
  const [maxCost, setMaxCost] = useState("");

  useEffect(() => {
    fetch("/airports.json")
      .then((res) => res.json())
      .then((data) => setAirports(data));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    router.push(
      `/results?from=${from}&to=${to}&tripType=${tripType}&maxCost=${maxCost}`
    );
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Flight Finder</h1>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="From City"
          value={from}
          onChange={(e) => setFrom(e.target.value)}
          list="from-airports"
        />
        <datalist id="from-airports">
          {airports.map((airport, idx) => (
            <option key={idx} value={airport.CITY} />
          ))}
        </datalist>

        <input
          placeholder="To City"
          value={to}
          onChange={(e) => setTo(e.target.value)}
          list="to-airports"
        />
        <datalist id="to-airports">
          {airports.map((airport, idx) => (
            <option key={idx} value={airport.CITY} />
          ))}
        </datalist>

        <select value={tripType} onChange={(e) => setTripType(e.target.value)}>
          <option value="round">Round Trip</option>
          <option value="oneway">One Way</option>
        </select>

        <input
          type="number"
          placeholder="Max Cost"
          value={maxCost}
          onChange={(e) => setMaxCost(e.target.value)}
        />

        <button type="submit">Search Flights</button>
      </form>
    </div>
  );
}
