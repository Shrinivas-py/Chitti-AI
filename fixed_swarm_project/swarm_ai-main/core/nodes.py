from __future__ import annotations
import asyncio
import json
import re

from core.state import SwarmState
from agents.factory import AgentFactory
from memory.memory import SwarmMemory
from config import settings

# ✅ Gemini instead of Groq
from core.gemini_client import call_gemini


# ─────────────────────────────────────────────────────────────
# NODE 1 — initialize
# ─────────────────────────────────────────────────────────────
def initialize_node(state: SwarmState) -> dict:
    print(f"\n{'='*60}")
    print("SWARM ENGINE — INITIALIZE")
    print(f"{'='*60}")

    problem     = state["problem"]
    num_agents  = state["num_agents"]
    max_iter    = state["max_iterations"]
    batch_size  = state["batch_size"]

    memory = SwarmMemory()
    memory.initialize(problem)

    factory = AgentFactory(num_agents=num_agents)
    factory.initialize()

    print(f"\nConfig | agents={num_agents} | iterations={max_iter} | batch={batch_size}")
    print(f"{'='*60}\n")

    return {
        "memory": memory,
        "factory": factory,
        "current_iteration": 0,
        "final_output": None,
        "error": None,
    }


# ─────────────────────────────────────────────────────────────
# NODE 2 — generate (UNCHANGED)
# ─────────────────────────────────────────────────────────────
async def generate_node(state: SwarmState) -> dict:
    memory: SwarmMemory   = state["memory"]
    factory: AgentFactory = state["factory"]
    batch_size: int       = state["batch_size"]

    iteration = memory.advance_iteration()

    active_agents = factory.get_active_agents()
    prior_ideas   = memory.get_context_for_agents()

    batches = [
        active_agents[i: i + batch_size]
        for i in range(0, len(active_agents), batch_size)
    ]

    for batch in batches:
        tasks = [
            _invoke_agent(agent, memory.problem, iteration, prior_ideas)
            for agent in batch
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for agent, result in zip(batch, results):
            if isinstance(result, Exception):
                print(f"[{agent.label()}] FAILED: {result}")
            elif result:
                memory.add_idea(
                    text=result,
                    agent_id=agent.id,
                    agent_style=agent.style,
                )

    return {"memory": memory, "current_iteration": iteration}


async def _invoke_agent(agent, problem: str, iteration: int, prior_ideas: list[dict]) -> str | None:
    chain      = agent.build_chain()
    input_data = agent.build_invoke_input(problem, iteration, prior_ideas)

    result = await chain.ainvoke(input_data)
    return result.strip() if result else None


# ─────────────────────────────────────────────────────────────
# NODE 3 — score (GEMINI)
# ─────────────────────────────────────────────────────────────
async def score_node(state: SwarmState) -> dict:
    memory: SwarmMemory   = state["memory"]
    factory: AgentFactory = state["factory"]
    iteration: int        = state["current_iteration"]

    iter_ideas = memory.get_ideas_for_iteration(iteration)
    if not iter_ideas:
        return {}

    ideas_numbered = "\n".join(
        f"{i + 1}. {idea.text}"
        for i, idea in enumerate(iter_ideas)
    )

    scoring_prompt = f"""
Score each idea from 1 to 10.

Problem: {memory.problem}

Ideas:
{ideas_numbered}

Return ONLY JSON array like: [7.2, 8.5, 6.1]
"""

    try:
        raw = call_gemini(scoring_prompt, settings.BIG_MODEL)

        match = re.search(r"\[[\d\s.,]+\]", raw)
        scores = json.loads(match.group()) if match else [5.0]*len(iter_ideas)

        for i, idea in enumerate(iter_ideas):
            score = float(scores[i]) if i < len(scores) else 5.0
            memory.update_score(idea.idea_id, score)

            agent = factory.get_agent_by_id(idea.agent_id)
            if agent:
                agent.record_score(score)

    except Exception as e:
        print("Scoring fallback:", e)
        import random
        for idea in iter_ideas:
            memory.update_score(idea.idea_id, round(random.uniform(4,7),1))

    return {"memory": memory, "factory": factory}


# ─────────────────────────────────────────────────────────────
# NODE 4 — evolve (UNCHANGED)
# ─────────────────────────────────────────────────────────────
def evolve_node(state: SwarmState) -> dict:
    factory: AgentFactory = state["factory"]
    factory.evolve()
    return {"factory": factory}


# ─────────────────────────────────────────────────────────────
# NODE 5 — synthesize (GEMINI)
# ─────────────────────────────────────────────────────────────
async def synthesize_node(state: SwarmState) -> dict:
    memory: SwarmMemory = state["memory"]

    top_ideas = memory.get_top_ideas()
    if not top_ideas:
        return {"final_output": "No ideas generated."}

    ideas_text = "\n".join(
        f"{i+1}. {idea.text}"
        for i, idea in enumerate(top_ideas)
    )

    prompt = f"""
Problem: {memory.problem}

Top ideas:
{ideas_text}

Combine into one clean final answer.
"""

    try:
        final = call_gemini(prompt, settings.BIG_MODEL)
        return {"final_output": final}

    except Exception as e:
        return {"final_output": f"Failed: {e}"}


# ─────────────────────────────────────────────────────────────
# NODE 6 — error
# ─────────────────────────────────────────────────────────────
def error_node(state: SwarmState) -> dict:
    return {"final_output": f"Error: {state.get('error')}"}