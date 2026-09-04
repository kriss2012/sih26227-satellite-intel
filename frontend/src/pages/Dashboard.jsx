import { useState } from 'react'
import SearchBar from '../components/SearchBar.jsx'

/**
 * Main analyst view. TODO (Sept 16-18 per PROJECT_PLAN.md):
 *  - filters row (date range, sensor, cloud %)
 *  - MapLibre map showing result locations
 *  - click a result -> before/after viewer + change map + confidence score
 *  - time slider across available dates
 *  - confirm / reject / needs-review buttons (human-in-the-loop)
 */
export default function Dashboard() {
  const [results, setResults] = useState([])

  return (
    <main className="p-4">
      <SearchBar onResults={setResults} />

      {results.length === 0 ? (
        <p className="px-4 text-sm text-slate-400">
          Search the archive to see results here.
        </p>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4">
          {results.map((r) => (
            <div
              key={r.tile_id}
              className="rounded-lg border border-slate-800 bg-slate-900 p-3 text-sm"
            >
              <div className="aspect-video rounded bg-slate-800 mb-2 flex items-center justify-center text-slate-500">
                tile preview
              </div>
              <p className="font-medium">{r.date} — {r.sensor}</p>
              <p className="text-slate-400">
                {r.latitude.toFixed(3)}, {r.longitude.toFixed(3)}
              </p>
              <p className="text-emerald-400">{Math.round(r.score * 100)}% match</p>
            </div>
          ))}
        </div>
      )}
    </main>
  )
}
