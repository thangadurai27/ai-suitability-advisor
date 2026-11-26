"""Pydantic schemas for the AI Suitability Advisor backend.

Defines request/response models for the API, including requirement schemas,
analysis results, and user data models. All schemas use Pydantic v2 for
validation and documentation generation."""

from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime


# Enums
class DecisionCategory(str, Enum):
    """AI suitability categories."""
    NO_AI = "No AI"
    ANALYTICS_BI = "Analytics / BI"
    CLASSICAL_ML = "Classical ML"
    DEEP_LEARNING = "Deep Learning"
    GENERATIVE_AI = "Generative AI"


class DecisionRule(str, Enum):
    """Identifiers for decision rules that influenced the result."""
    RULE_1_FIXED_RULES_PREFERRED = "R1: Fixed rules can solve task adequately → prefer traditional programming over AI"
    RULE_2_NO_TRAINING_DATA = "R2: When training data is unavailable → explain limitation and propose data collection or baseline strategy"
    RULE_3_NO_AI_AUTOMATIC = "R3: Unstructured input does NOT automatically mean Deep Learning"
    RULE_4_FORECASTING_NO_ML = "R4: Not all forecasting requires ML"
    RULE_5_RULES_VS_ML = "R5: If fixed rules can solve task adequately, prefer traditional programming over AI"
    RULE_6_CONFLICTING_ATTRIBUTES = "R6: If requirement has conflicting attributes → apply transparent priority policy and explain ambiguity"
    RULE_7_ANALYTICS_BI = "R7: Descriptive reporting and statistical trend analysis → Analytics/BI"
    RULE_8_CLASSICAL_ML_PREDICTION = "R8: Structured-data prediction and classification → Classical ML"
    RULE_9_DEEP_LEARNING_PERCEPTION = "R9: Complex image, audio or other high-dimensional perception tasks → Deep Learning"
    RULE_10_GENERATIVE_AI_CONTENT = "R10: Content generation, summarisation, semantic QA and language generation → Generative AI"
    RULE_11_DOMAIN_KNOWLEDGE = "R11: Domain-specific fixed rules → prefer traditional programming"
    RULE_12_SCALABILITY_CONSIDERATION = "R12: Scalability and maintenance considerations → prefer non-AI when appropriate"


# Decision result schema
class DecisionEvidence(BaseModel):
    """Evidence supporting the decision."""
    rule_ids: List[DecisionRule] = Field(default_factory=list, description="List of decision rule identifiers that influenced the result")
    text_support: List[str] = Field(default_factory=list, description="Textual evidence supporting each rule")
    data_points: Dict[str, Any] = Field(default_factory=dict, description="Additional data points used in the decision")


class DecisionResult(BaseModel):
    """Structured result from the decision engine."""
    decision: DecisionCategory
    reasons: List[str] = Field(description="Clear reasons for the recommendation")
    evidence: DecisionEvidence
    alternative_approach: str = Field(description="Alternative approach if AI is not selected")
    risks: List[str] = Field(description=" identified risks and limitations")
    data_requirements: List[str] = Field(description="Required data for implementation")
    first_next_step: str = Field(description="First recommended next step")
    lifecycle: List[str] = Field(description="Five lifecycle stages for AI-suitable requirements")
    responsible_roles: List[str] = Field(description="Engineering roles responsible for each stage")
    decision_id: str = Field(default_factory=lambda: f"dec-{datetime.utcnow().timestamp()}")


# Requirement schema
class RequirementSchema(BaseModel):
    """Schema representing a business requirement for AI suitability assessment."""
    id: str = Field(default_factory=lambda: f"req-{datetime.utcnow().timestamp()}")
    title: str = Field(min_length=1, max_length=200, description="Requirement title")
    description: str = Field(min_length=1, description="Detailed business problem description")
    fixed_rules_possible: bool = Field(default=False, description="Whether fixed rules can solve the task adequately")
    needs_learning_from_data: bool = Field(default=False, description="Whether the problem needs learning from data")
    unstructured_input: bool = Field(default=False, description="Whether the input is unstructured (images, audio, text)")
    requires_content_generation: bool = Field(default=False, description="Whether content generation is required")
    data_available: bool = Field(default=False, description="Whether relevant data is available")
    domain: str = Field(default="", description="Business domain (e.g., finance, healthcare, retail)")
    additional_context: str = Field(default="", description="Optional additional context about the requirement")

    @validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title must not be empty")
        return v.strip()

    @validator("description")
    def description_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Description must not be empty")
        return v.strip()

    @validator("domain")
    def domain_not_empty(cls, v):
        if not v.strip():
            return ""
        return v.strip()


# Request/Response models

class RequirementCreate(BaseModel):
    """Request model for creating a new requirement."""
    id: Optional[str] = Field(default=None, max_length=100, description="Optional caller-supplied requirement ID")
    title: str = Field(min_length=1, max_length=200, description="Requirement title")
    description: str = Field(min_length=1, description="Detailed business problem description")
    fixed_rules_possible: bool = Field(default=False, description="Whether fixed rules can solve the task adequately")
    needs_learning_from_data: bool = Field(default=False, description="Whether the problem needs learning from data")
    unstructured_input: bool = Field(default=False, description="Whether the input is unstructured (images, audio, text)")
    requires_content_generation: bool = Field(default=False, description="Whether content generation is required")
    data_available: bool = Field(default=False, description="Whether relevant data is available")
    domain: str = Field(default="", description="Business domain (e.g., finance, healthcare, retail)")
    additional_context: str = Field(default="", description="Optional additional context about the requirement")

    @validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title must not be empty")
        return v.strip()

    @validator("description")
    def description_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Description must not be empty")
        return v.strip()


class RequirementResponse(RequirementSchema):
    """Response model for requirement data including database ID."""
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AnalyzeRequest(BaseModel):
    """Request model for the analysis endpoint."""
    title: str = Field(min_length=1, max_length=200, description="Requirement title")
    description: str = Field(min_length=1, description="Detailed business problem description")
    fixed_rules_possible: bool = Field(default=False, description="Whether fixed rules can solve the task adequately")
    needs_learning_from_data: bool = Field(default=False, description="Whether the problem needs learning from data")
    unstructured_input: bool = Field(default=False, description="Whether the input is unstructured (images, audio, text)")
    requires_content_generation: bool = Field(default=False, description="Whether content generation is required")
    data_available: bool = Field(default=False, description="Whether relevant data is available")
    domain: str = Field(default="", description="Business domain (e.g., finance, healthcare, retail)")
    additional_context: str = Field(default="", description="Optional additional context about the requirement")

    @validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title must not be empty")
        return v.strip()

    @validator("description")
    def description_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Description must not be empty")
        return v.strip()


class AnalysisResult(BaseModel):
    """Response model for analysis results."""
    id: str
    requirement_id: str
    title: str
    decision_category: DecisionCategory
    reasons: List[str]
    evidence_rule_ids: List[str] = Field(default_factory=list, description="Rule identifiers that influenced the decision")
    evidence: DecisionEvidence
    alternative_approach: str
    risks: List[str]
    data_requirements: List[str]
    first_next_step: str
    lifecycle: List[str]
    responsible_roles: List[str]
    created_at: datetime


# Analytics summary
class AnalyticsSummary(BaseModel):
    """Analytics summary of all analyses."""
    total_analyses: int = Field(description="Total number of analyses performed")
    no_ai: int = Field(description="Count of No AI recommendations")
    analytics_bi: int = Field(description="Count of Analytics / BI recommendations")
    classical_ml: int = Field(description="Count of Classical ML recommendations")
    deep_learning: int = Field(description="Count of Deep Learning recommendations")
    generative_ai: int = Field(description="Count of Generative AI recommendations")


# CSV export
class CSVExport(BaseModel):
    """CSV export model."""
    csv_content: str = Field(description="CSV formatted data")
    record_count: int = Field(description="Number of records in the CSV")


# PDF export
class PDFExport(BaseModel):
    """PDF export model."""
    analysis_id: str = Field(description="Analysis ID")
    pdf_generated: bool = Field(description="Whether PDF was successfully generated")
    report_title: str = Field(description="Report title")
    content: str = Field(description="Report content summary")


# Health check
class HealthCheck(BaseModel):
    """Health check response model."""
    status: str = Field(description="Service status")
    version: str = Field(description="API version")
    database: str = Field(description="Database connection status")