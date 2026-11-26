import { useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { ArrowRight, CheckCircle2, Loader2, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { useToast } from '@/hooks/use-toast'
import {
  api,
  emptyRequirement,
  ruleLabel,
  SAMPLE_REQUIREMENTS,
  type AnalysisResult,
  type RequirementInput,
} from '@/services/api'

type BooleanKey =
  | 'fixed_rules_possible'
  | 'needs_learning_from_data'
  | 'unstructured_input'
  | 'requires_content_generation'
  | 'data_available'

const booleanFields: Array<{ key: BooleanKey; label: string; help: string }> = [
  { key: 'fixed_rules_possible', label: 'Fixed rules can solve it', help: 'Deterministic rules are enough.' },
  { key: 'needs_learning_from_data', label: 'Needs learning from data', help: 'Patterns must be learned from examples.' },
  { key: 'unstructured_input', label: 'Unstructured input', help: 'Images, audio or free-form text.' },
  { key: 'requires_content_generation', label: 'Generates content', help: 'The output is new text, images or summaries.' },
  { key: 'data_available', label: 'Relevant data available', help: 'Labelled or historical data exists today.' },
]

export default function RequirementAnalyzer() {
  const location = useLocation()
  const { toast } = useToast()
  const [form, setForm] = useState<RequirementInput>(emptyRequirement)
  const [sampleId, setSampleId] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<AnalysisResult | null>(null)

  useEffect(() => {
    const state = location.state as { requirement?: RequirementInput } | null
    const requirement = state?.requirement
    if (requirement) {
      setForm({ ...emptyRequirement(), ...requirement })
      setResult(null)
    }
  }, [location.state])

  const applySample = (id: string) => {
    setSampleId(id)
    const sample = SAMPLE_REQUIREMENTS.find((item) => item.id === id)
    if (sample) {
      const { expectedCategory: _expected, hint: _hint, ...payload } = sample
      setForm({ ...payload })
      setResult(null)
      setError(null)
    }
  }

  const setField = <K extends keyof RequirementInput>(key: K, value: RequirementInput[K]) => {
    setForm((current) => ({ ...current, [key]: value }))
  }

  const submit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const analysis = await api.analyze(form)
      setResult(analysis)
      toast({ title: 'Analysis complete', description: `Recommendation: ${analysis.decision_category}` })
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Analysis failed'
      setError(message)
      toast({ title: 'Analysis failed', description: message, variant: 'destructive' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <header>
        <h1 className="text-3xl font-bold">Requirement analyzer</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Answer a few questions about your business problem to get an explainable recommendation.
        </p>
      </header>

      <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_340px]">
        <Card>
          <CardHeader>
            <CardTitle>Your requirement</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={submit} className="space-y-5">
              <Select
                label="Start from an example (optional)"
                placeholder="Choose a sample requirement"
                value={sampleId}
                onChange={(event) => applySample(event.target.value)}
                options={SAMPLE_REQUIREMENTS.map((sample) => ({
                  value: sample.id || sample.title,
                  label: `${sample.title} · ${sample.expectedCategory}`,
                }))}
              />

              <Input
                label="Requirement title"
                name="title"
                required
                maxLength={200}
                placeholder="e.g. Predict which customers will cancel next month"
                value={form.title}
                onChange={(event) => setField('title', event.target.value)}
              />

              <Input
                label="Detailed business problem"
                as="textarea"
                required
                placeholder="Describe what the system should do and what data is involved…"
                value={form.description}
                onChange={(event) => setField('description', event.target.value)}
              />

              <fieldset className="grid gap-3 sm:grid-cols-2">
                <legend className="mb-2 text-sm font-medium">Requirement attributes</legend>
                {booleanFields.map(({ key, label, help }) => (
                  <label
                    key={key}
                    className="flex cursor-pointer items-start gap-3 rounded-lg border border-border p-3 hover:bg-accent/50"
                  >
                    <input
                      type="checkbox"
                      className="mt-0.5 h-4 w-4 accent-current text-primary"
                      checked={Boolean(form[key])}
                      onChange={(event) => setField(key, event.target.checked)}
                    />
                    <span>
                      <span className="block text-sm font-medium">{label}</span>
                      <span className="block text-xs text-muted-foreground">{help}</span>
                    </span>
                  </label>
                ))}
              </fieldset>

              <div className="grid gap-4 sm:grid-cols-2">
                <Input
                  label="Business domain"
                  placeholder="Finance, HR, Manufacturing…"
                  value={form.domain}
                  onChange={(event) => setField('domain', event.target.value)}
                />
                <Input
                  label="Additional context"
                  placeholder="Optional details"
                  value={form.additional_context || ''}
                  onChange={(event) => setField('additional_context', event.target.value)}
                />
              </div>

              {error && <p className="text-sm text-destructive">{error}</p>}

              <Button type="submit" disabled={loading} size="lg">
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
                {loading ? 'Analysing…' : 'Get recommendation'}
              </Button>
            </form>
          </CardContent>
        </Card>

        <div className="space-y-4">
          {!result && (
            <Card>
              <CardHeader>
                <CardTitle>How the decision works</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-muted-foreground">
                <p>The engine applies a fixed priority policy so the same input always gets the same result:</p>
                <ol className="list-decimal space-y-1 pl-5">
                  <li>Fixed rules → No AI</li>
                  <li>No data → No AI with a data-collection plan</li>
                  <li>Content generation → Generative AI</li>
                  <li>Perception tasks → Deep Learning</li>
                  <li>Reporting/trends → Analytics / BI</li>
                  <li>Other learning tasks → Classical ML</li>
                </ol>
              </CardContent>
            </Card>
          )}

          {result && (
            <Card className="border-primary/40 animate-fade-in">
              <CardHeader>
                <CardTitle>Recommendation</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="rounded-lg bg-primary/10 p-4">
                  <p className="text-xs uppercase tracking-wide text-muted-foreground">Recommended category</p>
                  <p className="mt-1 text-2xl font-bold text-primary">{result.decision_category}</p>
                </div>

                <div>
                  <h3 className="mb-1 text-sm font-semibold">Why</h3>
                  <ul className="space-y-1 text-sm text-muted-foreground">
                    {result.reasons.map((reason) => (
                      <li key={reason} className="flex gap-2">
                        <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-primary" /> {reason}
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="mb-1 text-sm font-semibold">Rules applied</h3>
                  <ul className="space-y-1 text-xs text-muted-foreground">
                    {(result.evidence_rule_ids?.length
                      ? result.evidence_rule_ids
                      : result.evidence?.rule_ids || []
                    ).map((rule) => <li key={rule}>{ruleLabel(rule)}</li>)}
                  </ul>
                </div>

                <div>
                  <h3 className="text-sm font-semibold">First next step</h3>
                  <p className="text-sm text-muted-foreground">{result.first_next_step}</p>
                </div>

                <div className="flex flex-col gap-2">
                  <Link to={`/results/${result.id}`}>
                    <Button className="w-full" variant="outline">
                      View full result <ArrowRight className="h-4 w-4" />
                    </Button>
                  </Link>
                  <Link to="/history">
                    <Button className="w-full" variant="ghost">Go to history</Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
