# tests/test_config.py
# ─────────────────────────────────────────────────────────────────────────────
# TEST 1: Configuration loads correctly.
# Run this first — if config fails, everything else will fail too.
# ─────────────────────────────────────────────────────────────────────────────
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_settings_load():
    """Settings must load without errors and have required fields."""
    from config import settings
    assert settings.GROQ_API_KEY, "GROQ_API_KEY is missing. Add it to your .env file."
    assert settings.AGENT_MODEL, "AGENT_MODEL not set"
    assert 2 <= settings.SWARM_NUM_AGENTS <= 50
    assert 1 <= settings.SWARM_NUM_ITERATIONS <= 10
    assert 1 <= settings.SWARM_BATCH_SIZE <= 10
    assert 0.0 <= settings.PRUNE_RATE <= 0.6
    assert settings.TEMPERATURE_MIN < settings.TEMPERATURE_MAX
    print(f"  PASS | model={settings.AGENT_MODEL} | agents={settings.SWARM_NUM_AGENTS}")


def test_temperature_range_sensible():
    """Temperature bounds must produce valid Groq temperatures."""
    from config import settings
    assert settings.TEMPERATURE_MIN >= 0.0
    assert settings.TEMPERATURE_MAX <= 1.0
    assert settings.TEMPERATURE_SCORING < settings.TEMPERATURE_MIN
    print(f"  PASS | temp range=[{settings.TEMPERATURE_MIN}, {settings.TEMPERATURE_MAX}]")