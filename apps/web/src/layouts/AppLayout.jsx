function AppLayout({ children }) {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <p className="app-eyebrow">Factory Vision AI Platform</p>
          <h1>Industrial Inspection Dashboard</h1>
        </div>
      </header>

      <main className="app-main">{children}</main>
    </div>
  );
}

export default AppLayout;