from dotenv import load_dotenv
import os

load_dotenv()

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    All configuration for the swarm engine.
    """

    # ── API KEYS ─────────────────────────────────────────────
    GROQ_API_KEY: str = Field(...)
    GEMINI_API_KEY: str = Field(...)   # ✅ FIXED (inside class)

    # Optional
    TAVILY_API_KEY: str = ""

    # ── GEMINI MODELS ────────────────────────────────────────
    SMALL_MODEL: str = "gemini-2.5-flash-lite"
    BIG_MODEL: str = "gemini-2.5-pro"

    # ── LEGACY (can remove later if not using Groq)
    AGENT_MODEL: str = "llama-3.3-70b-versatile"
    SCORING_MODEL: str = "llama-3.3-70b-versatile"

    # ── SWARM PARAMETERS ────────────────────────────────────
    SWARM_NUM_AGENTS: int = Field(default=10, ge=2, le=50)
    SWARM_NUM_ITERATIONS: int = Field(default=3, ge=1, le=10)
    SWARM_BATCH_SIZE: int = Field(default=5, ge=1, le=10)
    PRUNE_RATE: float = Field(default=0.30, ge=0.0, le=0.6)
    TOP_IDEAS_TO_KEEP: int = Field(default=10, ge=3, le=30)
    PRIOR_IDEAS_CONTEXT_WINDOW: int = Field(default=8, ge=1, le=20)

    # ── TOKEN LIMITS ────────────────────────────────────────
    MAX_TOKENS_AGENT: int = 250
    MAX_TOKENS_SCORING: int = 512
    MAX_TOKENS_SYNTHESIS: int = 2048

    # ── TEMPERATURES ────────────────────────────────────────
    TEMPERATURE_MIN: float = 0.4
    TEMPERATURE_MAX: float = 1.0
    TEMPERATURE_SCORING: float = 0.1
    TEMPERATURE_SYNTHESIS: float = 0.3

    # 🔥 IMPORTANT
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )


# Shared instance
settings = Settings()