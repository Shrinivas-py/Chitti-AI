from core.gemini_client import call_gemini
from config import settings


def get_agent_count(problem: str) -> int:
    """
    Uses SMALL Gemini model to decide number of agents dynamically.
    """

    prompt = f"""
You are optimizing a multi-agent AI system.

Problem:
{problem}

Decide how many agents (between 2 and 20) should work on this.

Rules:
- Simple problem → fewer agents
- Complex problem → more agents
- Return ONLY a number (no text)

Answer:
"""

    try:
        result = call_gemini(prompt, settings.SMALL_MODEL)

        # Clean result
        result = result.strip()

        # Extract number safely
        number = int(''.join(filter(str.isdigit, result)))

        # Clamp range
        if number < 2:
            return 2
        if number > 20:
            return 20

        return number

    except Exception as e:
        print("Agent count fallback:", e)
        return 5