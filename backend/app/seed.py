"""Seed the database with 15 demo requirements and their analysed results.

Run with ``python seed.py`` from the backend directory, or let the FastAPI
startup event call ``create_seed_data`` automatically.
"""

from __future__ import annotations

import hashlib
from uuid import uuid4

from sqlalchemy.orm import Session

from .core.decision_engine import RequirementSchema, decide_ai_suitability
from .crud import create_analysis
from .database import Base, SessionLocal, engine
from .models import Analysis, Requirement, User

# 10 required examples + 5 extensions.
SAMPLES: list[dict] = [
    {
        "id": "pan_validation",
        "title": "Validate PAN number format",
        "description": "Validate Permanent Account Number (PAN) card format for Indian income tax purposes",
        "fixed_rules_possible": True, "needs_learning_from_data": False,
        "unstructured_input": False, "requires_content_generation": False,
        "data_available": False, "domain": "Finance",
        "additional_context": "PAN numbers are 10-character alphanumeric identifiers",
    },
    {
        "id": "customer_cancellation",
        "title": "Predict which customers will cancel next month",
        "description": "Identify customers at risk of churning based on usage patterns and demographics",
        "fixed_rules_possible": False, "needs_learning_from_data": True,
        "unstructured_input": False, "requires_content_generation": False,
        "data_available": True, "domain": "Marketing",
        "additional_context": "Historical customer data with 2 years of usage history",
    },
    {
        "id": "support_email_summarisation",
        "title": "Summarise long support emails",
        "description": "Create concise summaries of customer support emails to reduce resolution time",
        "fixed_rules_possible": False, "needs_learning_from_data": False,
        "unstructured_input": True, "requires_content_generation": True,
        "data_available": True, "domain": "Customer Support",
        "additional_context": "Email corpus with labelled categories and resolutions",
    },
    {
        "id": "product_defect_detection",
        "title": "Detect defects in product photos",
        "description": "Identify manufacturing defects in product images on the assembly line",
        "fixed_rules_possible": False, "needs_learning_from_data": True,
        "unstructured_input": True, "requires_content_generation": False,
        "data_available": True, "domain": "Manufacturing",
        "additional_context": "Product image dataset with labelled defects",
    },
    {
        "id": "gst_calculation",
        "title": "Calculate GST on an invoice",
        "description": "Calculate Goods and Services Tax on invoice amounts based on tax slabs",
        "fixed_rules_possible": True, "needs_learning_from_data": False,
        "unstructured_input": False, "requires_content_generation": False,
        "data_available": False, "domain": "Finance",
        "additional_context": "GST rates vary by product category (5%, 12%, 18%, 28%)",
    },
    {
        "id": "demand_forecasting",
        "title": "Forecast weekly product demand",
        "description": "Predict weekly product demand based on historical sales data",
        "fixed_rules_possible": False, "needs_learning_from_data": True,
        "unstructured_input": False, "requires_content_generation": False,
        "data_available": True, "domain": "Operations",
        "additional_context": "Historical weekly sales data for 3+ years",
    },
    {
        "id": "hr_policy_qa",
        "title": "Answer employee questions from an HR policy PDF",
        "description": "Enable employees to ask questions about HR policies and get accurate answers",
        "fixed_rules_possible": False, "needs_learning_from_data": False,
        "unstructured_input": True, "requires_content_generation": True,
        "data_available": True, "domain": "HR",
        "additional_context": "HR policy document with Q&A pairs",
    },
    {
        "id": "invoice_sorting",
        "title": "Sort invoices by amount",
        "description": "Sort invoices in descending order of amount for prioritised processing",
        "fixed_rules_possible": True, "needs_learning_from_data": False,
        "unstructured_input": False, "requires_content_generation": False,
        "data_available": False, "domain": "Finance",
        "additional_context": "Invoice amounts are numeric values with currency information",
    },
    {
        "id": "fraud_detection",
        "title": "Detect fraudulent transactions",
        "description": "Identify potentially fraudulent credit card transactions in real-time",
        "fixed_rules_possible": False, "needs_learning_from_data": True,
        "unstructured_input": False, "requires_content_generation": False,
        "data_available": True, "domain": "Finance",
        "additional_context": "Transaction dataset with labelled fraud cases",
    },
    {
        "id": "customer_feedback",
        "title": "Classify customer feedback",
        "description": "Classify customer feedback as positive, neutral, or negative",
        "fixed_rules_possible": False, "needs_learning_from_data": True,
        "unstructured_input": True, "requires_content_generation": False,
        "data_available": True, "domain": "Customer Success",
        "additional_context": "Customer feedback comments with sentiment labels",
    },
    {
        "id": "quality_control",
        "title": "Perform image-based quality control",
        "description": "Inspect products for surface scratches and cosmetic defects",
        "fixed_rules_possible": False, "needs_learning_from_data": True,
        "unstructured_input": True, "requires_content_generation": False,
        "data_available": True, "domain": "Manufacturing",
        "additional_context": "High-resolution product images with defect labels",
    },
    {
        "id": "customer_chatbot",
        "title": "Build customer service chatbot",
        "description": "Create a chatbot to handle common customer inquiries and provide support",
        "fixed_rules_possible": False, "needs_learning_from_data": True,
        "unstructured_input": True, "requires_content_generation": True,
        "data_available": True, "domain": "Customer Service",
        "additional_context": "Customer interaction history and knowledge base articles",
    },
    {
        "id": "stock_prediction",
        "title": "Predict stock price movement",
        "description": "Predict whether a stock price will go up or down next day",
        "fixed_rules_possible": False, "needs_learning_from_data": True,
        "unstructured_input": False, "requires_content_generation": False,
        "data_available": True, "domain": "Finance",
        "additional_context": "Historical daily price data and trading volume for 5+ years",
    },
    {
        "id": "route_optimization",
        "title": "Optimise delivery routes",
        "description": "Determine the most efficient delivery routes based on traffic and location data",
        "fixed_rules_possible": False, "needs_learning_from_data": True,
        "unstructured_input": False, "requires_content_generation": False,
        "data_available": True, "domain": "Logistics",
        "additional_context": "GPS trajectory data, traffic patterns and delivery time windows",
    },
    {
        "id": "handform_parsing",
        "title": "Parse handwritten forms",
        "description": "Extract data from handwritten registration forms and applications",
        "fixed_rules_possible": False, "needs_learning_from_data": True,
        "unstructured_input": True, "requires_content_generation": False,
        "data_available": True, "domain": "Healthcare",
        "additional_context": "Scanned handwritten forms with labelled fields",
    },
]


def _engine_schema(data: dict) -> RequirementSchema:
    return RequirementSchema(
        id=data["id"],
        title=data["title"],
        description=data["description"],
        fixed_rules_possible=data["fixed_rules_possible"],
        needs_learning_from_data=data["needs_learning_from_data"],
        unstructured_input=data["unstructured_input"],
        requires_content_generation=data["requires_content_generation"],
        data_available=data["data_available"],
        domain=data["domain"],
        additional_context=data.get("additional_context", ""),
    )


def create_seed_data() -> None:
    """Idempotently create tables, demo requirements and their analyses."""
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "demo@ai-suitability-advisor.com").first():
            db.add(
                User(
                    id=f"user-{uuid4()}",
                    email="demo@ai-suitability-advisor.com",
                    hashed_password=hashlib.sha256(b"demo1234").hexdigest(),
                )
            )

        for data in SAMPLES:
            if not db.query(Requirement).filter(Requirement.id == data["id"]).first():
                db.add(
                    Requirement(
                        id=data["id"],
                        title=data["title"],
                        description=data["description"],
                        fixed_rules_possible=data["fixed_rules_possible"],
                        needs_learning_from_data=data["needs_learning_from_data"],
                        unstructured_input=data["unstructured_input"],
                        requires_content_generation=data["requires_content_generation"],
                        data_available=data["data_available"],
                        domain=data["domain"],
                        additional_context=data.get("additional_context", ""),
                        owner_id=None,
                    )
                )
        db.commit()

        for data in SAMPLES:
            if db.query(Analysis).filter(Analysis.requirement_id == data["id"]).first():
                continue
            result = decide_ai_suitability(_engine_schema(data))
            create_analysis(
                db,
                requirement_id=data["id"],
                title=data["title"],
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
    finally:
        db.close()


if __name__ == "__main__":
    create_seed_data()
    print(f"Seed complete: {len(SAMPLES)} requirements and analyses are available.")
