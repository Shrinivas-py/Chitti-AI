# config.py
# ─────────────────────────────────────────────────────────────────────────────
# Central settings for the Swarm Engine.
# All values can be overridden via environment variables or the .env file.
# ─────────────────────────────────────────────────────────────────────────────
import os
import sys
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # ── API Keys ──────────────────────────────────────────────────────────────
    GROQ_API_KEY: str   = os.getenv("GROQ_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # ── Models ────────────────────────────────────────────────────────────────
    # Both models use llama-3.1-8b-instant:
    #   - llama-3.3-70b-versatile has only 100k tokens/day on free tier
    #   - llama-3.1-8b-instant has 500k requests/day — much more headroom
    AGENT_MODEL: str   = "llama-3.1-8b-instant"
    SCORING_MODEL: str = "llama-3.1-8b-instant"

    # ── Swarm run defaults ────────────────────────────────────────────────────
    # 10 micro-agents = 10 virtualized copies of the model, each with a
    # distinct personality, running across 5 evolving iterations.
    SWARM_NUM_AGENTS: int     = 10
    SWARM_NUM_ITERATIONS: int = 5
    # Batch size reduced to 3 (from 5) to stay within Groq free-tier rate
    # limits. If you have a paid key, bump this back up to 5.
    SWARM_BATCH_SIZE: int     = 3

    # ── Temperature range ─────────────────────────────────────────────────────
    TEMPERATURE_MIN: float      = 0.10
    TEMPERATURE_MAX: float      = 1.00
    TEMPERATURE_SCORING: float  = 0.10
    TEMPERATURE_SYNTHESIS: float = 0.50

    # ── Token limits ──────────────────────────────────────────────────────────
    MAX_TOKENS_AGENT: int     = 200
    MAX_TOKENS_SCORING: int   = 80    # just needs a JSON array like [7.2, 8.5, 6.1]
    MAX_TOKENS_SYNTHESIS: int = 800

    # ── Memory / context ─────────────────────────────────────────────────────
    PRIOR_IDEAS_CONTEXT_WINDOW: int = 10
    TOP_IDEAS_TO_KEEP: int          = 5

    # ── Evolution ─────────────────────────────────────────────────────────────
    PRUNE_RATE: float = 0.30


settings = Settings()

# ── Startup guard: warn loudly if GROQ_API_KEY is missing ────────────────────
if not settings.GROQ_API_KEY:
    print(
        "\n[CONFIG] WARNING: GROQ_API_KEY is not set or is empty.\n"
        "         The swarm will fail to call the LLM and will fall back to\n"
        "         dummy output. Set GROQ_API_KEY in your .env file and retry.\n",
        file=sys.stderr,
    )