import { useEffect, useState } from 'react'
import { Download, FileSpreadsheet, FileText } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Select } from '@/components/ui/select'
import { useToast } from '@/hooks/use-toast'
import { api, type AnalysisListItem } from '@/services/api'

const reportContents = [
  'Requirement description and attributes',
  'Final decision category',
  'Decision rule identifiers and explanations',
  'Reasons, risks and limitations',
  'Data requirements',
  'Alternative approach and first next step',
  'Five-stage lifecycle roadmap and responsible roles',
]

export default function Reports() {
  const { toast } = useToast()
  const [analyses, setAnalyses] = useState<AnalysisListItem[]>([])
  const [selected, setSelected] = useState('')
  const [busy, setBusy] = useState<string | null>(null)

  useEffect(() => {
    api.getAnalyses().then(setAnalyses).catch(() => undefined)
  }, [])

  const run = async (kind: string, action: () => Promise<void>) => {
    setBusy(kind)
    try {
      await action()
      toast({ title: 'Download started', description: 'Your report is being saved.' })
    } catch (err) {
      toast({
        title: 'Export failed',
        description: err instanceof Error ? err.message : 'Unknown error',
        variant: 'destructive',
      })
    } finally {
      setBusy(null)
    }
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
      <header>
        <h1 className="text-3xl font-bold">Reports</h1>
        <p className="mt-1 text-sm text-muted-foreground">Export analysis data and decision reports.</p>
      </header>

      <Card className="mt-8">
        <CardHeader><CardTitle>Generate a report</CardTitle></CardHeader>
        <CardContent className="space-y-5">
          <div className="flex flex-wrap gap-3">
            <Button onClick={() => void run('csv', () => api.downloadCSV())} disabled={busy !== null}>
              <FileSpreadsheet className="h-4 w-4" />
              {busy === 'csv' ? 'Preparing…' : 'Export all as CSV'}
            </Button>
            <Button variant="outline" onClick={() => void run('all', () => api.downloadReport())} disabled={busy !== null}>
              <FileText className="h-4 w-4" />
              {busy === 'all' ? 'Preparing…' : 'Download complete PDF report'}
            </Button>
          </div>

          <div className="rounded-lg border border-border p-4">
            <h3 className="mb-3 text-sm font-semibold">Download one analysis as PDF</h3>
            <div className="flex flex-wrap items-end gap-3">
              <div className="min-w-64 flex-1">
                <Select
                  aria-label="Choose analysis"
                  placeholder="Choose an analysis"
                  value={selected}
                  onChange={(event) => setSelected(event.target.value)}
                  options={analyses.map((item) => ({ value: item.id, label: item.title }))}
                />
              </div>
              <Button
                variant="outline"
                disabled={!selected || busy !== null}
                onClick={() => void run(selected, () => api.downloadPdf(selected))}
              >
                <Download className="h-4 w-4" /> Download PDF
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader><CardTitle>What every report contains</CardTitle></CardHeader>
        <CardContent>
          <ul className="space-y-2">
            {reportContents.map((item) => (
              <li key={item} className="flex gap-2 text-sm text-muted-foreground">
                <span className="text-primary">✓</span> {item}
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}
