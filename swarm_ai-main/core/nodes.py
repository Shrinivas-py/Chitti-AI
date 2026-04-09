from __future__ import annotations
import asyncio
import json
import re
import time

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from core.state import SwarmState
from agents.factory import AgentFactory
from memory.memory import SwarmMemory
from config import settings


# ─────────────────────────────────────────────────────────────
# NODE 1 — initialize
# ─────────────────────────────────────────────────────────────
def initialize_node(state: SwarmState) -> dict:
    print(f"\n{'='*60}")
    print("SWARM ENGINE — INITIALIZE")
    print(f"{'='*60}")

    memory = SwarmMemory()
    memory.initialize(state["problem"])

    factory = AgentFactory(num_agents=state["num_agents"])
    factory.initialize()

    return {
        "memory": memory,
        "factory": factory,
        "current_iteration": 0,
        "final_output": None,
        "error": None,
    }


# ─────────────────────────────────────────────────────────────
# NODE 2 — generate
# ─────────────────────────────────────────────────────────────
async def generate_node(state: SwarmState) -> dict:
    memory: SwarmMemory = state["memory"]
    factory: AgentFactory = state["factory"]
    batch_size: int = state["batch_size"]

    iteration = memory.advance_iteration()

    agents = factory.get_active_agents()
    prior = memory.get_context_for_agents()

    batches = [agents[i:i+batch_size] for i in range(0, len(agents), batch_size)]

    for batch in batches:
        tasks = [
            _invoke_agent(agent, memory.problem, iteration, prior)
            for agent in batch
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for batch in batches:
            for agent in batch:
                try:
                    result = await _invoke_agent(agent, memory.problem, iteration, prior)
                    await asyncio.sleep(2)  # 🔥 VERY IMPORTANT DELAY

                except Exception as e:
                    if "rate_limit" in str(e):
                        print(f"[{agent.label()}] ⚠️ Rate limit hit. Waiting...")
                        await asyncio.sleep(6)
                        result = await _invoke_agent(agent, memory.problem, iteration, prior)
                    else:
                         print(f"[{agent.label()}] FAILED: {e}")
                         continue

                if not result:
                    continue

                content     = result.get("content", "").strip()
                action_type = result.get("action_type", "generate")
                reason      = result.get("reason", "")

                if not content:
                    continue

                # Compute parent_ids
                parent_ids = []
                
                scored = sorted(
                    [i for i in memory.get_all_ideas() if i.score > 0],
                    key=lambda x: x.score,
                    reverse=True,
                )

                if action_type == "refine" and scored:
                    parent_ids = [scored[0].idea_id]
                elif action_type == "combine" and len(scored) >= 2:
                    parent_ids = [scored[0].idea_id, scored[1].idea_id]

                memory.add_idea(
                    text=content,
                    agent_id=agent.id,
                    agent_style=agent.style,
                    action_type=action_type,
                    reason=reason,
                    parent_ids=parent_ids,
                )
    return {"memory": memory, "current_iteration": iteration}


async def _invoke_agent(agent, problem, iteration, prior):
    chain = agent.build_chain()
    data = agent.build_invoke_input(problem, iteration, prior)
    res = await chain.ainvoke(data)
    if not res:
        return None

    res = res.strip()

    # Try to extract structured JSON from the response
    try:
        # Strategy 1: direct parse if the whole response is JSON
        parsed = None
        stripped = res.strip()
        if stripped.startswith('{'):
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError:
                pass

        # Strategy 2: greedy match from first '{' to last '}' — handles
        # nested braces and markdown code fences like ```json { ... } ```
        if not parsed:
            first = stripped.find('{')
            last  = stripped.rfind('}')
            if first != -1 and last != -1 and last > first:
                try:
                    parsed = json.loads(stripped[first:last + 1])
                except json.JSONDecodeError:
                    pass

        if parsed and "content" in parsed:
            return {
                "content":     parsed["content"].strip(),
                "action_type": parsed.get("action_type", "generate"),
                "reason":      parsed.get("reason", ""),
            }
    except Exception:
        pass

    # Fallback: treat whole response as plain content
    return {
        "content":     res,
        "action_type": "generate" if iteration <= 1 else "refine",
        "reason":      "",
    }


# ─────────────────────────────────────────────────────────────
# NODE 3 — score (GROQ)
# ─────────────────────────────────────────────────────────────
async def score_node(state: SwarmState) -> dict:
    memory = state["memory"]
    factory = state["factory"]
    iteration = state["current_iteration"]

    ideas = memory.get_ideas_for_iteration(iteration)
    if not ideas:
        return {}

    ideas_text = "\n".join(
        f"{i+1}. {idea.text}"
        for i, idea in enumerate(ideas)
    )

    prompt = f"""
Score each idea from 1 to 10.

Problem: {memory.problem}

Ideas:
{ideas_text}

Return ONLY a JSON array like: [7.2, 8.5, 6.1]
No explanation. No text. Only the array.
"""

    llm = ChatGroq(
        model=settings.SCORING_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=settings.TEMPERATURE_SCORING,
        max_tokens=settings.MAX_TOKENS_SCORING,
    )

    scores = [5.0] * len(ideas)  # safe default
    for attempt in range(3):
        try:
            response = await llm.ainvoke([HumanMessage(content=prompt)])
            raw = response.content.strip()
            match = re.search(r"\[[\d\s.,]+\]", raw)
            if match:
                scores = json.loads(match.group())
            break
        except Exception as e:
            err = str(e)
            if "429" in err or "rate_limit" in err.lower():
                wait = 15 * (attempt + 1)
                print(f"[score_node] Rate-limited. Waiting {wait}s before retry {attempt+1}/3...")
                await asyncio.sleep(wait)
            else:
                print(f"[score_node] Scoring failed: {e}. Using default scores.")
                break

    for i, idea in enumerate(ideas):
        score = float(scores[i]) if i < len(scores) else 5.0
        memory.update_score(idea.idea_id, score)

        agent = factory.get_agent_by_id(idea.agent_id)
        if agent:
            agent.record_score(score)

    return {"memory": memory, "factory": factory}


# ─────────────────────────────────────────────────────────────
# NODE 4 — evolve
# ─────────────────────────────────────────────────────────────
def evolve_node(state: SwarmState) -> dict:
    factory = state["factory"]
    factory.evolve()
    return {"factory": factory}


# ─────────────────────────────────────────────────────────────
# NODE 5 — synthesize (GROQ)
# ─────────────────────────────────────────────────────────────
async def synthesize_node(state: SwarmState) -> dict:
    memory = state["memory"]

    ideas = memory.get_top_ideas()
    if not ideas:
        return {"final_output": "No ideas generated."}

    ideas_text = "\n".join(
        f"{i+1}. {idea.text}"
        for i, idea in enumerate(ideas)
    )

    prompt = f"""
Problem: {memory.problem}

Top ideas:
{ideas_text}

Combine them into one final structured answer.
"""

    llm = ChatGroq(
        model=settings.SCORING_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=settings.TEMPERATURE_SYNTHESIS,
        max_tokens=settings.MAX_TOKENS_SYNTHESIS,
    )

    for attempt in range(3):
        try:
            response = await llm.ainvoke([HumanMessage(content=prompt)])
            return {"final_output": response.content.strip()}
        except Exception as e:
            err = str(e)
            if "429" in err or "rate_limit" in err.lower():
                wait = 15 * (attempt + 1)
                print(f"[synthesize_node] Rate-limited. Waiting {wait}s before retry {attempt+1}/3...")
                await asyncio.sleep(wait)
            else:
                print(f"[synthesize_node] Synthesis failed: {e}. Returning raw top ideas.")
                break

    # Fallback: just return the raw top ideas as plain text
    fallback = "\n".join(f"- {idea.text}" for idea in ideas)
    return {"final_output": f"[Synthesis unavailable — top ideas]\n{fallback}"}


# ─────────────────────────────────────────────────────────────
# NODE 6 — error
# ─────────────────────────────────────────────────────────────
def error_node(state: SwarmState) -> dict:
    return {"final_output": f"Error: {state.get('error')}"}