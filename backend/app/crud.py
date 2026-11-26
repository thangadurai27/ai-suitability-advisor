"""CRUD operations for AI Suitability Advisor database models.

Provides create, read, update, and delete operations for users,
requirements, and analyses. All operations support both authenticated
user contexts and anonymous/demo mode."""

from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional, Dict, Any
from uuid import uuid4

from .models import User, Requirement, Analysis


# ===== User CRUD =====

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email address.
    
    Args:
        db: Database session.
        email: Email address to search for.
        
    Returns:
        User instance if found, None otherwise.
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, hashed_password: str) -> User:
    """Create a new user.
    
    Args:
        db: Database session.
        email: User email address.
        hashed_password: Hashed password for the user.
        
    Returns:
        Created User instance.
    """
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ===== Requirement CRUD =====

def get_requirement(db: Session, requirement_id: str) -> Optional[Requirement]:
    """Get a requirement by ID.
    
    Args:
        db: Database session.
        requirement_id: Requirement UUID string.
        
    Returns:
        Requirement instance if found, None otherwise.
    """
    return db.query(Requirement).filter(Requirement.id == requirement_id).first()


def get_requirements(
    db: Session,
    owner_id: Optional[str] = None,
    domain: Optional[str] = None,
) -> List[Requirement]:
    """List requirements with optional filtering.
    
    Args:
        db: Database session.
        owner_id: Filter by owner (None for demo/anonymous data).
        domain: Filter by domain.
        
    Returns:
        List of Requirement instances.
    """
    query = db.query(Requirement)
    
    if owner_id is not None:
        query = query.filter(Requirement.owner_id == owner_id)
    if domain is not None:
        query = query.filter(Requirement.domain == domain)
    
    return query.order_by(Requirement.created_at.desc()).all()


def create_requirement(
    db: Session,
    title: str,
    description: str,
    fixed_rules_possible: bool,
    needs_learning_from_data: bool,
    unstructured_input: bool,
    requires_content_generation: bool,
    data_available: bool,
    domain: str,
    additional_context: str = "",
    owner_id: Optional[str] = None,
    requirement_id: Optional[str] = None,
) -> Requirement:
    """Create a new requirement.
    
    Args:
        db: Database session.
        title: Requirement title.
        description: Detailed business problem description.
        fixed_rules_possible: Whether fixed rules can solve the task.
        needs_learning_from_data: Whether the problem needs learning from data.
        unstructured_input: Whether the input is unstructured.
        requires_content_generation: Whether content generation is required.
        data_available: Whether relevant data is available.
        domain: Business domain.
        additional_context: Optional additional context.
        owner_id: User ID (None for demo/anonymous access).
        
    Returns:
        Created Requirement instance.
    """
    db_requirement = Requirement(
        id=requirement_id or str(uuid4()),
        title=title,
        description=description,
        fixed_rules_possible=fixed_rules_possible,
        needs_learning_from_data=needs_learning_from_data,
        unstructured_input=unstructured_input,
        requires_content_generation=requires_content_generation,
        data_available=data_available,
        domain=domain,
        additional_context=additional_context,
        owner_id=owner_id,
    )
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement


# ===== Analysis CRUD =====

def get_analysis(db: Session, analysis_id: str) -> Optional[Analysis]:
    """Get an analysis by ID.
    
    Args:
        db: Database session.
        analysis_id: Analysis UUID string.
        
    Returns:
        Analysis instance if found, None otherwise.
    """
    return db.query(Analysis).filter(Analysis.id == analysis_id).first()


def get_analyses(
    db: Session,
    owner_id: Optional[str] = None,
    decision_category: Optional[str] = None,
) -> List[Analysis]:
    """List analyses with optional filtering.
    
    Args:
        db: Database session.
        owner_id: Filter by owner (None for demo/anonymous data).
        decision_category: Filter by decision category.
        
    Returns:
        List of Analysis instances.
    """
    query = db.query(Analysis)
    
    if owner_id is not None:
        query = query.filter(Analysis.owner_id == owner_id)
    if decision_category is not None:
        query = query.filter(Analysis.decision_category == decision_category)
    
    return query.order_by(Analysis.created_at.desc()).all()


def create_analysis(
    db: Session,
    requirement_id: str,
    title: str,
    decision_category: str,
    reasons: List[str],
    evidence_rule_ids: List[str],
    alternative_approach: str,
    risks: List[str],
    data_requirements: List[str],
    first_next_step: str,
    lifecycle: List[str],
    responsible_roles: List[str],
    owner_id: Optional[str] = None,
) -> Analysis:
    """Create a new analysis record.
    
    Args:
        db: Database session.
        requirement_id: Linked requirement ID (or empty for stand-alone analysis).
        title: Analysis title/requirement title.
        decision_category: Decision category from decision engine.
        reasons: List of reason strings.
        evidence_rule_ids: List of decision rule IDs that influenced the result.
        alternative_approach: Description of alternative approach.
        risks: List of risk strings.
        data_requirements: List of data requirement strings.
        first_next_step: First recommended next step.
        lifecycle: List of lifecycle stage strings.
        responsible_roles: List of responsible role strings.
        owner_id: User ID (None for demo/anonymous access).
        
    Returns:
        Created Analysis instance.
    """
    # Serialize lists to JSON strings for storage
    import json
    
    db_analysis = Analysis(
        requirement_id=requirement_id,
        title=title,
        decision_category=decision_category,
        reasons=json.dumps(reasons) if isinstance(reasons, list) else reasons,
        evidence_rule_ids=json.dumps(evidence_rule_ids) if isinstance(evidence_rule_ids, list) else str(evidence_rule_ids),
        alternative_approach=alternative_approach,
        risks=json.dumps(risks) if isinstance(risks, list) else risks,
        data_requirements=json.dumps(data_requirements) if isinstance(data_requirements, list) else data_requirements,
        first_next_step=first_next_step,
        lifecycle=json.dumps(lifecycle) if isinstance(lifecycle, list) else lifecycle,
        responsible_roles=json.dumps(responsible_roles) if isinstance(responsible_roles, list) else str(responsible_roles),
        owner_id=owner_id,
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis


def delete_analysis(db: Session, analysis_id: str) -> bool:
    """Delete an analysis by ID.
    
    Args:
        db: Database session.
        analysis_id: Analysis UUID string.
        
    Returns:
        True if deleted successfully, False if not found.
    """
    db_analysis = get_analysis(db, analysis_id)
    if db_analysis:
        db.delete(db_analysis)
        db.commit()
        return True
    return False


def get_analysis_counts_by_category(
    db: Session,
    owner_id: Optional[str] = None,
) -> Dict[str, int]:
    """Get count of analyses grouped by decision category.
    
    Args:
        db: Database session.
        owner_id: Filter by owner (None for all data).
        
    Returns:
        Dictionary mapping decision category to count.
    """
    from sqlalchemy import func
    
    query = db.query(
        Analysis.decision_category, func.count(Analysis.id)
    )
    
    if owner_id is not None:
        query = query.filter(Analysis.owner_id == owner_id)
    
    query = query.group_by(Analysis.decision_category)
    
    result = {row[0]: row[1] for row in query.all()}
    return result


def export_csv_report(db: Session, owner_id: Optional[str] = None) -> str:
    """Export all analyses as CSV report.
    
    Args:
        db: Database session.
        owner_id: Filter by owner (None for all data).
        
    Returns:
        CSV formatted string containing all analysis data.
    """
    import json
    import csv
    import io
    
    from .crud import get_analyses
    
    analyses = get_analyses(db, owner_id=owner_id)
    
    # Build CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header row
    writer.writerow([
        "ID", "Title", "Decision Category", "Reasons",
        "Evidence Rule IDs", "Alternative Approach", "Risks",
        "Data Requirements", "First Next Step", "Lifecycle",
        "Responsible Roles", "Created At"
    ])
    
    # Data rows
    for analysis in analyses:
        writer.writerow([
            analysis.id or "",
            analysis.title or "",
            analysis.decision_category or "",
            analysis.reasons or "",
            analysis.evidence_rule_ids or "",
            analysis.alternative_approach or "",
            analysis.risks or "",
            analysis.data_requirements or "",
            analysis.first_next_step or "",
            analysis.lifecycle or "",
            analysis.responsible_roles or "",
            analysis.created_at.isoformat() if analysis.created_at else "",
        ])
    
    csv_string = output.getvalue()
    return csv_string