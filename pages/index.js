import { useState } from "react";
import { useRouter } from "next/router";

export default function Home() {
  const router = useRouter();
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const [tripType, setTripType] = useState("round");
  const [maxCost, setMaxCost] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // redirect with filters as query params
    router.push(`/results?from=${from}&to=${to}&tripType=${tripType}&maxCost=${maxCost}`);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Flight Finder</h1>
      <form onSubmit={handleSubmit}>
        <input placeholder="From City" value={from} onChange={(e) => setFrom(e.target.value)} />
        <input placeholder="To City" value={to} onChange={(e) => setTo(e.target.value)} />
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
