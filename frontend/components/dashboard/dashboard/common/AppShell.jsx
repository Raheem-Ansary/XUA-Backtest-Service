import Sidebar from "./Sidebar";

export default function AppShell({ title, subtitle, children }) {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="content">
        <header className="content__header">
          <h1>{title}</h1>
          {subtitle ? <p>{subtitle}</p> : null}
        </header>
        {children}
      </main>
    </div>
  );
}
