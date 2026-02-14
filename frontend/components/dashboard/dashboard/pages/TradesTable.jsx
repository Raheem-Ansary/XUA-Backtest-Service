function formatDate(value) {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString();
}

function formatNumber(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "-";
  return Number(value).toFixed(2);
}

export default function TradesTable({ trades }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Direction</th>
            <th>Entry Time</th>
            <th>Exit Time</th>
            <th>Entry</th>
            <th>Exit</th>
            <th>PnL</th>
            <th>Exit Reason</th>
          </tr>
        </thead>
        <tbody>
          {trades?.length ? (
            trades.map((trade, index) => (
              <tr key={`${trade.entry_time || "entry"}-${trade.exit_time || "open"}-${index}`}>
                <td>{trade.direction || "-"}</td>
                <td>{formatDate(trade.entry_time)}</td>
                <td>{formatDate(trade.exit_time)}</td>
                <td>{formatNumber(trade.entry_price)}</td>
                <td>{formatNumber(trade.exit_price)}</td>
                <td>{formatNumber(trade.pnl)}</td>
                <td>{trade.exit_reason || "-"}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={7}>No trades available.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
