import { useCallback, useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { History, Loader2, Search, Trash2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { useToast } from '@/hooks/use-toast'
import { api, CATEGORIES, type AnalysisListItem } from '@/services/api'

export default function AnalysisHistory() {
  const { toast } = useToast()
  const [analyses, setAnalyses] = useState<AnalysisListItem[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')

  const load = useCallback(async () => {
    setLoading(true)
    try {
      setAnalyses(await api.getAnalyses())
    } catch (err) {
      toast({
        title: 'Could not load history',
        description: err instanceof Error ? err.message : 'Unknown error',
        variant: 'destructive',
      })
    } finally {
      setLoading(false)
    }
  }, [toast])

  useEffect(() => { void load() }, [load])

  const filtered = useMemo(
    () => analyses.filter((item) =>
      item.title.toLowerCase().includes(search.toLowerCase()) &&
      (!category || item.decision_category === category)),
    [analyses, search, category],
  )

  const remove = async (id: string) => {
    if (!window.confirm('Delete this analysis permanently?')) return
    try {
      await api.deleteAnalysis(id)
      toast({ title: 'Analysis deleted' })
      await load()
    } catch (err) {
      toast({ title: 'Delete failed', description: err instanceof Error ? err.message : 'Unknown error', variant: 'destructive' })
    }
  }

  const removeAll = async () => {
    if (!window.confirm(`Delete all ${analyses.length} analyses? This cannot be undone.`)) return
    try {
      await Promise.all(analyses.map((item) => api.deleteAnalysis(item.id)))
      toast({ title: 'All analyses deleted' })
      await load()
    } catch (err) {
      toast({ title: 'Delete failed', description: err instanceof Error ? err.message : 'Unknown error', variant: 'destructive' })
    }
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">Analysis history</h1>
          <p className="mt-1 text-sm text-muted-foreground">Every saved recommendation, searchable and exportable.</p>
        </div>
        {analyses.length > 0 && (
          <Button variant="destructive" size="sm" onClick={() => void removeAll()}>
            <Trash2 className="h-4 w-4" /> Delete all
          </Button>
        )}
      </header>

      <Card className="mt-6">
        <CardContent className="grid gap-4 pt-5 sm:grid-cols-[1fr_220px]">
          <div className="relative">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input className="pl-9" placeholder="Search analyses…" value={search} onChange={(e) => setSearch(e.target.value)} />
          </div>
          <Select
            placeholder="All categories"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            options={CATEGORIES.map((value) => ({ value, label: value }))}
          />
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader><CardTitle>Saved analyses ({filtered.length})</CardTitle></CardHeader>
        <CardContent>
          {loading ? (
            <p className="flex items-center gap-2 text-sm text-muted-foreground"><Loader2 className="h-4 w-4 animate-spin" /> Loading…</p>
          ) : filtered.length === 0 ? (
            <div className="py-8 text-center">
              <History className="mx-auto h-8 w-8 text-muted-foreground" />
              <p className="mt-3 text-sm text-muted-foreground">No analyses found. Try the analyzer or library.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {filtered.map((item) => (
                <div key={item.id} className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-border p-4 hover:bg-accent/40">
                  <div className="min-w-0 flex-1">
                    <Link to={`/results/${item.id}`} className="font-medium hover:text-primary hover:underline">
                      {item.title || 'Untitled'}
                    </Link>
                    <p className="mt-1 text-xs text-muted-foreground">
                      {item.created_at ? new Date(item.created_at).toLocaleString() : '—'}
                    </p>
                  </div>
                  <span className="rounded-full bg-primary/10 px-2 py-0.5 text-xs text-primary">
                    {item.decision_category}
                  </span>
                  <Button size="sm" variant="ghost" onClick={() => void remove(item.id)} aria-label="Delete analysis">
                    <Trash2 className="h-4 w-4 text-destructive" />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
