import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

function RichText({ text }: { text: string }) {
  return (
    <>
      {text.split(/(\*\*[^*]+\*\*)/g).map((part, index) =>
        part.startsWith('**') && part.endsWith('**') ? (
          <strong key={index} className="font-semibold text-foreground">{part.slice(2, -2)}</strong>
        ) : (
          <span key={index}>{part}</span>
        ),
      )}
    </>
  )
}

const sections: Array<{ title: string; items: string[] }> = [
  {
    title: 'AI vs ML vs Deep Learning vs Generative AI',
    items: [
      '**Artificial Intelligence (AI)** is the broad field of computing systems that perform tasks normally requiring human intelligence.',
      '**Machine Learning (ML)** is a subset of AI that learns patterns from data without being explicitly programmed for each task.',
      '**Deep Learning** uses multi-layer neural networks for complex patterns in large datasets.',
      '**Generative AI** creates new content — text, images, audio or video — that resembles human-generated material.',
    ],
  },
  {
    title: 'Supervised and unsupervised learning',
    items: [
      '**Supervised learning** trains on labelled inputs and outputs for classification and regression.',
      '**Unsupervised learning** discovers structure in unlabelled data, for example clustering with k-means or dimensionality reduction with PCA.',
    ],
  },
  {
    title: 'Classification and regression',
    items: [
      '**Classification** predicts a discrete label: spam detection, sentiment analysis, fraud detection.',
      '**Regression** predicts a continuous number: price prediction, demand forecasting, risk scoring.',
    ],
  },
  {
    title: 'Computer vision',
    items: [
      'Computer vision enables systems to derive meaning from images and video. Typical tasks include image classification, object detection and segmentation.',
      'It is powerful but expensive: prefer classical ML or simple rules when the perception task is trivial.',
    ],
  },
  {
    title: 'NLP, LLMs and RAG',
    items: [
      '**NLP** covers text classification, entity extraction, translation and generation.',
      '**LLMs** are large transformer-based language models trained on broad text corpora.',
      '**RAG (Retrieval-Augmented Generation)** grounds model answers in retrieved documents, improving accuracy and reducing hallucination for question answering.',
    ],
  },
  {
    title: 'The five-stage AI lifecycle',
    items: [
      '1. **Problem Framing** — define the problem, success metrics and constraints.',
      '2. **Data Collection and Preparation** — gather, clean and preprocess data.',
      '3. **Model Development** — train, tune and validate the model.',
      '4. **Deployment** — release the model into production infrastructure.',
      '5. **Monitoring and Improvement** — track performance and retrain when needed.',
    ],
  },
  {
    title: 'Engineering roles',
    items: [
      '**Product Owner / Business Analyst** — define value, scope and success criteria.',
      '**Data Engineer** — build reliable data pipelines and ensure data quality.',
      '**Data Scientist** — analyse data, select models and evaluate results.',
      '**ML / Deep Learning Engineer** — implement, scale and operate models.',
      '**AI Engineer** — design LLM and RAG systems with safety controls.',
      '**Backend and DevOps Engineers** — integrate services, CI/CD, monitoring and scaling.',
    ],
  },
  {
    title: 'When NOT to use AI',
    items: [
      'When deterministic rules solve the problem adequately.',
      'When training data is unavailable or too costly to collect.',
      'When outcomes must be fully deterministic and explainable.',
      'When implementation and operating costs outweigh the benefit.',
      'When errors could cause serious harm without strong safeguards.',
    ],
  },
]

export default function LearningCenter() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
      <header>
        <h1 className="text-3xl font-bold">Learning center</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Concepts behind the recommendations and the technology categories.
        </p>
      </header>

      <div className="mt-8 space-y-6">
        {sections.map((section) => (
          <Card key={section.title}>
            <CardHeader><CardTitle>{section.title}</CardTitle></CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                {section.items.map((item) => (
                  <li key={item} className="flex gap-2">
                    <span className="text-primary">•</span>
                    <span><RichText text={item} /></span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
