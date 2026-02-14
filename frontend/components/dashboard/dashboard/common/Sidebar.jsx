"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { name: "Dashboard", href: "/" },
  { name: "Run Backtest", href: "/run-backtest" },
  { name: "Strategies", href: "/strategies" },
  { name: "Reports", href: "/reports" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <p>Gold Backtest</p>
        <span>XAUUSD Control Panel</span>
      </div>

      <nav className="sidebar__nav">
        {navItems.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`sidebar__link ${active ? "sidebar__link--active" : ""}`}
            >
              {item.name}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
