const rawApiBaseUrl = process.env.NEXT_PUBLIC_API_URL || "";
const API_BASE_URL = rawApiBaseUrl.trim().replace(/\/+$/, "");

if (!API_BASE_URL) {
  console.warn(
    "NEXT_PUBLIC_API_URL is missing. Set it in frontend/.env.local (example: http://localhost:8000)."
  );
}

function extractErrorMessage(payload, fallback) {
  if (!payload) return fallback || "Request failed. Please try again.";
  if (typeof payload === "string" && payload.trim().length) return payload;

  if (typeof payload === "object") {
    if (typeof payload.detail === "string" && payload.detail.trim().length) return payload.detail;
    if (typeof payload.message === "string" && payload.message.trim().length) return payload.message;
  }

  return fallback || "Request failed. Please try again.";
}

async function request(path, options = {}) {
  if (!API_BASE_URL) {
    throw new Error("API base URL is not configured. Set NEXT_PUBLIC_API_URL in frontend/.env.local.");
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  const raw = await response.text();
  let data = null;
  if (raw) {
    try {
      data = JSON.parse(raw);
    } catch {
      data = raw;
    }
  }

  if (!response.ok) {
    throw new Error(extractErrorMessage(data, `${response.status} ${response.statusText}`));
  }

  return data;
}

export function getBacktestParameters() {
  return request("/api/backtest/parameters");
}

export function runBacktest(payload) {
  return request("/api/backtest/run", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getBacktest(id) {
  return request(`/api/backtest/${id}`);
}

export function getBacktestEquityCurve(id) {
  return request(`/api/backtest/${id}/equity-curve`);
}

export async function pollBacktest(id, { intervalMs = 2000, timeoutMs = 60 * 60 * 1000 } = {}) {
  const started = Date.now();

  while (true) {
    const job = await getBacktest(id);
    if (job.status === "completed" || job.status === "failed") {
      return job;
    }

    if (Date.now() - started > timeoutMs) {
      throw new Error("Backtest polling timed out.");
    }

    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }
}
