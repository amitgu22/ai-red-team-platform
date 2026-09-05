import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [page, setPage] = useState("Dashboard");
  const [providers, setProviders] = useState([]);
  const [targets, setTargets] = useState([]);

  async function load() {
    const [p, t] = await Promise.all([
      fetch(`${API}/api/providers`).then(r => r.json()),
      fetch(`${API}/api/targets`).then(r => r.json())
    ]);
    setProviders(p);
    setTargets(t);
  }

  useEffect(() => { load(); }, []);

  async function seedProviders() {
    await fetch(`${API}/api/providers/seed`, {method: "POST"});
    load();
  }

  async function seedTarget() {
    await fetch(`${API}/api/targets/seed`, {method: "POST"});
    load();
  }

  const nav = ["Dashboard", "Providers", "Targets", "Scenarios", "Strategies", "Test Configurations", "Campaigns", "Findings", "Reports"];

  return (
    <div className="app">
      <aside>
        <div className="brand">AI <span>RED TEAM</span></div>
        <div className="subtitle">Security Testing Platform</div>
        {nav.map(item => (
          <button className={page === item ? "nav active" : "nav"} onClick={() => setPage(item)} key={item}>
            {item}
          </button>
        ))}
        <div className="phase">PHASE 1 POC</div>
      </aside>

      <main>
        <header>
          <div>
            <div className="eyebrow">AI SECURITY CENTER</div>
            <h1>{page}</h1>
          </div>
          <button className="primary">+ New Campaign</button>
        </header>

        {page === "Dashboard" && (
          <>
            <section className="cards">
              <Card title="Security Score" value="72" suffix="/100" note="Demo baseline" />
              <Card title="Attack Coverage" value="84" suffix="%" note="Target capability coverage" />
              <Card title="Findings" value="47" suffix="" note="3 critical · 11 high" />
              <Card title="Providers" value={providers.length || "0"} suffix="" note="Execution engines" />
            </section>

            <section className="grid">
              <Panel title="Attack Surface">
                {[
                  ["Prompt Injection", 91],
                  ["Jailbreak", 78],
                  ["Data Leakage", 69],
                  ["RAG", 57],
                  ["Agent", 51],
                  ["Tool Abuse", 38]
                ].map(([name, score]) => <div className="barrow" key={name}><span>{name}</span><div className="bar"><i style={{width: score + "%"}} /></div><b>{score}%</b></div>)}
              </Panel>
              <Panel title="Environment">
                <div className="status">● API online</div>
                <div className="status">● PostgreSQL connected</div>
                <div className="status">● Redis available</div>
                <div className="status">● Sample target ready</div>
              </Panel>
            </section>
          </>
        )}

        {page === "Providers" && (
          <section className="panel">
            <div className="panelhead"><h2>Execution Providers</h2><button onClick={seedProviders}>Load POC Providers</button></div>
            {providers.length === 0 ? <Empty text="No providers yet. Load the four Phase 1 provider definitions." /> :
              providers.map(p => <div className="listrow" key={p.id}><div><strong>{p.name}</strong><small>{p.provider_type} · {p.capabilities.join(" · ")}</small></div><span className="pill">READY</span></div>)}
          </section>
        )}

        {page === "Targets" && (
          <section className="panel">
            <div className="panelhead"><h2>Target Applications</h2><button onClick={seedTarget}>Add Sample Target</button></div>
            {targets.length === 0 ? <Empty text="No targets registered." /> :
              targets.map(t => <div className="listrow" key={t.id}><div><strong>{t.name}</strong><small>{t.target_type} · {t.endpoint}</small></div><span className="pill">READY</span></div>)}
          </section>
        )}

        {["Scenarios", "Strategies", "Test Configurations", "Campaigns", "Findings", "Reports"].includes(page) && (
          <section className="panel placeholder">
            <div className="icon">◈</div>
            <h2>{page} module</h2>
            <p>This module is scaffolded for Phase 2. The data model and UI navigation are intentionally prepared for the orchestrator, attack scenarios, evaluation, findings and reporting layers.</p>
          </section>
        )}
      </main>
    </div>
  );
}

function Card({title, value, suffix, note}) {
  return <div className="card"><div className="muted">{title}</div><div className="metric">{value}<small>{suffix}</small></div><div className="note">{note}</div></div>
}

function Panel({title, children}) {
  return <div className="panel"><h2>{title}</h2>{children}</div>
}

function Empty({text}) {
  return <div className="empty">{text}</div>
}

createRoot(document.getElementById("root")).render(<App />);
