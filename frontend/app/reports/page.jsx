"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import AppShell from "../../components/dashboard/dashboard/common/AppShell";
import TradesTable from "../../components/dashboard/dashboard/pages/TradesTable";
import { getBacktest } from "../../lib/api";

export default function ReportsPage() {
  const [result, setResult] = useState(null);
  const [jobId, setJobId] = useState("");
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadReport() {
      try {
        const latestJobId = localStorage.getItem("latestBacktestJobId");
        if (!latestJobId) {
          setError("No report available yet. Run a backtest first.");
          return;
        }

        setJobId(latestJobId);
        const job = await getBacktest(latestJobId);
        setStatus(job.status);

        if (job.status === "completed") {
          setResult(job.result);
        } else if (job.status === "failed") {
          setError(job.error || "Backtest failed.");
        } else {
          setError("Backtest is not finished yet.");
        }
      } catch (err) {
        setError(err.message || "Unable to load report.");
      }
    }
    loadReport();
  }, []);

  return (
    <AppShell title="Reports" subtitle="Latest backtest report and closed trade log">
      {jobId ? <p className="notice">Job ID: {jobId} ({status})</p> : null}
      {error ? (
        <p className="notice">
          {error} <Link href="/run-backtest">Go to Run Backtest</Link>
        </p>
      ) : null}
      {result ? (
        <section className="panel">
          <h2>Latest Run: {result.symbol}</h2>
          <p className="report-meta">
            Return: {Number(result.total_return_pct || 0).toFixed(2)}% | Win Rate: {Number(result.win_rate_pct || 0).toFixed(2)}% | Max DD: {Number(result.max_drawdown_pct || 0).toFixed(2)}% | Trades: {result.total_trades}
          </p>
          <TradesTable trades={result.trade_list || []} />
        </section>
      ) : null}
    </AppShell>
  );
}
