import { useRouter } from "next/router";
import { useEffect, useState } from "react";

export default function Results() {
  const router = useRouter();
  const { from, to, tripType, maxCost } = router.query;
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!router.isReady) return;

    const fetchFlights = async () => {
      try {
        const res = await fetch("/api/flights");
        const data = await res.json();

        // apply filters client-side
        const filtered = data.flights.filter((f) => {
          return (
            (!from || f.from.toLowerCase().includes(from.toLowerCase())) &&
            (!to || f.to.toLowerCase().includes(to.toLowerCase())) &&
            (!tripType || f.type === tripType) &&
            (!maxCost || f.cost <= parseInt(maxCost))
          );
        });

        setFlights(filtered);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchFlights();
  }, [router.isReady, from, to, tripType, maxCost]);

  if (loading) return <p>Loading flights...</p>;

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Available Flights</h1>
      <p>Filters: From {from} → To {to} | {tripType} | Max ${maxCost}</p>

      {flights.length === 0 ? (
        <p>No flights found.</p>
      ) : (
        <ul>
          {flights.map((f, i) => (
            <li key={i}>
              {f.from} → {f.to} | ${f.cost} + tax | {f.duration} | {f.type}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
