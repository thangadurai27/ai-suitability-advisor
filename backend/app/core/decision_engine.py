"""Decision engine for AI suitability assessment.

This module implements a structured, rule-based decision engine that evaluates
business requirements and recommends the most suitable technology approach:
1. No AI (Traditional Programming / Rules)
2. Analytics / Business Intelligence
3. Classical Machine Learning
4. Deep Learning
5. Generative AI

The engine follows deterministic calculations with transparent priority policies
and provides explainable results with decision rule identifiers.
"""

from __future__ import annotations
from dataclasses import dataclass, field

from enum import Enum, auto
from typing import Any, Dict, List, Optional


class DecisionCategory(Enum):
    """AI suitability categories."""

    NO_AI = "No AI"
    ANALYTICS_BI = "Analytics / BI"
    CLASSICAL_ML = "Classical ML"
    DEEP_LEARNING = "Deep Learning"
    GENERATIVE_AI = "Generative AI"


class DecisionRule(Enum):
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


@dataclass
class DecisionEvidence:
    """Evidence supporting the decision."""

    rule_ids: List[DecisionRule] = field(default_factory=list)
    text_support: List[str] = field(default_factory=list)
    data_points: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecisionResult:
    """Structured result from the decision engine."""

    decision: DecisionCategory
    reasons: List[str]
    evidence: DecisionEvidence
    alternative_approach: str
    risks: List[str]
    data_requirements: List[str]
    first_next_step: str
    lifecycle: List[str]
    responsible_roles: List[str]
    decision_id: str = field(default_factory=lambda: "decision-")


@dataclass
class RequirementSchema:
    """Schema representing a business requirement."""

    id: str
    title: str
    description: str
    fixed_rules_possible: bool
    needs_learning_from_data: bool
    unstructured_input: bool
    requires_content_generation: bool
    data_available: bool
    domain: str
    additional_context: str = ""


@dataclass
class DecisionEngineConfig:
    """Configuration for the decision engine."""

    priority_policy: List[DecisionRule] = field(default_factory=lambda: [
        DecisionRule.RULE_1_FIXED_RULES_PREFERRED,
        DecisionRule.RULE_2_NO_TRAINING_DATA,
        DecisionRule.RULE_5_RULES_VS_ML,
        DecisionRule.RULE_11_DOMAIN_KNOWLEDGE,
        DecisionRule.RULE_12_SCALABILITY_CONSIDERATION,
    ])
    ambiguity_policy: str = "Apply transparent priority: fixed_rules_possible > data_available > needs_learning_from_data > unstructured_input > requires_content_generation"


def decide_ai_suitability(requirement: RequirementSchema) -> DecisionResult:
    """Determine the AI suitability for a given business requirement.

    Args:
        requirement: The requirement schema containing all relevant attributes.

    Returns:
        A DecisionResult with the recommended category and full explanation.
    """
    # Collect influencing rules
    influencing_rules: List[DecisionRule] = []

    # Rule R11: Domain knowledge consideration
    if requirement.domain:
        influencing_rules.append(DecisionRule.RULE_11_DOMAIN_KNOWLEDGE)

    # Step 1: Check if fixed rules can solve the task adequately (R1, R5)
    if requirement.fixed_rules_possible:
        influencing_rules.append(DecisionRule.RULE_1_FIXED_RULES_PREFERRED)
        influencing_rules.append(DecisionRule.RULE_5_RULES_VS_ML)
        return DecisionResult(
            decision=DecisionCategory.NO_AI,
            reasons=[
                "Fixed rules can adequately solve this task.",
                "Traditional programming approach is more reliable, maintainable, and cost-effective.",
                "No AI necessary when business rules are well-defined and deterministic.",
            ],
            evidence=DecisionEvidence(
                rule_ids=[DecisionRule.RULE_1_FIXED_RULES_PREFERRED, DecisionRule.RULE_5_RULES_VS_ML],
                text_support=[
                    "Requirement indicates fixed rules are possible.",
                    "Business problem has deterministic solution space.",
                ],
            ),
            alternative_approach="Traditional rule-based implementation with explicit business logic.",
            risks=[
                "Rule set may become complex over time and require refactoring.",
                "Fixed rules cannot adapt to changing business conditions without updates.",
            ],
            data_requirements=[],
            first_next_step="Document business rules and implement traditional software solution.",
            responsible_roles=["Backend Engineer", "Product Owner"],
            lifecycle=["Not applicable - traditional software development"],
            decision_id=f"dec-{requirement.id}" if requirement.id else "decision-generic",
        )

    # Step 2: Check for unavailable training data (R2)
    if not requirement.data_available:
        influencing_rules.append(DecisionRule.RULE_2_NO_TRAINING_DATA)
        return DecisionResult(
            decision=DecisionCategory.NO_AI,
            reasons=[
                "Insufficient training data for machine learning approach.",
                "AI models require substantial labelled data to achieve reliable performance.",
                "Recommend data collection strategy or baseline traditional approach.",
            ],
            evidence=DecisionEvidence(
                rule_ids=[DecisionRule.RULE_2_NO_TRAINING_DATA],
                text_support=[
                    "Requirement indicates data is not available.",
                    "Without data, ML model training would be unreliable or impossible.",
                ],
            ),
            alternative_approach="Implement data collection plan first, or use traditional programming with manual processes.",
            risks=[
                "Delayed implementation while data is collected.",
                "Model performance uncertainty if limited data is available.",
            ],
            data_requirements=[
                "Collect and label minimum viable dataset before model development.",
                "Establish data pipeline for ongoing model updates.",
            ],
            first_next_step="Initiate data collection and assessment program.",
            responsible_roles=["Data Engineer", "Data Scientist"],
            lifecycle=[
                "Problem Framing",
                "Data Collection and Preparation",
                "Model Development",
                "Deployment",
                "Monitoring and Improvement",
            ],
            decision_id=f"dec-{requirement.id}" if requirement.id else "decision-generic",
        )

    # Step 3: Check for content generation requirements (R10)
    if requirement.requires_content_generation:
        influencing_rules.append(DecisionRule.RULE_10_GENERATIVE_AI_CONTENT)
        return DecisionResult(
            decision=DecisionCategory.GENERATIVE_AI,
            reasons=[
                "Requirement involves content generation, summarisation, or language generation.",
                "Generative AI is the appropriate technology for text generation tasks.",
                "LLM-based architecture suitable for semantic question answering.",
            ],
            evidence=DecisionEvidence(
                rule_ids=[DecisionRule.RULE_10_GENERATIVE_AI_CONTENT],
                text_support=[
                    "Requirement specifies content generation is needed.",
                    "Generative AI models excel at text generation and summarisation.",
                ],
            ),
            alternative_approach="Template-based content generation or rule-based approaches for simple cases.",
            risks=[
                "Generated content may contain errors or hallucinations.",
                "Requires careful prompt engineering and output validation.",
                "Computational costs may be higher than traditional approaches.",
            ],
            data_requirements=[
                "Content corpus or source material for grounding/attribution.",
                "Evaluation framework for output quality.",
            ],
            first_next_step="Design LLM prompt architecture and prepare content source material.",
            responsible_roles=["AI Engineer", "ML Engineer"],
            lifecycle=[
                "Problem Framing",
                "Data Collection and Preparation",
                "Model Development",
                "Deployment",
                "Monitoring and Improvement",
            ],
            decision_id=f"dec-{requirement.id}" if requirement.id else "decision-generic",
        )

    # Step 4: Check for complex high-dimensional perception (R9) - Deep Learning
    # Rule R3: Unstructured input does NOT automatically mean Deep Learning
    # Distinguish between perception tasks (images, audio) and text classification
    domain_lower = requirement.domain.lower() if requirement.domain else ""
    has_perception_input = (
        requirement.unstructured_input
        and not requirement.requires_content_generation
        and requirement.domain
        and domain_lower in [
            "manufacturing", "healthcare", "media", "entertainment",
            "automotive", "surveillance",
        ]
    )
    is_text_classification = (
        requirement.unstructured_input
        and not requirement.requires_content_generation
        and requirement.domain
        and domain_lower in [
            "customer success", "marketing", "hr", "finance", "ecommerce",
        ]
    )

    if has_perception_input:
        influencing_rules.append(DecisionRule.RULE_3_NO_AI_AUTOMATIC)
        influencing_rules.append(DecisionRule.RULE_9_DEEP_LEARNING_PERCEPTION)
        return DecisionResult(
            decision=DecisionCategory.DEEP_LEARNING,
            reasons=[
                "Requirement involves unstructured input (images, audio, etc.) that requires",
                "high-dimensional perception typically handled by deep learning models.",
                "However, note that unstructured input does NOT automatically mean Deep Learning "
                "(see Rule R3).",
            ],
            evidence=DecisionEvidence(
                rule_ids=[DecisionRule.RULE_3_NO_AI_AUTOMATIC, DecisionRule.RULE_9_DEEP_LEARNING_PERCEPTION],
                text_support=[
                    "Requirement has unstructured input component.",
                    "Task involves perception of complex data modalities.",
                ],
            ),
            alternative_approach="Classical ML with feature engineering may suffice for simpler unstructured tasks.",
            risks=[
                "Deep learning requires significant data and compute resources.",
                "Model interpretability is limited compared to classical ML.",
                "Overkill for simpler unstructured tasks.",
            ],
            data_requirements=[
                "Labeled dataset representative of the input domain.",
                "Compute resources for model training.",
            ],
            first_next_step="Data collection and preprocessing for deep learning pipeline.",
            responsible_roles=["Deep Learning Engineer", "ML Engineer"],
            lifecycle=[
                "Problem Framing",
                "Data Collection and Preparation",
                "Model Development",
                "Deployment",
                "Monitoring and Improvement",
            ],
            decision_id=f"dec-{requirement.id}" if requirement.id else "decision-generic",
        )

    if is_text_classification and not requirement.requires_content_generation:
        # Text classification tasks go to Classical ML, not Deep Learning
        influencing_rules.append(DecisionRule.RULE_8_CLASSICAL_ML_PREDICTION)
        return DecisionResult(
            decision=DecisionCategory.CLASSICAL_ML,
            reasons=[
                "Requirement involves text classification or sentiment analysis.",
                "Classical machine learning algorithms (e.g., Logistic Regression, Naive Bayes,"
                " SVMs) are well-suited for labelled text classification tasks.",
                "Rule R3: Unstructured input does NOT automatically mean Deep Learning.",
            ],
            evidence=DecisionEvidence(
                rule_ids=[DecisionRule.RULE_8_CLASSICAL_ML_PREDICTION],
                text_support=[
                    "Requirement has unstructured text input component.",
                    "Task involves text classification rather than content generation or perception.",
                ],
            ),
            alternative_approach="Deep learning (e.g., transformers) if data volume is very large,"
            " or rule-based approach for simple categorization.",
            risks=[
                "May not capture complex semantic patterns compared to large language models.",
                "Feature engineering required for optimal text representation.",
                "Limited context window compared to transformer-based models.",
            ],
            data_requirements=[
                "Labelled training dataset with text and sentiment/class labels.",
                "Text preprocessing pipeline (tokenization, cleaning).",
            ],
            first_next_step="Prepare labelled dataset and train classical ML classification model.",
            responsible_roles=["Data Scientist", "ML Engineer"],
            lifecycle=[
                "Problem Framing",
                "Data Collection and Preparation",
                "Model Development",
                "Deployment",
                "Monitoring and Improvement",
            ],
            decision_id=f"dec-{requirement.id}" if requirement.id else "decision-generic",
        )

    # Step 4 Fallback: Deep Learning for unstructured perception tasks
    # (only reached if neither has_perception_input nor is_text_classification matched)
    if requirement.unstructured_input and not requirement.requires_content_generation:
        influencing_rules.append(DecisionRule.RULE_9_DEEP_LEARNING_PERCEPTION)
        return DecisionResult(
            decision=DecisionCategory.DEEP_LEARNING,
            reasons=[
                "Requirement involves unstructured input that requires deep learning",
                "for perception or complex pattern recognition.",
            ],
            evidence=DecisionEvidence(
                rule_ids=[DecisionRule.RULE_9_DEEP_LEARNING_PERCEPTION],
                text_support=[
                    "Requirement has unstructured input component.",
                ],
            ),
            alternative_approach="Classical ML with feature engineering may suffice for simpler tasks.",
            risks=[
                "Deep learning requires significant data and compute resources.",
                "Model interpretability is limited.",
            ],
            data_requirements=[
                "Labeled dataset representative of the input domain.",
                "Compute resources for model training.",
            ],
            first_next_step="Data collection and preprocessing for deep learning pipeline.",
            responsible_roles=["Deep Learning Engineer", "ML Engineer"],
            lifecycle=[
                "Problem Framing",
                "Data Collection and Preparation",
                "Model Development",
                "Deployment",
                "Monitoring and Improvement",
            ],
            decision_id=f"dec-{requirement.id}" if requirement.id else "decision-generic",
        )

    # Step 5: Check for descriptive reporting and statistical trends (R7)
    # Rule R7: Descriptive reporting and statistical trend analysis → Analytics/BI
    # Exclude classification/prediction tasks (e.g., fraud detection, customer classification)
    # These should be Classical ML per Rule R8
    # Distinguish based on task type: forecasting/trend analysis vs. entity classification
    task_involves_classification = any(
        keyword in requirement.title.lower()
        for keyword in ["detect", "classify", "identify", "fraud", "anomaly"]
    )
    task_involves_forecasting = any(
        keyword in requirement.title.lower()
        for keyword in ["forecast", "predict", "demand", "trend", "weekly", "monthly"]
    )
    is_descriptive_reporting = (
        domain_lower in ["finance", "sales", "operations", "business"]
        and not requirement.requires_content_generation
        and (not requirement.needs_learning_from_data or task_involves_forecasting)
        and not task_involves_classification
    )
    if is_descriptive_reporting:
        influencing_rules.append(DecisionRule.RULE_7_ANALYTICS_BI)
        return DecisionResult(
            decision=DecisionCategory.ANALYTICS_BI,
            reasons=[
                "Requirement involves descriptive reporting, statistical trend analysis,",
                "or business intelligence for finance/sales/operations domains.",
                "Analytics/BI tools can provide these insights without ML.",
            ],
            evidence=DecisionEvidence(
                rule_ids=[DecisionRule.RULE_7_ANALYTICS_BI],
                text_support=[
                    "Domain suggests business intelligence or reporting needs.",
                    "Task involves trend analysis and descriptive statistics.",
                ],
            ),
            alternative_approach="Business intelligence dashboards, reporting tools, or spreadsheet-based analysis.",
            risks=[
                "Limited predictive capability compared to ML models.",
                "May not detect complex non-linear patterns.",
            ],
            data_requirements=[
                "Historical data for trend analysis and reporting.",
                "Analytics platform or BI tool implementation.",
            ],
            first_next_step="Implement BI dashboard or reporting pipeline with historical data.",
            responsible_roles=["Data Engineer", "Business Analyst"],
            lifecycle=[
                "Problem Framing",
                "Data Collection and Preparation",
                "Model Development (descriptive models)",
                "Deployment",
                "Monitoring and Improvement",
            ],
            decision_id=f"dec-{requirement.id}" if requirement.id else "decision-generic",
        )

    # Step 6: Check for structured-data prediction and classification (R8) - Classical ML
    influencing_rules.append(DecisionRule.RULE_8_CLASSICAL_ML_PREDICTION)
    return DecisionResult(
        decision=DecisionCategory.CLASSICAL_ML,
        reasons=[
            "Requirement involves structured-data prediction or classification.",
            "Classical machine learning algorithms are well-suited for these tasks.",
            "When labelled data is available, classical ML provides reliable, interpretable results.",
        ],
        evidence=DecisionEvidence(
            rule_ids=[DecisionRule.RULE_8_CLASSICAL_ML_PREDICTION],
            text_support=[
                "Task fits structured prediction/classification pattern.",
                "Available data supports supervised learning approach.",
            ],
        ),
        alternative_approach="Deep learning if data volume is very large, or rule-based approach for simple cases.",
        risks=[
            "May not capture complex patterns in very high-dimensional data.",
            "Feature engineering required for optimal performance.",
            "Model may overfit if training data is limited.",
        ],
        data_requirements=[
            "Labelled training dataset with features and targets.",
            "Feature engineering and validation split.",
        ],
        first_next_step="Prepare labelled dataset and train classical ML model.",
        responsible_roles=["Data Scientist", "ML Engineer"],
        lifecycle=[
            "Problem Framing",
            "Data Collection and Preparation",
            "Model Development",
            "Deployment",
            "Monitoring and Improvement",
        ],
        decision_id=f"dec-{requirement.id}" if requirement.id else "decision-generic",
    )


def validate_requirement_schema(requirement: RequirementSchema) -> bool:
    """Validate that a requirement schema has valid attributes.

    Args:
        requirement: The requirement schema to validate.

    Returns:
        True if the requirement is valid, False otherwise.
    """
    # Check that at least the core attributes are present
    core_attrs = [
        "title", "description", "fixed_rules_possible",
        "needs_learning_from_data", "unstructured_input",
        "requires_content_generation", "data_available", "domain",
    ]
    for attr in core_attrs:
        if not hasattr(requirement, attr):
            return False
    return True