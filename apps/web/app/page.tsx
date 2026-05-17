"use client";

import { useState } from "react";
import styles from "./page.module.css";

type AskResponse = {
  answer: string;
  confidence: string;
  evidence: { ref_id: string; excerpt?: string }[];
};

export default function Home() {
  const [question, setQuestion] = useState(
    "Which unresolved certification risks could delay flight testing?"
  );
  const [programId] = useState("demo-program");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<AskResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleAsk(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);
    try {
      const res = await fetch("/api/v1/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, program_id: programId }),
      });
      if (!res.ok) throw new Error(`API error ${res.status}`);
      setResponse(await res.json());
    } catch {
      setError(
        "Could not reach the API. Start the gateway (port 8000) and Docker infrastructure."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={styles.shell}>
      <header className={styles.header}>
        <div className={styles.brand}>
          <span className={styles.logo} aria-hidden>
            ✈
          </span>
          <div>
            <h1>AeroCert Intelligence</h1>
            <p>Living digital certification model</p>
          </div>
        </div>
        <nav className={styles.nav} aria-label="Main">
          <span className={styles.navActive}>Dashboard</span>
          <span>Traceability</span>
          <span>Impact</span>
          <span>Audit</span>
        </nav>
      </header>

      <main className={styles.main}>
        <section className={styles.metrics}>
          {[
            { label: "Requirements traced", value: "—", sub: "Connect ingestion" },
            { label: "Open certification gaps", value: "—", sub: "Graph + regulatory" },
            { label: "Audit readiness", value: "—", sub: "Phase 2 scoring" },
            { label: "Unresolved risks", value: "—", sub: "Impact agent" },
          ].map((m) => (
            <article key={m.label} className={styles.metricCard}>
              <h3>{m.label}</h3>
              <p className={styles.metricValue}>{m.value}</p>
              <p className={styles.metricSub}>{m.sub}</p>
            </article>
          ))}
        </section>

        <section className={styles.queryPanel}>
          <h2>Certification intelligence query</h2>
          <p className={styles.hint}>
            Every answer must cite traceable evidence — no ungrounded responses.
          </p>
          <form onSubmit={handleAsk} className={styles.form}>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              rows={3}
              aria-label="Certification question"
            />
            <button type="submit" disabled={loading}>
              {loading ? "Analyzing…" : "Ask with evidence"}
            </button>
          </form>
          {error && <p className={styles.error}>{error}</p>}
          {response && (
            <article className={styles.answer}>
              <div className={styles.confidence}>
                Confidence: <strong>{response.confidence}</strong>
              </div>
              <p>{response.answer}</p>
              {response.evidence.length > 0 && (
                <ul>
                  {response.evidence.map((ev) => (
                    <li key={ev.ref_id}>
                      <code>{ev.ref_id}</code>
                      {ev.excerpt && <span> — {ev.excerpt.slice(0, 120)}…</span>}
                    </li>
                  ))}
                </ul>
              )}
            </article>
          )}
        </section>

        <section className={styles.mapPlaceholder}>
          <h2>Dependency map</h2>
          <p>
            Requirements → tests → hazards → DO-178C objectives visualization
            connects here once the knowledge graph is populated.
          </p>
        </section>
      </main>
    </div>
  );
}
