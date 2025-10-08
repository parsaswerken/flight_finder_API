import { useRouter } from "next/router";
import { useEffect, useState } from "react";

export default function Results() {
  const router = useRouter();
  const { from, to, tripType, maxCost, outbound, inbound, adults, children, infants } = router.query;

  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!from || !to) return;

    async function fetchFlights() {
      setLoading(true);

      try {
        const res = await fetch(
          `/api/flights?from=${from}&to=${to}&tripType=${tripType || "1"}&maxCost=${maxCost || ""}&outbound=${outbound || ""}&inbound=${inbound || ""}&adults=${adults || 1}&children=${children || 0}&infants=${infants || 0}`
        );

        const data = await res.json();
        setFlights(data.flights || []);
      } catch (err) {
        console.error("Error fetching flights:", err);
      }

      setLoading(false);
    }

    fetchFlights();
  }, [from, to, tripType, maxCost, outbound, inbound, adults, children, infants]);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Flight Results</h1>
      <p>
        From: {from} → To: {to} <br />
        Trip Type: {tripType} | Outbound: {outbound} | Inbound: {inbound}
      </p>

      {loading && <p>Loading flights...</p>}

      {!loading && flights.length === 0 && <p>No flights found.</p>}

      <ul>
        {flights.map((f, i) => (
          <li key={i}>
            ✈️ {f.departure_city} → {f.arrival_city} | ${f.price} | {f.duration} | {f.trip_type}
          </li>
        ))}
      </ul>
    </div>
  );
}
