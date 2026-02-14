import "./globals.css";

export const metadata = {
  title: "Gold Backtest System",
  description: "Web dashboard for XAUUSD backtesting engine",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
