/* Typed API client for the AI Suitability Advisor backend. */

const API_BASE = (import.meta.env.VITE_API_URL as string | undefined) || ''

export interface RequirementInput {
  id?: string
  title: string
  description: string
  fixed_rules_possible: boolean
  needs_learning_from_data: boolean
  unstructured_input: boolean
  requires_content_generation: boolean
  data_available: boolean
  domain: string
  additional_context?: string
}

export interface SampleRequirement extends RequirementInput {
  expectedCategory: string
  hint: string
}

export interface AnalyticsSummary {
  total_analyses: number
  no_ai: number
  analytics_bi: number
  classical_ml: number
  deep_learning: number
  generative_ai: number
}

export interface AnalysisListItem {
  id: string
  requirement_id: string
  title: string
  decision_category: string
  created_at: string | null
}

export interface AnalysisDetail extends AnalysisListItem {
  reasons: string[]
  evidence_rule_ids: string[]
  alternative_approach: string
  risks: string[]
  data_requirements: string[]
  first_next_step: string
  lifecycle: string[]
  responsible_roles: string[]
}

export interface AnalysisResult extends AnalysisDetail {
  evidence: {
    rule_ids: string[]
    text_support: string[]
    data_points: Record<string, unknown>
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options?.headers || {}),
      },
    })
  } catch {
    throw new Error('Cannot reach the backend. Check that the API server is running on port 8000.')
  }

  if (!response.ok) {
    let detail = `Request failed (${response.status})`
    try {
      const body = await response.json()
      if (body?.detail) detail = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail)
    } catch {
      /* keep the generic message */
    }
    throw new Error(detail)
  }

  if (response.status === 204) return undefined as T
  return (await response.json()) as T
}

async function download(path: string, filename: string, options?: RequestInit): Promise<void> {
  const response = await fetch(`${API_BASE}${path}`, options)
  if (!response.ok) throw new Error(`Download failed (${response.status})`)
  const blob = await response.blob()
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  document.body.appendChild(anchor)
  anchor.click()
  anchor.remove()
  URL.revokeObjectURL(url)
}

export const api = {
  healthCheck: () => request<{ status: string; version: string; database: string }>('/api/health'),
  getRequirements: () => request<RequirementInput[]>('/api/requirements'),
  createRequirement: (payload: RequirementInput) =>
    request<RequirementInput>('/api/requirements', { method: 'POST', body: JSON.stringify(payload) }),
  analyze: (payload: RequirementInput) =>
    request<AnalysisResult>('/api/analyze', { method: 'POST', body: JSON.stringify(payload) }),
  getAnalyses: () => request<AnalysisListItem[]>('/api/analyses'),
  getAnalysis: (id: string) => request<AnalysisDetail>(`/api/analyses/${encodeURIComponent(id)}`),
  deleteAnalysis: (id: string) =>
    request<void>(`/api/analyses/${encodeURIComponent(id)}`, { method: 'DELETE' }),
  getSummary: () => request<AnalyticsSummary>('/api/analytics/summary'),
  downloadCSV: () => download('/api/reports/csv', 'ai_suitability_analyses.csv'),
  downloadReport: () =>
    download('/api/reports/all', 'all_analyses_report.pdf', { method: 'POST' }),
  downloadPdf: (id: string) =>
    download(`/api/reports/${encodeURIComponent(id)}/pdf`, `analysis_${id}.pdf`),
}

export const CATEGORIES = [
  'No AI',
  'Analytics / BI',
  'Classical ML',
  'Deep Learning',
  'Generative AI',
] as const

export const DECISION_RULES: Record<string, string> = {
  R1: 'Fixed rules can solve the task adequately → prefer traditional programming over AI.',
  R2: 'When training data is unavailable → explain the limitation and propose data collection.',
  R3: 'Unstructured input does NOT automatically mean Deep Learning.',
  R4: 'Not all forecasting requires ML.',
  R5: 'If fixed rules can solve the task, prefer traditional programming over AI.',
  R6: 'Conflicting attributes → apply a transparent priority policy and explain ambiguity.',
  R7: 'Descriptive reporting and statistical trend analysis → Analytics / BI.',
  R8: 'Structured-data prediction and classification → Classical ML.',
  R9: 'Complex image, audio and other perception tasks → Deep Learning.',
  R10: 'Content generation, summarisation and semantic QA → Generative AI.',
  R11: 'Domain-specific fixed rules → prefer traditional programming.',
  R12: 'Scalability and maintenance considerations → prefer non-AI where appropriate.',
}

export function ruleLabel(ruleId: string): string {
  const key = (ruleId || '').split(':')[0].trim()
  return `${key}: ${DECISION_RULES[key] || ruleId}`
}

export const SAMPLE_REQUIREMENTS: SampleRequirement[] = [
  {
    id: 'pan_validation',
    title: 'Validate PAN number format',
    description: 'Validate Permanent Account Number (PAN) card format for Indian income tax purposes',
    fixed_rules_possible: true, needs_learning_from_data: false, unstructured_input: false,
    requires_content_generation: false, data_available: false, domain: 'Finance',
    additional_context: 'PAN numbers are 10-character alphanumeric identifiers',
    expectedCategory: 'No AI', hint: 'A regex/rule check is deterministic and explainable.',
  },
  {
    id: 'customer_cancellation',
    title: 'Predict which customers will cancel next month',
    description: 'Identify customers at risk of churning based on usage patterns and demographics',
    fixed_rules_possible: false, needs_learning_from_data: true, unstructured_input: false,
    requires_content_generation: false, data_available: true, domain: 'Marketing',
    additional_context: 'Historical customer data with 2 years of usage history',
    expectedCategory: 'Classical ML', hint: 'Labelled historical data supports supervised classification.',
  },
  {
    id: 'support_email_summarisation',
    title: 'Summarise long support emails',
    description: 'Create concise summaries of customer support emails to reduce resolution time',
    fixed_rules_possible: false, needs_learning_from_data: false, unstructured_input: true,
    requires_content_generation: true, data_available: true, domain: 'Customer Support',
    additional_context: 'Email corpus with labelled categories and resolutions',
    expectedCategory: 'Generative AI', hint: 'The output is newly generated text, so an LLM is appropriate.',
  },
  {
    id: 'product_defect_detection',
    title: 'Detect defects in product photos',
    description: 'Identify manufacturing defects in product images on the assembly line',
    fixed_rules_possible: false, needs_learning_from_data: true, unstructured_input: true,
    requires_content_generation: false, data_available: true, domain: 'Manufacturing',
    additional_context: 'Product image dataset with labelled defects',
    expectedCategory: 'Deep Learning', hint: 'Image perception at scale is a deep-learning task.',
  },
  {
    id: 'gst_calculation',
    title: 'Calculate GST on an invoice',
    description: 'Calculate Goods and Services Tax on invoice amounts based on tax slabs',
    fixed_rules_possible: true, needs_learning_from_data: false, unstructured_input: false,
    requires_content_generation: false, data_available: false, domain: 'Finance',
    additional_context: 'GST rates vary by product category (5%, 12%, 18%, 28%)',
    expectedCategory: 'No AI', hint: 'Tax slabs are explicit rules; no learning is required.',
  },
  {
    id: 'demand_forecasting',
    title: 'Forecast weekly product demand',
    description: 'Predict weekly product demand based on historical sales data',
    fixed_rules_possible: false, needs_learning_from_data: true, unstructured_input: false,
    requires_content_generation: false, data_available: true, domain: 'Operations',
    additional_context: 'Historical weekly sales data for 3+ years',
    expectedCategory: 'Analytics / BI', hint: 'Trend analysis and descriptive forecasting fit BI tooling.',
  },
  {
    id: 'hr_policy_qa',
    title: 'Answer employee questions from an HR policy PDF',
    description: 'Enable employees to ask questions about HR policies and get accurate answers',
    fixed_rules_possible: false, needs_learning_from_data: false, unstructured_input: true,
    requires_content_generation: true, data_available: true, domain: 'HR',
    additional_context: 'HR policy document with Q&A pairs',
    expectedCategory: 'Generative AI', hint: 'Retrieval-augmented generation is the standard approach.',
  },
  {
    id: 'invoice_sorting',
    title: 'Sort invoices by amount',
    description: 'Sort invoices in descending order of amount for prioritised processing',
    fixed_rules_possible: true, needs_learning_from_data: false, unstructured_input: false,
    requires_content_generation: false, data_available: false, domain: 'Finance',
    additional_context: 'Invoice amounts are numeric values with currency information',
    expectedCategory: 'No AI', hint: 'Sorting is a basic deterministic operation.',
  },
  {
    id: 'fraud_detection',
    title: 'Detect fraudulent transactions',
    description: 'Identify potentially fraudulent credit card transactions in real-time',
    fixed_rules_possible: false, needs_learning_from_data: true, unstructured_input: false,
    requires_content_generation: false, data_available: true, domain: 'Finance',
    additional_context: 'Transaction dataset with labelled fraud cases',
    expectedCategory: 'Classical ML', hint: 'Labelled transaction data supports classification models.',
  },
  {
    id: 'customer_feedback',
    title: 'Classify customer feedback',
    description: 'Classify customer feedback as positive, neutral, or negative',
    fixed_rules_possible: false, needs_learning_from_data: true, unstructured_input: true,
    requires_content_generation: false, data_available: true, domain: 'Customer Success',
    additional_context: 'Customer feedback comments with sentiment labels',
    expectedCategory: 'Classical ML', hint: 'Text classification does not automatically require deep learning.',
  },
  {
    id: 'quality_control',
    title: 'Perform image-based quality control',
    description: 'Inspect products for surface scratches and cosmetic defects',
    fixed_rules_possible: false, needs_learning_from_data: true, unstructured_input: true,
    requires_content_generation: false, data_available: true, domain: 'Manufacturing',
    additional_context: 'High-resolution product images with defect labels',
    expectedCategory: 'Deep Learning', hint: 'Visual inspection with labelled images suits CNNs.',
  },
  {
    id: 'customer_chatbot',
    title: 'Build customer service chatbot',
    description: 'Create a chatbot to handle common customer inquiries and provide support',
    fixed_rules_possible: false, needs_learning_from_data: true, unstructured_input: true,
    requires_content_generation: true, data_available: true, domain: 'Customer Service',
    additional_context: 'Customer interaction history and knowledge base articles',
    expectedCategory: 'Generative AI', hint: 'Conversational generation is a generative AI use case.',
  },
  {
    id: 'stock_prediction',
    title: 'Predict stock price movement',
    description: 'Predict whether a stock price will go up or down next day',
    fixed_rules_possible: false, needs_learning_from_data: true, unstructured_input: false,
    requires_content_generation: false, data_available: true, domain: 'Finance',
    additional_context: 'Historical daily price data and trading volume for 5+ years',
    expectedCategory: 'Classical ML', hint: 'Structured numeric features support classical models.',
  },
  {
    id: 'route_optimization',
    title: 'Optimise delivery routes',
    description: 'Determine the most efficient delivery routes based on traffic and location data',
    fixed_rules_possible: false, needs_learning_from_data: true, unstructured_input: false,
    requires_content_generation: false, data_available: true, domain: 'Logistics',
    additional_context: 'GPS trajectory data, traffic patterns and delivery time windows',
    expectedCategory: 'Analytics / BI', hint: 'Operations research and analytics are sufficient here.',
  },
  {
    id: 'handform_parsing',
    title: 'Parse handwritten forms',
    description: 'Extract data from handwritten registration forms and applications',
    fixed_rules_possible: false, needs_learning_from_data: true, unstructured_input: true,
    requires_content_generation: false, data_available: true, domain: 'Healthcare',
    additional_context: 'Scanned handwritten forms with labelled fields',
    expectedCategory: 'Deep Learning', hint: 'Handwriting recognition relies on vision models.',
  },
]

export const emptyRequirement = (): RequirementInput => ({
  title: '',
  description: '',
  fixed_rules_possible: false,
  needs_learning_from_data: false,
  unstructured_input: false,
  requires_content_generation: false,
  data_available: false,
  domain: '',
  additional_context: '',
})
