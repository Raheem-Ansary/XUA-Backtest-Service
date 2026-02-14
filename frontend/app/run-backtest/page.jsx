"use client";

import { useEffect, useMemo, useState } from "react";

import AppShell from "../../components/dashboard/dashboard/common/AppShell";
import EquityChart from "../../components/dashboard/dashboard/pages/EquityChart";
import MetricCards from "../../components/dashboard/dashboard/pages/MetricCards";
import TradesTable from "../../components/dashboard/dashboard/pages/TradesTable";
import { getBacktestParameters, pollBacktest, runBacktest } from "../../lib/api";

function parseInput(raw, defaultValue) {
  if (typeof defaultValue === "boolean") return Boolean(raw);
  if (typeof defaultValue === "number") {
    const num = Number(raw);
    return Number.isNaN(num) ? defaultValue : num;
  }
  return raw;
}

export default function RunBacktestPage() {
  const [base, setBase] = useState({
    symbol: "XAUUSD",
    timeframe: "5m",
    start_date: "",
    end_date: "",
    initial_cash: 100000,
  });
  const [strategyParams, setStrategyParams] = useState({});
  const [defaults, setDefaults] = useState({});

  const [jobId, setJobId] = useState("");
  const [status, setStatus] = useState("idle");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [bootLoading, setBootLoading] = useState(true);
  const [error, setError] = useState("");

  const parameterEntries = useMemo(() => Object.entries(defaults), [defaults]);

  useEffect(() => {
    async function loadDefaults() {
      setBootLoading(true);
      setError("");
      try {
        const response = await getBacktestParameters();
        const params = response?.strategy_params || {};
        setDefaults(params);
        setStrategyParams(params);
      } catch (err) {
        setError(err.message || "Failed to load strategy parameters.");
      } finally {
        setBootLoading(false);
      }
    }
    loadDefaults();
  }, []);

  async function onRun(event) {
    event.preventDefault();
    setError("");
    setLoading(true);
    setResult(null);
    setStatus("queued");

    try {
      const runResponse = await runBacktest({
        ...base,
        start_date: base.start_date || null,
        end_date: base.end_date || null,
        strategy_params: strategyParams,
      });

      const id = runResponse.id;
      setJobId(id);
      localStorage.setItem("latestBacktestJobId", id);

      const completed = await pollBacktest(id, { intervalMs: 2000 });
      setStatus(completed.status);

      if (completed.status === "failed") {
        throw new Error(completed.error || "Backtest failed.");
      }

      setResult(completed.result);
      localStorage.setItem("latestBacktestResult", JSON.stringify(completed.result));
    } catch (err) {
      setStatus("failed");
      setError(err.message || "Backtest failed. Please check your inputs.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell title="Run Backtest" subtitle="Configure and execute the original XAUUSD Backtrader strategy">
      <section className="panel">
        {bootLoading ? (
          <div className="loading-inline">
            <span className="spinner" />
            <span>Loading strategy parameters...</span>
          </div>
        ) : null}

        <form className="form-grid" onSubmit={onRun}>
          <label>
            <span>Symbol</span>
            <input
              type="text"
              value={base.symbol}
              onChange={(e) => setBase((prev) => ({ ...prev, symbol: e.target.value }))}
              disabled={loading}
            />
          </label>

          <label>
            <span>Timeframe</span>
            <input
              type="text"
              value={base.timeframe}
              onChange={(e) => setBase((prev) => ({ ...prev, timeframe: e.target.value }))}
              disabled={loading}
            />
          </label>

          <label>
            <span>Start Date</span>
            <input
              type="date"
              value={base.start_date}
              onChange={(e) => setBase((prev) => ({ ...prev, start_date: e.target.value }))}
              disabled={loading}
            />
          </label>

          <label>
            <span>End Date</span>
            <input
              type="date"
              value={base.end_date}
              onChange={(e) => setBase((prev) => ({ ...prev, end_date: e.target.value }))}
              disabled={loading}
            />
          </label>

          <label>
            <span>Initial Cash</span>
            <input
              type="number"
              step="any"
              value={base.initial_cash}
              onChange={(e) => setBase((prev) => ({ ...prev, initial_cash: Number(e.target.value) }))}
              disabled={loading}
            />
          </label>

          {parameterEntries.length ? (
            <div className="param-block">
              <h3>Strategy Parameters</h3>
              <div className="param-grid">
                {parameterEntries.map(([key, defaultValue]) => (
                  <label key={key}>
                    <span>{key}</span>
                    {typeof defaultValue === "boolean" ? (
                      <input
                        type="checkbox"
                        checked={Boolean(strategyParams[key])}
                        onChange={(e) =>
                          setStrategyParams((prev) => ({
                            ...prev,
                            [key]: e.target.checked,
                          }))
                        }
                        disabled={loading}
                      />
                    ) : (
                      <input
                        type={typeof defaultValue === "number" ? "number" : "text"}
                        step={typeof defaultValue === "number" ? "any" : undefined}
                        value={strategyParams[key] ?? ""}
                        onChange={(e) =>
                          setStrategyParams((prev) => ({
                            ...prev,
                            [key]: parseInput(e.target.value, defaultValue),
                          }))
                        }
                        disabled={loading}
                      />
                    )}
                  </label>
                ))}
              </div>
            </div>
          ) : null}

          <div className="form-actions">
            <button type="submit" className="btn-primary" disabled={loading || bootLoading}>
              {loading ? "Running Backtest..." : "Run Backtest"}
            </button>
          </div>
        </form>

        {jobId ? <p className="notice">Job ID: {jobId}</p> : null}
        {status !== "idle" ? <p className="notice">Status: {status}</p> : null}
        {error ? <p className="error">{error}</p> : null}
      </section>

      {result ? (
        <>
          <MetricCards result={result} />

          <section className="panel panel--chart">
            <h2>Equity Curve</h2>
            <div className="chart-container">
              <EquityChart equityCurve={result.equity_curve || []} />
            </div>
          </section>

          <section className="panel">
            <h2>Trades</h2>
            <TradesTable trades={result.trade_list || []} />
          </section>
        </>
      ) : null}
    </AppShell>
  );
}
