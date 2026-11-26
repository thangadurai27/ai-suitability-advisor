"""SQLAlchemy models for AI Suitability Advisor.

Defines database tables for users, requirements, and analyses.
All models use UUID identifiers where appropriate and support
user ownership tracking for multi-tenant data isolation."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4, UUID

from sqlalchemy import (
    String,
    Text,
    DateTime,
    Integer,
    Boolean,
    Index,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


class User(Base):
    """User model for authentication and ownership tracking."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    requirements = relationship("Requirement", back_populates="owner", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="owner", cascade="all, delete-orphan")


class Requirement(Base):
    """Requirement model representing a business requirement.

    Stores the attributes of a business problem for AI suitability assessment."""

    __tablename__ = "requirements"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    fixed_rules_possible: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    needs_learning_from_data: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    unstructured_input: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    requires_content_generation: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    data_available: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    domain: Mapped[str] = mapped_column(String(100), nullable=False)
    additional_context: Mapped[str] = mapped_column(Text, nullable=True)
    owner_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=True
    )  # NULL for demo/anonymous access
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    owner = relationship("User", back_populates="requirements")
    analyses = relationship("Analysis", back_populates="requirement", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_requirements_owner_id", "owner_id"),
        Index("ix_requirements_domain", "domain"),
    )


class Analysis(Base):
    """Analysis model representing a completed AI suitability analysis.

    Stores the results of the decision engine evaluation including
    the recommended category, reasons, risks, and lifecycle information."""

    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    requirement_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("requirements.id"), nullable=False
    )  # Links to requirement or raw text
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    decision_category: Mapped[str] = mapped_column(String(50), nullable=False)
    reasons: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_rule_ids: Mapped[str] = mapped_column(
        Text, nullable=True
    )  # JSON-serialized list of rule IDs
    alternative_approach: Mapped[str] = mapped_column(Text, nullable=True)
    risks: Mapped[str] = mapped_column(Text, nullable=True)
    data_requirements: Mapped[str] = mapped_column(Text, nullable=True)
    first_next_step: Mapped[str] = mapped_column(Text, nullable=True)
    lifecycle: Mapped[str] = mapped_column(Text, nullable=True)
    responsible_roles: Mapped[str] = mapped_column(
        Text, nullable=True
    )  # JSON-serialized list of roles
    owner_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=True
    )  # NULL for demo/anonymous access

    # Relationships
    owner = relationship("User", back_populates="analyses")
    requirement = relationship("Requirement", back_populates="analyses")

    __table_args__ = (
        Index("ix_analyses_owner_id", "owner_id"),
        Index("ix_analyses_decision_category", "decision_category"),
        Index("ix_analyses_created_at", "created_at"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )