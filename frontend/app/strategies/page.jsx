"use client";

import { useEffect, useMemo, useState } from "react";

import AppShell from "../../components/dashboard/dashboard/common/AppShell";
import { getBacktestParameters } from "../../lib/api";

export default function StrategiesPage() {
  const [params, setParams] = useState({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const entries = useMemo(() => Object.entries(params), [params]);

  useEffect(() => {
    async function loadParameters() {
      setLoading(true);
      try {
        const data = await getBacktestParameters();
        setParams(data.strategy_params || {});
      } catch (err) {
        setError(err.message || "Unable to load strategy parameters");
      } finally {
        setLoading(false);
      }
    }
    loadParameters();
  }, []);

  return (
    <AppShell title="Strategy Parameters" subtitle="Runtime-configurable parameters from the original Backtrader strategy">
      {error ? <p className="error">{error}</p> : null}
      <section className="panel">
        {loading ? (
          <div className="loading-inline">
            <span className="spinner" />
            <span>Loading parameters...</span>
          </div>
        ) : entries.length ? (
          <div className="strategy-grid">
            {entries.map(([name, value]) => (
              <article key={name} className="strategy-card">
                <h3>{name}</h3>
                <p className="strategy-class">Type: {typeof value}</p>
                <p>Default: {String(value)}</p>
              </article>
            ))}
          </div>
        ) : (
          <p>No parameters found.</p>
        )}
      </section>
    </AppShell>
  );
}
