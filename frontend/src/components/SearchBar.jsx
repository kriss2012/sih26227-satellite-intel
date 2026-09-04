import { useState } from 'react'
import axios from 'axios'

/**
 * Natural-language + image search entry point.
 * TODO: wire the "Find Similar" image-search flow once a result tile is selected.
 */
export default function SearchBar({ onResults }) {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)

  const runSearch = async () => {
    if (!query.trim()) return
    setLoading(true)
    try {
      const { data } = await axios.post('/api/search/text', {
        query,
        top_k: 12,
      })
      onResults(data)
    } catch (err) {
      console.error('Search failed', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex gap-2 p-4">
      <input
        className="flex-1 rounded-md bg-slate-900 border border-slate-700 px-3 py-2 text-sm"
        placeholder='e.g. "new structures near a river"'
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && runSearch()}
      />
      <button
        onClick={runSearch}
        disabled={loading}
        className="rounded-md bg-emerald-600 px-4 py-2 text-sm font-medium hover:bg-emerald-500 disabled:opacity-50"
      >
        {loading ? 'Searching…' : 'Search'}
      </button>
    </div>
  )
}
