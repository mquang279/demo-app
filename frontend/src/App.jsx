import { useEffect, useRef, useState } from 'react'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'
const endpoints = { health: '/api/health', version: '/api/version', message: '/api/message' }

function Details({ data }) {
  if (!data) return <p className="content-text">Loading…</p>
  return <dl className="details">{Object.entries(data).map(([key, value]) => (
    <div key={key}><dt>{key}</dt><dd>{String(value)}</dd></div>
  ))}</dl>
}

function App() {
  const [data, setData] = useState({})
  const [errors, setErrors] = useState({})
  const loaded = useRef(false)

  useEffect(() => {
    if (loaded.current) return
    loaded.current = true
    Object.entries(endpoints).forEach(async ([key, path]) => {
      try {
        const response = await fetch(`${API_BASE_URL}${path}`)
        const payload = await response.json()
        if (!response.ok) throw new Error(payload.error || `HTTP ${response.status}`)
        setData((current) => ({ ...current, [key]: payload }))
      } catch (error) {
        setErrors((current) => ({ ...current, [key]: error.message }))
      }
    })
  }, [])

  const content = (key, children) => errors[key]
    ? <p className="error-message">{errors[key]}</p>
    : children

  return (
    <main className="page-shell">
      <header className="hero">
        <div>
          <span className="eyebrow">LIVE DEMO DASHBOARD</span>
          <h1>DevOps Demo App</h1>
          <p>CI/CD Pipeline &amp; Cloud Observability</p>
        </div>
        <div className="api-badge"><span /> API: {API_BASE_URL}</div>
      </header>

      <section className="dashboard">
        <article className="card status-card">
          <div className="card-heading"><span className="icon">●</span><h2>Backend Status</h2></div>
          {content('health', data.health ? <>
            <div className={`status ${data.health.status === 'ok' ? 'ok' : ''}`}>
              <span className="status-dot" />{data.health.status}
            </div>
            <Details data={{ service: data.health.service, version: data.health.version }} />
          </> : <p className="content-text">Loading…</p>)}
        </article>

        <article className="card version-card">
          <div className="card-heading"><span className="icon">◆</span><h2>Version</h2></div>
          {content('version', <Details data={data.version} />)}
        </article>

        <article className="card message-card">
          <div className="card-heading"><span className="icon">▰</span><h2>Message</h2></div>
          {content('message', <Details data={data.message} />)}
        </article>

      </section>

      <footer><span className="pulse" /> Observability ready · Logs · Metrics · Traces-ready</footer>
    </main>
  )
}

export default App
