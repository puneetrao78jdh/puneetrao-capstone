"""Typed configuration + run summary — Pydantic v2 models.

Two models with different roles:
  - Settings:    config (same every run; loaded at module init)
  - RunSummary:  observation (one row per execution; produced at run end)
"""
from __future__ import annotations
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load local .env in developer environments (VS Code on your laptop).
# Vocareum usually sets OPENAI_API_KEY in the environment directly, so this is
# harmless there as well.
load_dotenv()


class Settings(BaseSettings):
    """Runtime configuration. Validated at construction."""
    model_config = SettingsConfigDict(
      env_file=".env",
      env_file_encoding="utf-8"
    )
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    questions_csv: Path  = Path("data/questions.csv")
    results_json:  Path  = Path("results.json")
    results_db:    Path  = Path("results.db")
    batch_size:    int   = Field(5,   gt=0, le=20)
    fail_rate:     float = Field(0.0, ge=0.0, le=1.0)
    max_retries: int = Field(2, ge=0)
    retry_delay_s: float = Field(1.0, ge=0.0)
    model:         str   = "gpt-4o-mini"
    use_fake:      bool  = False


class RunSummary(BaseModel):
    """One row per pipeline execution. Persisted to the `runs` table."""

    started_at:       float
    elapsed_seconds:  float = Field(ge=0.0)
    n_questions:      int   = Field(ge=0)
    n_succeeded:      int   = Field(ge=0)
    n_retries_total:  int   = Field(ge=0)
    total_cost_usd:   float = Field(ge=0.0)
    fail_rate:        float = Field(ge=0.0, le=1.0)
    use_fake:         bool
