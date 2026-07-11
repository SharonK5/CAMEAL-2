"""
config/settings.py

Global configuration for the CAMEAL Framework.

Context-Aware Adaptation, Monitoring,
Evaluation, Accountability and Learning (CAMEAL)

Author: Sharon Rhodah Kaitano
"""

from pathlib import Path
import os
from dataclasses import dataclass, field

# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"
LOG_DIR = PROJECT_ROOT / "logs"
REPORT_DIR = PROJECT_ROOT / "reports"
CACHE_DIR = PROJECT_ROOT / "cache"
TEMP_DIR = PROJECT_ROOT / "temp"

DOCUMENTS_DIR = DATA_DIR / "documents"
VECTOR_DB_DIR = DATA_DIR / "vector_store"
GRAPH_DB_DIR = DATA_DIR / "knowledge_graph"

# Create directories automatically
for directory in [
    DATA_DIR,
    MODEL_DIR,
    LOG_DIR,
    REPORT_DIR,
    CACHE_DIR,
    TEMP_DIR,
    DOCUMENTS_DIR,
    VECTOR_DB_DIR,
    GRAPH_DB_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)


# ==========================================================
# SYSTEM CONFIGURATION
# ==========================================================

@dataclass
class SystemConfig:

    system_name: str = "CAMEAL"

    version: str = "0.1.0"

    mode: str = os.getenv("CAMEAL_MODE", "offline")
    # offline | online | hybrid

    environment: str = os.getenv("CAMEAL_ENV", "development")

    debug: bool = True

    timezone: str = "Africa/Nairobi"

    language: str = "en"

    max_workers: int = 4


# ==========================================================
# GOVERNANCE CONFIGURATION
# ==========================================================

@dataclass
class GovernanceConfig:

    monitoring_enabled: bool = True

    evaluation_enabled: bool = True

    accountability_enabled: bool = True

    adaptation_enabled: bool = True

    learning_enabled: bool = True

    human_review_required: bool = True

    confidence_threshold: float = 0.75

    evidence_threshold: float = 0.80


# ==========================================================
# REPOSITORY CONFIGURATION
# ==========================================================

@dataclass
class RepositoryConfig:

    chunk_size: int = 500

    chunk_overlap: int = 100

    max_results: int = 10

    semantic_search: bool = True

    keyword_search: bool = True


# ==========================================================
# MACHINE LEARNING
# ==========================================================

@dataclass
class MLConfig:

    random_seed: int = 42

    train_test_split: float = 0.2

    retrain_threshold: float = 0.85

    enable_prediction_logging: bool = True


# ==========================================================
# AI CONFIGURATION
# ==========================================================

@dataclass
class AIConfig:

    provider: str = os.getenv("LLM_PROVIDER", "ollama")

    model: str = os.getenv("LLM_MODEL", "llama3.2")

    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "mxbai-embed-large"
    )

    temperature: float = 0.2

    max_tokens: int = 2048

    enable_external_sources: bool = True


# ==========================================================
# CLIMATE CONFIGURATION
# ==========================================================

@dataclass
class ClimateConfig:

    default_country: str = "Kenya"

    enable_satellite_data: bool = True

    enable_weather_data: bool = True

    update_interval_hours: int = 24


# ==========================================================
# SECURITY CONFIGURATION
# ==========================================================

@dataclass
class SecurityConfig:

    encryption_enabled: bool = True

    audit_logging: bool = True

    anonymize_sensitive_data: bool = True


# ==========================================================
# APPLICATION SETTINGS
# ==========================================================

@dataclass
class Settings:

    system: SystemConfig = field(default_factory=SystemConfig)

    governance: GovernanceConfig = field(default_factory=GovernanceConfig)

    repository: RepositoryConfig = field(default_factory=RepositoryConfig)

    ml: MLConfig = field(default_factory=MLConfig)

    ai: AIConfig = field(default_factory=AIConfig)

    climate: ClimateConfig = field(default_factory=ClimateConfig)

    security: SecurityConfig = field(default_factory=SecurityConfig)


settings = Settings()
