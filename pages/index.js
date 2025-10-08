import { useState } from "react";
import { useRouter } from "next/router";
import airports from "../publicairports.json";

export default function Home() {
  const router = useRouter();
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const [tripType, setTripType] = useState("round");
  const [maxCost, setMaxCost] = useState("");

  // filter airports list for suggestions
  const filterAirports = (input) => {
    if (!input) return [];
    return airports
      .filter((a) =>
        (a.CITY + " " + a.IATA + " " + a.AIRPORT)
          .toLowerCase()
          .includes(input.toLowerCase())
      )
      .slice(0, 10); // limit suggestions
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // redirect with filters as query params
    router.push(
      `/results?from=${from}&to=${to}&tripType=${tripType}&maxCost=${maxCost}`
    );
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Flight Finder</h1>
      <form onSubmit={handleSubmit}>
        {/* FROM AIRPORT INPUT */}
        <input
          list="fromOptions"
          placeholder="From Airport"
          value={from}
          onChange={(e) => setFrom(e.target.value)}
        />
        <datalist id="fromOptions">
          {filterAirports(from).map((a, i) => (
            <option key={i} value={`${a.CITY} (${a.IATA}) - ${a.AIRPORT}`} />
          ))}
        </datalist>

        {/* TO AIRPORT INPUT */}
        <input
          list="toOptions"
          placeholder="To Airport"
          value={to}
          onChange={(e) => setTo(e.target.value)}
        />
        <datalist id="toOptions">
          {filterAirports(to).map((a, i) => (
            <option key={i} value={`${a.CITY} (${a.IATA}) - ${a.AIRPORT}`} />
          ))}
        </datalist>

        {/* TRIP TYPE */}
        <select
          value={tripType}
          onChange={(e) => setTripType(e.target.value)}
        >
          <option value="round">Round Trip</option>
          <option value="oneway">One Way</option>
        </select>

        {/* MAX COST */}
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
