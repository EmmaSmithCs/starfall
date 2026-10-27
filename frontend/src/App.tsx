import { useEffect, useState } from 'react';
import "./App.css";

type Approach = {
    nasa_id: string;
    name: string;
    approach_date: string;
    miss_distance_km: number;
    relative_velocity_kph: number;
    is_potentially_hazardous: boolean;
};

function App() {
    const [approaches, setApproaches] = useState<Approach[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function loadApproaches() {
            try {
                const today = new Date();
                const end = new Date(today);
                end.setDate(today.getDate() + 7);

                const formatDate = (date: Date) =>
                [
                    date.getFullYear(),
                    String(date.getMonth() + 1).padStart(2, '0'),
                    String(date.getDate()).padStart(2, '0')
                ].join('-');

                const response = await fetch(
                    `http://127.0.0.1:8000/api/approaches?start_date=${formatDate(today)}&end_date=${formatDate(end)}`
                );

                if (!response.ok) {
                    throw new Error(`COULD NOT RETRIEVE DATA: HTTP error! status: ${response.status}`);
                }

                const data: Approach[] = await response.json();
                setApproaches(data);

            } catch {
                setError("Unable to load aestroid data. Is the Starfall API running?");
            } finally {
                setLoading(false);
            }
        }
        void loadApproaches();

    }, []);

    const hazardousCount = approaches.filter(
        (approach) => approach.is_potentially_hazardous,
    ).length;

    const sortedApproaches = [...approaches].sort(
        (a,b) =>
            new Date(a.approach_date).getTime() - new Date(b.approach_date).getTime()
    )

    const formatDistance = (distance: number) => {
        return new Intl.NumberFormat("en-GB", {
            maximumFractionDigits: 0,
        }).format(distance);
    }

    return (
        <main className="dashboard">
            <header className="topbar">
                <a className="brand" href="/">
                    <span className="brand-icon">✳</span>
                    STARFALL
                </a>
                <span className="live-status">
                    <span className="status-dot" />
                    NASA DATA
                </span>
            </header>

            <section className="hero">
                <p className="eyebrow">NEAR-EARTH OBJECT TRACKER</p>
                <h1>
                    Our corner of
                    <br />
                    <span>the universe.</span>
                </h1>
                <p className="hero-description">
                    Explore the aestroids passing through our neighbourhood of space.
                    Real observations, sourced from NASA.
                </p>
            </section>

            <section className="stats-grid" aria-label="Asteroid statistics">
                <article className="stat-card">
                    <p className="stat-label">CLOSE APPROACHES</p>
                    <p className="stat-value">
                        {loading ? "-" : approaches.length}
                    </p>
                    <p className="stat-caption">Next 7 days</p>
                </article>

                <article className="stat-card">
                    <p className="stat-label">POTENTIALLY HAZARDOUS</p>
                    <p className="stat-value">
                        {loading ? "-" : hazardousCount}
                    </p>
                    <p className="stat-caption">Flagged by NASA</p>
                </article>

                <article className="stat-card">
                    <p className="stat-label">DATA SOURCE</p>
                    <p className="stat-value">NASA</p>
                    <p className="stat-caption">Near-Earth Object Web Service</p>
                </article>
            </section>

            <section className="appraoches-section">
                <div className="section-heading">
                    <div>
                        <p className="eyebrow">LIVE FEED</p>
                        <h2>Upcoming approaches</h2>
                    </div>
                    <span className="range-label">7-DAY WINDOW</span>
                </div>

                {loading && <p className="message">Scanning the skies...</p>}

                {error && <p className="message error">{error}</p>}

                {!loading && !error && approaches.length === 0 && (
                    <p className="message">No approaches in the next 7 days.</p>
                )}

                {!loading && !error && approaches.length > 0 && (
                    <div className="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>ASTEROID</th>
                                    <th>APPROACH DATE</th>
                                    <th>DISTANCE (KM)</th>
                                    <th>RELATIVE VELOCITY (KPH)</th>
                                    <th>STATUS</th>
                                </tr>
                            </thead>
                            <tbody>
                                {sortedApproaches.map((approach, index) =>
                                    <tr key={`${approach.nasa_id}-${approach.approach_date}-${index}`}>
                                        <td className="asteroid-name">{approach.name}</td>
                                        <td>{approach.approach_date}</td>
                                        <td>{formatDistance(approach.miss_distance_km)}</td>
                                        <td>{formatDistance(approach.relative_velocity_kph)}</td>
                                        <td>
                                            <span
                                                className={`status-pill ${approach.is_potentially_hazardous ? "hazardous" : "safe"}`}
                                            >
                                                {approach.is_potentially_hazardous ? "Potentially Hazardous" : "Not Flagged"}
                                            </span>
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
            </section>

            <footer>
                <span>STARFALL © 2026</span>
                <span>DATA PROVIDED BY NASA / JPL</span>
            </footer>
        </main>
    );    
}

export default App;