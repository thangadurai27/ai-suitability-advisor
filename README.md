# AI Suitability Advisor

## Intelligent Business Technology Decision Platform

### Project Overview

**AI Suitability Advisor** is a production-ready full-stack SaaS web application that helps businesses evaluate whether AI is actually necessary for their technology requirements. The platform recommends the most suitable technology approach from five categories:

1. **No AI** (Traditional Programming / Rules)
2. **Analytics / Business Intelligence**
3. **Classical Machine Learning**
4. **Deep Learning**
5. **Generative AI**

The system provides explainable recommendations with decision rule identifiers, data requirements, risks, lifecycle roadmaps, and responsible engineering roles.

---

## Problem Statement

Businesses frequently request AI solutions without knowing whether AI is actually necessary. This platform solves that problem by providing a structured, rule-based decision engine that evaluates business requirements and recommends the most suitable technology approach. The system emphasizes explainability and practical engineering decisions over "AI for AI's sake."

---

## Features

### Core Features

- **Requirement Analysis**: Input business problems and receive technology recommendations
- **Decision Engine**: Rule-based engine with 12 transparent decision rules
- **Analysis History**: View, search, and filter previously analysed requirements
- **Requirements Library**: Preloaded example requirements with search and filters
- **Reporting**: CSV and PDF export of analysis results
- **Learning Center**: Educational content about AI/ML concepts and engineering roles
- **Sample Data Playground**: Demo mode that works without registration

### Decision Categories

The engine recommends exactly one of:

- **No AI** - When fixed rules can solve the task adequately
- **Analytics / BI** - When descriptive reporting and statistical trend analysis suffice
- **Classical ML** - When structured-data prediction or classification is needed
- **Deep Learning** - When complex image, audio, or high-dimensional perception tasks
- **Generative AI** - When content generation, summarisation, or language generation is needed

### Decision Rules (R1-R12)

1. R1: Fixed rules can solve task adequately → prefer traditional programming over AI
2. R2: When training data is unavailable → explain limitation and propose data collection
3. R3: Unstructured input does NOT automatically mean Deep Learning
4. R4: Not all forecasting requires ML
5. R5: If fixed rules can solve task adequately, prefer traditional programming over AI
6. R6: If requirement has conflicting attributes → apply transparent priority policy
7. R7: Descriptive reporting and statistical trend analysis → Analytics/BI
8. R8: Structured-data prediction and classification → Classical ML
9. R9: Complex image, audio, or high-dimensional perception tasks → Deep Learning
10. R10: Content generation, summarisation, semantic QA and language generation → Generative AI
11. R11: Domain-specific fixed rules → prefer traditional programming
12. R12: Scalability and maintenance considerations → prefer non-AI when appropriate

---

## Technology Stack

### Frontend

- **React 18** with TypeScript and strict type checking
- **Vite 5** for the development server and production build
- **Tailwind CSS 3** for styling (navy / violet / blue accents)
- **React Router 6** for navigation
- **Lucide React** for icons
- **Recharts** for charts (installed)
- A small typed `fetch` client with a Vite `/api` proxy to the backend

### Backend

- **FastAPI** (Python 3.11+)
- **SQLAlchemy** 2.0 ORM with one shared declarative `Base`
- **Pydantic v2** for request/response validation
- **PostgreSQL** via `DATABASE_URL`; zero-setup SQLite by default
- **Pytest** for decision-engine tests
- Demo/anonymous mode — no registration or JWT required

### Infrastructure

- **Docker** and **Docker Compose** for local development
- **Vercel** for frontend deployment
- **Render** for backend deployment
- **Supabase** for managed PostgreSQL

---

## Architecture

```mermaid
graph TD
    subgraph Frontend ["React Frontend"]
        A[Landing Page] --> B[Dashboard]
        B --> C[Requirement Analyzer]
        C --> D[Analysis Results]
        D --> E[Requirements Library]
        D --> F[Analysis History]
        D --> G[Reports]
        D --> H[Learning Center]
        D --> I[Settings]
    end

    subgraph Backend ["FastAPI Backend"]
        J[API Routes] --> K[Decision Engine]
        K --> L[Requirement Schema Validation]
        L --> M[Database (PostgreSQL/SQLite)]
        M --> N[Analytics Summary]
        N --> O[Report Generation]
    end

    style Frontend fill:#e8f0fe,stroke:#1d4ed8,stroke-width:2px
    style Backend fill:#d1d9e1,stroke:#374151,stroke-width:2px
```

---

## Installation

### Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Git

### One-click launch (Windows)

Double-click `C:\TechMahindra\Day1\Run_Application.bat`. It starts the API on port 8000,
the Vite dev server on port 5173, and opens the website. Close the two server windows to stop.

### Backend Setup

```bash
# 1. Navigate to backend
cd ai-suitability-advisor/backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file in backend (example lives at project root)
cp ../.env.example .env
# Edit .env with your configuration (SQLite works without any edits)

# 4. Create tables and preload 15 demo requirements/analyses
python setup_db.py
# (the API also does this automatically on startup)

# 5. Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# 1. Navigate to frontend
cd ai-suitability-advisor/frontend

# 2. Install dependencies
npm install

# 3. Start the development server
npm run dev
```

### Environment Variables

Create `.env` in the backend directory:

```
DATABASE_URL="sqlite:///./ai_suitability_advisor.db"
SECRET_KEY="your-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS="http://localhost:5173,http://localhost:3000"
```

---

## API Documentation

### Health Check

```
GET /api/health
```

Returns service health status and database connection.

### Requirement Analysis

```
POST /api/analyze
```

Takes a requirement object and returns analysis results including:
- Recommended category
- Decision reasons and rule IDs
- Risks and data requirements
- First next step and lifecycle roadmap

### Analysis History

```
GET /api/analyses
GET /api/analyses/{analysis_id}
DELETE /api/analyses/{analysis_id}
```

### Analytics

```
GET /api/analytics/summary
```

Returns count of analyses by category.

### Reports

```
GET /api/reports/csv
GET /api/reports/{analysis_id}/pdf
```

---

## Sample Requirements (Preloaded)

The following 10 sample requirements are preloaded in the system:

| # | Requirement | Category | Decision Rule |
|---|-----------|----------|---------------|
| 1 | Validate PAN number format | No AI | R1, R5 |
| 2 | Predict customer cancellation | Classical ML | R8 |
| 3 | Summarise long support emails | Generative AI | R10 |
| 4 | Detect defects in product photos | Deep Learning | R3, R9 |
| 5 | Calculate GST on an invoice | No AI | R1, R5 |
| 6 | Forecast weekly product demand | Analytics / BI | R4, R7 |
| 7 | Answer employee questions from HR policy PDF | Generative AI | R10 |
| 8 | Sort invoices by amount | No AI | R1, R5 |
| 9 | Detect fraudulent transactions | Classical ML | R8 |
| 10 | Classify customer feedback | Classical ML | R8, R3 |

Plus 5 additional realistic sample requirements are available in the Requirements Library.

---

## Decision Engine

The decision engine implements structured, rule-based calculations:

- **Deterministic calculations** are normally "No AI"
- **Descriptive reporting** is "Analytics / BI"
- **Structured-data prediction/classification** is "Classical ML"
- **Complex perception tasks** are "Deep Learning"
- **Content generation** is "Generative AI"

Every result includes:
- Decision category with explanation
- Clear reasons for the recommendation
- Decision rule identifiers (R1-R12)
- Evidence supporting the decision
- Alternative approach description
- Identified risks and limitations
- Data requirements
- First recommended next step
- 5-stage AI lifecycle roadmap
- Responsible engineering roles

---

## Testing

### Decision Engine Tests

All 16 decision engine tests pass, verifying:

- PAN validation → No AI
- GST calculation → No AI
- Invoice sorting → No AI
- Customer cancellation → Classical ML
- Product defect detection → Deep Learning
- Email summarisation → Generative AI
- HR policy QA → Generative AI
- Demand forecasting → Analytics / BI
- Fraud detection → Classical ML
- Customer feedback → Classical ML
- Lifecycle has 5 stages for AI-suitable requirements
- Rule IDs included in evidence
- Reasons provided for every classification
- Data requirements for AI-suitable requirements
- Alternative approach always provided
- Responsible roles always provided

Run tests:

```bash
cd ai-suitability-advisor/backend
python -m pytest tests/ -v
```

---

## Deployment

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Set the build command: `npm run build`
3. Set the output directory: `dist`
4. Add environment variable: `VITE_API_URL=https://your-backend.onrender.com`
5. Deploy

### Backend (Render)

1. Create a new Web Service on Render
2. Set the build command: `pip install -r requirements.txt`
3. Set the start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env`
5. Add PostgreSQL database service
6. Deploy

### Docker Compose

```bash
docker-compose up --build
```

This builds both images and serves the compiled frontend through nginx on port 5173,
proxying `/api` to the FastAPI backend on port 8000. Data is kept in a named volume.

### Docker

Individual Dockerfiles are available for both frontend and backend.

---

## Future Improvements

- User authentication and authorization
- PostgreSQL production deployment
- Advanced report generation with templates
- LLM integration for enhanced natural language processing
- Real-time collaboration features
- API rate limiting and enhanced security
- Multi-tenant architecture for SaaS scaling

---

## Engineering Quality Requirements

- Clean architecture and modular code
- Reusable frontend components
- TypeScript used properly (minimal `any` types)
- Pydantic schemas for all API requests/responses
- Meaningful comments and docstrings
- Loading, empty, and error states handled
- All navigation and buttons functional
- Application works with sample data
- No fake charts or fabricated statistics
- No non-functional placeholders
- No TODOs for core features

---

## Authors

Senior AI Engineer / Full-Stack Developer - AI Suitability Advisor Platform

---
*This is a professional, accessible, production-ready AI/ML SaaS application, not merely an academic demonstration.*