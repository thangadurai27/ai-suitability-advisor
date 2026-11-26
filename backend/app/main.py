"""FastAPI application entry point for AI Suitability Advisor.

Public demo mode: all endpoints are available without registration.
"""

from __future__ import annotations

import json
import logging
import os
from contextlib import asynccontextmanager
from typing import Any
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

from .core.decision_engine import (
    RequirementSchema as EngineRequirement,
    decide_ai_suitability,
    validate_requirement_schema,
)
from .database import Base, engine, get_db, init_db
from .models import Analysis, Requirement, User
from .schemas import (
    AnalysisResult,
    AnalyticsSummary,
    DecisionCategory,
    DecisionEvidence,
    HealthCheck,
    RequirementCreate,
    RequirementResponse,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create tables and preload demo data on startup."""
    init_db()
    try:
        from .seed import create_seed_data

        create_seed_data()
    except Exception:
        logger.exception("Seeding failed; application will still start")
    yield


app = FastAPI(
    title="AI Suitability Advisor",
    description="Intelligent business technology decision platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

_default_origins = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"
allowed_origins = [o.strip() for o in os.getenv("CORS_ORIGINS", _default_origins).split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _as_list(value: Any, fallback: list | None = None) -> list:
    """Decode JSON-serialised list columns, tolerating legacy plain strings."""
    fallback = fallback if fallback is not None else []
    if not value:
        return fallback
    if isinstance(value, list):
        return value
    try:
        decoded = json.loads(value)
        return decoded if isinstance(decoded, list) else [str(decoded)]
    except (ValueError, TypeError):
        return [str(value)]


def _pdf_bytes(title: str, lines: list[str]) -> bytes:
    """Build a small, valid single-page PDF without external dependencies."""

    def esc(text: str) -> str:
        return (
            text.replace("\\", "\\\\")
            .replace("(", "\\(")
            .replace(")", "\\)")
            .encode("ascii", "replace")
            .decode("ascii")
        )

    content_lines = ["BT", "/F1 16 Tf", "56 736 Td", f"({esc(title)}) Tj", "/F1 11 Tf", "18 TL"]
    for line in lines[:52]:
        safe = "".join(ch for ch in str(line) if ch.isprintable())
        content_lines.append(f"T* ({esc(safe[:100])}) Tj")
    content_lines.append("ET")
    stream = "\n".join(content_lines).encode("latin-1", "replace")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]

    output = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode() + body + b"\nendobj\n")
    xref_offset = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets:
        output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode()
    )
    return bytes(output)


@app.get("/api/health", response_model=HealthCheck, tags=["Health"])
async def health_check() -> HealthCheck:
    return HealthCheck(status="healthy", version="1.0.0", database="connected")


@app.get("/api/requirements", response_model=list[RequirementResponse], tags=["Requirements"])
async def list_requirements(db: Session = Depends(get_db)) -> list[Requirement]:
    from .crud import get_requirements

    return get_requirements(db)


@app.post("/api/requirements", response_model=RequirementResponse, tags=["Requirements"])
async def create_new_requirement(
    payload: RequirementCreate, db: Session = Depends(get_db)
) -> Requirement:
    from .crud import create_requirement, get_requirement

    requirement_id = payload.id or f"req-{uuid4()}"
    if get_requirement(db, requirement_id):
        raise HTTPException(status_code=409, detail="Requirement ID already exists")
    return create_requirement(
        db,
        requirement_id=requirement_id,
        title=payload.title,
        description=payload.description,
        fixed_rules_possible=payload.fixed_rules_possible,
        needs_learning_from_data=payload.needs_learning_from_data,
        unstructured_input=payload.unstructured_input,
        requires_content_generation=payload.requires_content_generation,
        data_available=payload.data_available,
        domain=payload.domain,
        additional_context=payload.additional_context,
    )


@app.post("/api/analyze", response_model=AnalysisResult, tags=["Analysis"])
async def analyze_requirement(
    payload: RequirementCreate, db: Session = Depends(get_db)
) -> AnalysisResult:
    """Evaluate a requirement and persist the explainable result."""
    from .crud import create_analysis, create_requirement, get_requirement

    req_schema = EngineRequirement(
        id=payload.id or f"req-{uuid4()}",
        title=payload.title,
        description=payload.description,
        fixed_rules_possible=payload.fixed_rules_possible,
        needs_learning_from_data=payload.needs_learning_from_data,
        unstructured_input=payload.unstructured_input,
        requires_content_generation=payload.requires_content_generation,
        data_available=payload.data_available,
        domain=payload.domain,
        additional_context=payload.additional_context or "",
    )

    if not validate_requirement_schema(req_schema):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid requirement schema: missing required attributes.",
        )

    result = decide_ai_suitability(req_schema)

    db_requirement = get_requirement(db, req_schema.id)
    if not db_requirement:
        db_requirement = create_requirement(
            db,
            requirement_id=req_schema.id,
            title=payload.title,
            description=payload.description,
            fixed_rules_possible=payload.fixed_rules_possible,
            needs_learning_from_data=payload.needs_learning_from_data,
            unstructured_input=payload.unstructured_input,
            requires_content_generation=payload.requires_content_generation,
            data_available=payload.data_available,
            domain=payload.domain,
            additional_context=payload.additional_context or "",
        )

    db_analysis = create_analysis(
        db,
        requirement_id=db_requirement.id,
        title=payload.title,
        decision_category=result.decision.value,
        reasons=result.reasons,
        evidence_rule_ids=[rule.value for rule in result.evidence.rule_ids],
        alternative_approach=result.alternative_approach,
        risks=result.risks,
        data_requirements=result.data_requirements,
        first_next_step=result.first_next_step,
        lifecycle=result.lifecycle,
        responsible_roles=result.responsible_roles,
    )

    return AnalysisResult(
        id=db_analysis.id,
        requirement_id=db_analysis.requirement_id,
        title=db_analysis.title,
        decision_category=DecisionCategory(result.decision.value),
        reasons=result.reasons,
        evidence_rule_ids=[rule.value for rule in result.evidence.rule_ids],
        evidence=DecisionEvidence(
            rule_ids=[rule.value for rule in result.evidence.rule_ids],
            text_support=result.evidence.text_support,
            data_points=result.evidence.data_points,
        ),
        alternative_approach=result.alternative_approach,
        risks=result.risks,
        data_requirements=result.data_requirements,
        first_next_step=result.first_next_step,
        lifecycle=result.lifecycle,
        responsible_roles=result.responsible_roles,
        created_at=db_analysis.created_at,
    )


@app.get("/api/analyses", tags=["Analysis"])
async def list_analyses(db: Session = Depends(get_db)) -> list[dict]:
    from .crud import get_analyses

    analyses = get_analyses(db)
    return [
        {
            "id": a.id,
            "requirement_id": a.requirement_id,
            "title": a.title,
            "decision_category": a.decision_category,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in analyses
    ]


@app.get("/api/analyses/{analysis_id}", tags=["Analysis"])
async def get_analysis_detail(analysis_id: str, db: Session = Depends(get_db)) -> dict:
    from .crud import get_analysis

    analysis = get_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail=f"Analysis with ID {analysis_id} not found")
    return {
        "id": analysis.id,
        "requirement_id": analysis.requirement_id,
        "title": analysis.title,
        "decision_category": analysis.decision_category,
        "reasons": _as_list(analysis.reasons),
        "evidence_rule_ids": _as_list(analysis.evidence_rule_ids),
        "alternative_approach": analysis.alternative_approach or "",
        "risks": _as_list(analysis.risks),
        "data_requirements": _as_list(analysis.data_requirements),
        "first_next_step": analysis.first_next_step or "",
        "lifecycle": _as_list(analysis.lifecycle),
        "responsible_roles": _as_list(analysis.responsible_roles),
        "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
    }


@app.delete("/api/analyses/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Analysis"])
async def delete_analysis(analysis_id: str, db: Session = Depends(get_db)) -> None:
    from .crud import delete_analysis

    if not delete_analysis(db, analysis_id):
        raise HTTPException(status_code=404, detail=f"Analysis with ID {analysis_id} not found")


@app.get("/api/analytics/summary", response_model=AnalyticsSummary, tags=["Analytics"])
async def analytics_summary(db: Session = Depends(get_db)) -> AnalyticsSummary:
    from .crud import get_analysis_counts_by_category

    counts = get_analysis_counts_by_category(db)
    return AnalyticsSummary(
        total_analyses=sum(counts.values()),
        no_ai=counts.get("No AI", 0),
        analytics_bi=counts.get("Analytics / BI", 0),
        classical_ml=counts.get("Classical ML", 0),
        deep_learning=counts.get("Deep Learning", 0),
        generative_ai=counts.get("Generative AI", 0),
    )


@app.get("/api/reports/csv", tags=["Reports"])
async def export_csv(db: Session = Depends(get_db)) -> Response:
    from .crud import export_csv_report

    return Response(
        content=export_csv_report(db),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="ai_suitability_analyses.csv"'},
    )


@app.get("/api/reports/{analysis_id}/pdf", tags=["Reports"])
async def export_pdf(analysis_id: str, db: Session = Depends(get_db)) -> Response:
    from .crud import get_analysis

    analysis = get_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail=f"Analysis with ID {analysis_id} not found")
    lines = [
        f"Analysis ID: {analysis.id}",
        f"Category: {analysis.decision_category}",
        "Reasons: " + "; ".join(_as_list(analysis.reasons)),
        "Risks: " + "; ".join(_as_list(analysis.risks)),
        "Next step: " + (analysis.first_next_step or "N/A"),
    ]
    return Response(
        content=_pdf_bytes(f"AI Suitability Analysis: {analysis.title}", lines),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="analysis_{analysis.id}.pdf"'},
    )


@app.post("/api/reports/all", tags=["Reports"])
async def export_all_report(db: Session = Depends(get_db)) -> Response:
    from .crud import get_analyses

    analyses = get_analyses(db)
    lines = [f"{a.title} - {a.decision_category}" for a in analyses]
    return Response(
        content=_pdf_bytes("AI Suitability Advisor - Complete Analysis Report", lines or ["No analyses yet"]),
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="all_analyses_report.pdf"'},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Any, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def general_exception_handler(_: Any, exc: Exception):
    logger.exception("Unexpected error: %s", exc)
    return JSONResponse(
        status_code=500, content={"detail": "An unexpected error occurred. Please try again later."}
    )
