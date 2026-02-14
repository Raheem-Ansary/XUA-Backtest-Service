"use client";

import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function formatLabel(value) {
  if (!value) return "-";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return String(value);
  return parsed.toLocaleString();
}

export default function EquityChart({ equityCurve }) {
  if (!equityCurve?.length) {
    return <p className="panel__empty">No equity curve data available.</p>;
  }

  return (
    <Line
      data={{
        labels: equityCurve.map((point) => formatLabel(point.timestamp)),
        datasets: [
          {
            label: "Equity Curve",
            data: equityCurve.map((point) => point.value),
            borderColor: "#e2b100",
            backgroundColor: "#e2b100",
            pointRadius: 0,
            borderWidth: 2,
          },
        ],
      }}
      options={{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
        },
      }}
    />
  );
}
