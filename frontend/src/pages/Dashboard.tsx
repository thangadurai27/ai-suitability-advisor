import { useCallback, useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  BarChart3,
  BrainCircuit,
  Code2,
  Plus,
  ShieldCheck,
  Sparkles,
  Target,
  Trash2,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useToast } from '@/hooks/use-toast'
import {
  api,
  CATEGORIES,
  type AnalysisListItem,
  type AnalyticsSummary,
} from '@/services/api'

const emptySummary: AnalyticsSummary = {
  total_analyses: 0,
  no_ai: 0,
  analytics_bi: 0,
  classical_ml: 0,
  deep_learning: 0,
  generative_ai: 0,
}

const keyForCategory: Record<string, keyof AnalyticsSummary> = {
  'No AI': 'no_ai',
  'Analytics / BI': 'analytics_bi',
  'Classical ML': 'classical_ml',
  'Deep Learning': 'deep_learning',
  'Generative AI': 'generative_ai',
}

const categoryIcons: Record<string, typeof ShieldCheck> = {
  'No AI': ShieldCheck,
  'Analytics / BI': BarChart3,
  'Classical ML': Target,
  'Deep Learning': BrainCircuit,
  'Generative AI': Sparkles,
}

export default function Dashboard() {
  const navigate = useNavigate()
  const { toast } = useToast()
  const [summary, setSummary] = useState<AnalyticsSummary>(emptySummary)
  const [analyses, setAnalyses] = useState<AnalysisListItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const [summaryData, analysesData] = await Promise.all([api.getSummary(), api.getAnalyses()])
      setSummary(summaryData)
      setAnalyses(analysesData)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load dashboard data'
      setError(message)
      toast({ title: 'Could not load dashboard', description: message, variant: 'destructive' })
    } finally {
      setLoading(false)
    }
  }, [toast])

  useEffect(() => {
    void load()
  }, [load])

  const remove = async (id: string) => {
    if (!window.confirm('Delete this analysis permanently?')) return
    try {
      await api.deleteAnalysis(id)
      toast({ title: 'Analysis deleted' })
      await load()
    } catch (err) {
      toast({
        title: 'Delete failed',
        description: err instanceof Error ? err.message : 'Unknown error',
        variant: 'destructive',
      })
    }
  }

  const maxCount = Math.max(1, ...CATEGORIES.map((c) => Number(summary[keyForCategory[c]]) || 0))

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="mt-1 text-sm text-muted-foreground">Overview of all saved analyses.</p>
        </div>
        <Button onClick={() => navigate('/analyze')}>
          <Plus className="h-4 w-4" /> New analysis
        </Button>
      </header>

      {error && (
        <div className="mt-6 rounded-lg border border-destructive/40 bg-destructive/10 p-4 text-sm text-destructive">
          {error} <button className="ml-2 underline" onClick={() => void load()}>Retry</button>
        </div>
      )}

      {loading ? (
        <p className="mt-10 text-center text-muted-foreground">Loading dashboard…</p>
      ) : (
        <>
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <Card className="cursor-pointer" onClick={() => navigate('/history')}>
              <CardContent className="flex items-center justify-between pt-5">
                <div>
                  <p className="text-sm text-muted-foreground">Total analyses</p>
                  <p className="text-3xl font-bold">{summary.total_analyses}</p>
                </div>
                <BarChart3 className="h-8 w-8 text-primary" />
              </CardContent>
            </Card>
            {CATEGORIES.map((category) => {
              const Icon = categoryIcons[category]
              return (
                <Card key={category}>
                  <CardContent className="flex items-center justify-between pt-5">
                    <div>
                      <p className="text-sm text-muted-foreground">{category}</p>
                      <p className="text-3xl font-bold">{summary[keyForCategory[category]] ?? 0}</p>
                    </div>
                    <Icon className="h-8 w-8 text-primary" />
                  </CardContent>
                </Card>
              )
            })}
          </div>

          <Card className="mt-8">
            <CardHeader>
              <CardTitle>Category distribution</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {CATEGORIES.map((category) => {
                const count = Number(summary[keyForCategory[category]]) || 0
                return (
                  <div key={category} className="flex items-center gap-3">
                    <span className="w-32 shrink-0 text-sm text-muted-foreground">{category}</span>
                    <div className="h-3 flex-1 overflow-hidden rounded-full bg-muted">
                      <div
                        className="h-full rounded-full bg-primary transition-all"
                        style={{ width: `${(count / maxCount) * 100}%` }}
                      />
                    </div>
                    <span className="w-8 text-right text-sm font-medium">{count}</span>
                  </div>
                )
              })}
            </CardContent>
          </Card>

          <Card className="mt-8">
            <CardHeader>
              <CardTitle>Recent analyses</CardTitle>
            </CardHeader>
            <CardContent>
              {analyses.length === 0 ? (
                <p className="text-sm text-muted-foreground">
                  No analyses yet. <Link to="/analyze" className="underline">Run your first analysis</Link>.
                </p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-border text-left text-muted-foreground">
                        <th className="pb-2">Title</th>
                        <th className="pb-2">Category</th>
                        <th className="pb-2">Date</th>
                        <th className="pb-2 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analyses.slice(0, 10).map((item) => (
                        <tr key={item.id} className="border-b border-border/60 last:border-0">
                          <td className="py-3 pr-4">
                            <Link className="font-medium hover:text-primary hover:underline" to={`/results/${item.id}`}>
                              {item.title || 'Untitled'}
                            </Link>
                          </td>
                          <td className="py-3 pr-4">
                            <span className="rounded-full bg-primary/10 px-2 py-0.5 text-xs text-primary">
                              {item.decision_category}
                            </span>
                          </td>
                          <td className="py-3 pr-4 text-muted-foreground">
                            {item.created_at ? new Date(item.created_at).toLocaleDateString() : '—'}
                          </td>
                          <td className="py-3 text-right">
                            <Button variant="ghost" size="sm" onClick={() => void remove(item.id)} aria-label="Delete analysis">
                              <Trash2 className="h-4 w-4 text-destructive" />
                            </Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </CardContent>
          </Card>
        </>
      )}
    </div>
  )
}
