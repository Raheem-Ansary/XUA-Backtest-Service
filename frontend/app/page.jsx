"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import AppShell from "../components/dashboard/dashboard/common/AppShell";
import EquityChart from "../components/dashboard/dashboard/pages/EquityChart";
import MetricCards from "../components/dashboard/dashboard/pages/MetricCards";
import TradesTable from "../components/dashboard/dashboard/pages/TradesTable";
import { getBacktest } from "../lib/api";

export default function DashboardPage() {
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadLatest() {
      try {
        const jobId = localStorage.getItem("latestBacktestJobId");
        if (jobId) {
          const job = await getBacktest(jobId);
          setStatus(job.status);
          if (job.status === "completed" && job.result) {
            setResult(job.result);
            localStorage.setItem("latestBacktestResult", JSON.stringify(job.result));
            return;
          }
          if (job.status === "failed") {
            setError(job.error || "Latest backtest failed.");
          }
        }

        const raw = localStorage.getItem("latestBacktestResult");
        if (raw) {
          setResult(JSON.parse(raw));
        }
      } catch (err) {
        setError(err.message || "Unable to load latest backtest.");
      }
    }
    loadLatest();
  }, []);

  return (
    <AppShell title="Dashboard" subtitle="Latest XAUUSD backtest performance summary">
      {error ? (
        <p className="error">
          {error} <Link href="/run-backtest">Run another backtest</Link>
        </p>
      ) : null}

      {!result ? (
        <section className="panel">
          <p className="notice">
            No completed backtest found. <Link href="/run-backtest">Run Backtest</Link>
          </p>
          {status !== "idle" ? <p className="notice">Latest job status: {status}</p> : null}
        </section>
      ) : (
        <>
          <MetricCards result={result} />

          <section className="panel panel--chart">
            <h2>Equity Curve</h2>
            <div className="chart-container">
              <EquityChart equityCurve={result.equity_curve || []} />
            </div>
          </section>

          <section className="panel">
            <h2>Trade List</h2>
            <TradesTable trades={result.trade_list || []} />
          </section>
        </>
      )}
    </AppShell>
  );
}
