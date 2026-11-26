import { useNavigate } from 'react-router-dom'
import {
  BarChart3,
  BrainCircuit,
  CheckCircle2,
  Code2,
  FileText,
  Lightbulb,
  Search,
  ShieldCheck,
  Sparkles,
  Target,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { CATEGORIES } from '@/services/api'

const categoryCards = [
  { title: CATEGORIES[0], icon: ShieldCheck, description: 'Deterministic rules and traditional software.', color: 'text-navy-500' },
  { title: CATEGORIES[1], icon: BarChart3, description: 'Dashboards, reporting and trend analysis.', color: 'text-violet-500' },
  { title: CATEGORIES[2], icon: Target, description: 'Prediction and classification on structured data.', color: 'text-primary' },
  { title: CATEGORIES[3], icon: BrainCircuit, description: 'Image, audio and other perception tasks.', color: 'text-amber-500' },
  { title: CATEGORIES[4], icon: Sparkles, description: 'Generation, summarisation and semantic QA.', color: 'text-rose-500' },
]

const benefits = [
  { icon: CheckCircle2, title: 'Accurate recommendations', text: 'Evidence-based suggestions from a transparent rule engine.' },
  { icon: Lightbulb, title: 'Explainable decisions', text: 'See the exact rules, reasons, risks and data requirements.' },
  { icon: FileText, title: 'Project roadmap', text: 'A five-stage lifecycle and responsible engineering roles.' },
]

export default function LandingPage() {
  const navigate = useNavigate()

  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <header className="animate-fade-in-up">
        <span className="inline-flex items-center gap-2 rounded-full border border-border bg-card px-3 py-1 text-xs text-muted-foreground">
          <ShieldCheck className="h-3.5 w-3.5 text-primary" /> Demo mode — no registration required
        </span>
        <h1 className="mt-6 max-w-4xl text-4xl font-bold tracking-tight sm:text-6xl">
          Know when AI is the right answer.
        </h1>
        <p className="mt-5 max-w-2xl text-lg text-muted-foreground">
          Describe a business requirement and get a transparent recommendation across five technology
          approaches — from simple rules to generative AI — with reasons, risks and next steps.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Button size="lg" onClick={() => navigate('/analyze')}>
            <Search className="h-4 w-4" /> Start analysing
          </Button>
          <Button size="lg" variant="outline" onClick={() => navigate('/dashboard')}>
            <BarChart3 className="h-4 w-4" /> View dashboard
          </Button>
        </div>
      </header>

      <section className="mt-16" aria-labelledby="how-it-works">
        <h2 id="how-it-works" className="text-2xl font-bold sm:text-3xl">How it works</h2>
        <div className="mt-6 grid gap-4 md:grid-cols-3">
          {[
            ['1', 'Describe', 'Enter a business problem or pick one of 15 ready-made examples.'],
            ['2', 'Evaluate', 'The rule engine applies an explicit priority policy to the requirement.'],
            ['3', 'Recommend', 'Receive a category, explanation, risks, data needs and a roadmap.'],
          ].map(([number, title, text]) => (
            <Card key={number} className="animate-fade-in-up">
              <CardHeader>
                <span className="text-3xl font-bold text-primary">{number}</span>
                <CardTitle>{title}</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground">{text}</CardContent>
            </Card>
          ))}
        </div>
      </section>

      <section className="mt-16" aria-labelledby="categories">
        <h2 id="categories" className="text-2xl font-bold sm:text-3xl">Five technology categories</h2>
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          {categoryCards.map(({ title, icon: Icon, description, color }) => (
            <Card key={title} className="animate-fade-in-up">
              <CardContent className="pt-5">
                <Icon className={`mb-3 h-9 w-9 ${color}`} />
                <h3 className="font-semibold">{title}</h3>
                <p className="mt-1 text-sm text-muted-foreground">{description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      <section className="mt-16" aria-labelledby="benefits">
        <h2 id="benefits" className="text-2xl font-bold sm:text-3xl">Why use it</h2>
        <div className="mt-6 grid gap-4 md:grid-cols-3">
          {benefits.map(({ icon: Icon, title, text }) => (
            <div key={title} className="flex gap-3 rounded-lg border border-border bg-card p-4">
              <Icon className="h-5 w-5 shrink-0 text-primary" />
              <div>
                <h3 className="font-medium">{title}</h3>
                <p className="mt-1 text-sm text-muted-foreground">{text}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="mt-16 rounded-xl border border-border bg-card p-8 animate-fade-in-up">
        <div className="flex flex-col items-start justify-between gap-6 sm:flex-row sm:items-center">
          <div>
            <h2 className="text-2xl font-bold">Example: Predict customer cancellation</h2>
            <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
              Structured historical data plus a prediction target → Classical ML, with a labelled dataset,
              a validation split and a five-stage delivery lifecycle.
            </p>
          </div>
          <Button onClick={() => navigate('/analyze')}>Try your own requirement</Button>
        </div>
      </section>
    </div>
  )
}
