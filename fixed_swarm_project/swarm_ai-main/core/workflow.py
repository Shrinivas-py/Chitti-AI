from __future__ import annotations
from langgraph.graph import StateGraph, START, END

from core.state import SwarmState
from core.nodes import (
    initialize_node,
    generate_node,
    score_node,
    evolve_node,
    synthesize_node,
    error_node,
)

from config import settings
from core.utils import get_agent_count   # ✅ NEW


# ─────────────────────────────────────────────────────────────────────────────
# Routing function
# ─────────────────────────────────────────────────────────────────────────────

def _route_after_scoring(state: SwarmState) -> str:
    if state.get("error"):
        return "error"

    current  = state.get("current_iteration", 0)
    max_iter = state.get("max_iterations", settings.SWARM_NUM_ITERATIONS)

    if current < max_iter:
        return "evolve"
    return "finish"


# ─────────────────────────────────────────────────────────────────────────────
# Graph builder
# ─────────────────────────────────────────────────────────────────────────────

def build_graph():
    graph = StateGraph(SwarmState)

    graph.add_node("initialize", initialize_node)
    graph.add_node("generate",   generate_node)
    graph.add_node("score",      score_node)
    graph.add_node("evolve",     evolve_node)
    graph.add_node("synthesize", synthesize_node)
    graph.add_node("error",      error_node)

    graph.add_edge(START, "initialize")

    graph.add_edge("initialize", "generate")
    graph.add_edge("generate",   "score")

    graph.add_conditional_edges(
        "score",
        _route_after_scoring,
        {
            "evolve":  "evolve",
            "finish":  "synthesize",
            "error":   "error",
        },
    )

    graph.add_edge("evolve", "generate")

    graph.add_edge("synthesize", END)
    graph.add_edge("error",      END)

    return graph.compile()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENTRY
# ─────────────────────────────────────────────────────────────────────────────

async def run_swarm(
    problem: str,
    num_agents: int    = None,
    num_iterations: int = None,
    batch_size: int    = None,
) -> dict:

    graph = build_graph()

    # 🔥 Gemini SMALL MODEL decides agent count
    dynamic_agents = get_agent_count(problem)

    initial_state: SwarmState = {
        "problem":          problem,
        "max_iterations":   num_iterations or settings.SWARM_NUM_ITERATIONS,
        "batch_size":       batch_size     or settings.SWARM_BATCH_SIZE,

        # ✅ REPLACED THIS LINE
        "num_agents":       num_agents or dynamic_agents,

        "memory":           None,
        "factory":          None,
        "current_iteration": 0,
        "final_output":     None,
        "error":            None,
    }

    final_state = await graph.ainvoke(initial_state)
    return final_state