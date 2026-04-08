# core/state.py
# ─────────────────────────────────────────────────────────────────────────────
# SwarmState — the single object that flows through every LangGraph node.
#
# LangGraph requires TypedDict for the state schema.
# Every node receives the full state, modifies what it needs,
# and returns ONLY the fields it changed.
# LangGraph merges the returned dict back into the full state automatically.
#
# Why TypedDict and not Pydantic?
#   LangGraph's StateGraph is built on TypedDict.
#   Pydantic objects live as VALUES inside the state (e.g. memory, factory).
# ─────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
from typing import TypedDict, Optional
from memory.memory import SwarmMemory
from agents.factory import AgentFactory


class SwarmState(TypedDict):
    """
    Complete state of one swarm run.
    Flows through every node: initialize → generate → score → evolve → synthesize.

    Fields set before the graph starts (in workflow.py → run_swarm):
        problem           → the user's input question/task
        max_iterations    → total generate→score→evolve cycles to run
        batch_size        → concurrent agents per batch (controls Groq rate limit safety)
        num_agents        → total agents to spawn

    Fields set by initialize_node (first node):
        memory            → SwarmMemory instance (the shared whiteboard)
        factory           → AgentFactory instance (manages agent pool)
        current_iteration → starts at 0, incremented by generate_node

    Fields set by the final nodes:
        final_output      → synthesized answer string (set by synthesize_node)
        error             → error message if anything fails (set by error_node)
    """

    # ── Run configuration (set once before graph starts) ─────────────────────
    problem: str
    max_iterations: int
    batch_size: int
    num_agents: int

    # ── Live state (updated by nodes as graph runs) ───────────────────────────
    memory: Optional[SwarmMemory]
    factory: Optional[AgentFactory]
    current_iteration: int

    # ── Outputs ───────────────────────────────────────────────────────────────
    final_output: Optional[str]
    error: Optional[str]