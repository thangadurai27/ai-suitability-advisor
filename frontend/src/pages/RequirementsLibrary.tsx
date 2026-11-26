import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Play, Search } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { api, SAMPLE_REQUIREMENTS, type RequirementInput, type SampleRequirement } from '@/services/api'

type LibraryItem = RequirementInput & {
  expectedCategory?: string
  hint?: string
}

export default function RequirementsLibrary() {
  const navigate = useNavigate()
  const [items, setItems] = useState<LibraryItem[]>(SAMPLE_REQUIREMENTS as LibraryItem[])
  const [search, setSearch] = useState('')
  const [domain, setDomain] = useState('')
  const [loadError, setLoadError] = useState<string | null>(null)

  useEffect(() => {
    api.getRequirements()
      .then((saved) => {
        const samples = SAMPLE_REQUIREMENTS as LibraryItem[]
        const merged = new Map<string, LibraryItem>()
        saved.forEach((item) => merged.set(item.id || item.title, item))
        samples.forEach((item) => merged.set(item.id || item.title, { ...item, ...merged.get(item.id || item.title) }))
        setItems([...merged.values()])
      })
      .catch(() => setLoadError('Showing built-in examples; saved requirements could not be loaded.'))
  }, [])

  const domains = useMemo(
    () => [...new Set(items.map((item) => item.domain).filter(Boolean))].sort(),
    [items],
  )

  const filtered = items.filter((item) => {
    const matchesSearch =
      item.title.toLowerCase().includes(search.toLowerCase()) ||
      item.description.toLowerCase().includes(search.toLowerCase())
    const matchesDomain = !domain || item.domain === domain
    return matchesSearch && matchesDomain
  })

  const analyse = (item: LibraryItem) => {
    const payload: RequirementInput = { ...item }
    navigate('/analyze', { state: { requirement: payload } })
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <header>
        <h1 className="text-3xl font-bold">Requirements library</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          {SAMPLE_REQUIREMENTS.length} ready-made examples covering all five recommendation categories.
        </p>
      </header>

      {loadError && <p className="mt-4 text-sm text-amber-600">{loadError}</p>}

      <Card className="mt-6">
        <CardContent className="grid gap-4 pt-5 sm:grid-cols-[1fr_220px_auto]">
          <div className="relative">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              aria-label="Search requirements"
              className="pl-9"
              placeholder="Search title or description…"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>
          <Select
            aria-label="Filter by domain"
            placeholder="All domains"
            value={domain}
            onChange={(event) => setDomain(event.target.value)}
            options={domains.map((value) => ({ value, label: value }))}
          />
          <Button variant="outline" onClick={() => { setSearch(''); setDomain('') }}>Clear</Button>
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Requirements ({filtered.length})</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {filtered.length === 0 && (
            <p className="text-sm text-muted-foreground">No requirements match your filters.</p>
          )}
          {filtered.map((item) => {
            const sample = item as SampleRequirement
            return (
              <div key={item.id || item.title} className="rounded-lg border border-border p-4 transition-colors hover:bg-accent/40">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <h3 className="font-semibold">{item.title}</h3>
                      {sample.expectedCategory && (
                        <span className="rounded-full bg-primary/10 px-2 py-0.5 text-xs text-primary">
                          {sample.expectedCategory}
                        </span>
                      )}
                    </div>
                    <p className="mt-1 text-sm text-muted-foreground">{item.description}</p>
                    {sample.hint && <p className="mt-1 text-xs text-muted-foreground">💡 {sample.hint}</p>}
                    <p className="mt-2 text-xs text-muted-foreground">Domain: {item.domain || 'General'}</p>
                  </div>
                  <Button size="sm" variant="outline" onClick={() => analyse(item)}>
                    <Play className="h-3.5 w-3.5" /> Analyse
                  </Button>
                </div>
              </div>
            )
          })}
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader><CardTitle>Add your own requirement</CardTitle></CardHeader>
        <CardContent>
          <p className="mb-4 text-sm text-muted-foreground">
            Use the analyzer to evaluate a custom business problem with the same decision policy.
          </p>
          <Button onClick={() => navigate('/analyze')}>Open analyzer</Button>
        </CardContent>
      </Card>
    </div>
  )
}
