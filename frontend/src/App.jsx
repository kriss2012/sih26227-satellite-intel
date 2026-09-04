import Dashboard from './pages/Dashboard.jsx'

function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 px-6 py-4">
        <h1 className="text-lg font-semibold tracking-tight">
          🛰️ Satellite Intelligence Platform
        </h1>
      </header>
      <Dashboard />
    </div>
  )
}

export default App
