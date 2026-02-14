function formatNumber(value, suffix = "") {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "-";
  return `${Number(value).toFixed(2)}${suffix}`;
}

function formatCurrency(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "-";
  return Number(value).toLocaleString(undefined, { style: "currency", currency: "USD" });
}

export default function MetricCards({ result }) {
  const metrics = [
    { title: "Total Return", value: formatNumber(result?.total_return_pct, "%") },
    { title: "Net Profit", value: formatCurrency(result?.net_profit) },
    { title: "Max Drawdown", value: formatNumber(result?.max_drawdown_pct, "%") },
    { title: "Sharpe Ratio", value: formatNumber(result?.sharpe_ratio) },
    { title: "Total Trades", value: result?.total_trades ?? "-" },
    { title: "Win Rate", value: formatNumber(result?.win_rate_pct, "%") },
  ];

  return (
    <section className="metrics-grid">
      {metrics.map((item) => (
        <article key={item.title} className="metric-card">
          <h3>{item.title}</h3>
          <p>{item.value}</p>
        </article>
      ))}
    </section>
  );
}
