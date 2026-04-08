# api.py
# ─────────────────────────────────────────────────────────────────────────────
# The orchestrator / merge point between your agent engine and the MCP backend.
#
# Two responsibilities:
#   1. Run the swarm and collect the final state
#   2. Format results and hand them off to the MCP server
#
# Your friend's MCP server does NOT need to know about LangGraph, nodes,
# or any internal swarm mechanics. It just receives a clean payload dict.
#
# HOW YOUR FRIEND CONNECTS:
#   Replace the stub at the bottom (_send_to_mcp_server) with an actual
#   HTTP POST to his MCP server. The payload schema is defined in SwarmResult.
# ─────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
import asyncio
import json
from dataclasses import dataclass, asdict

from core.workflow import run_swarm
from config import settings


# ─────────────────────────────────────────────────────────────────────────────
# SwarmResult — the payload this engine sends to the MCP backend
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class SwarmResult:
    """
    Complete result of one swarm run.
    This dict is what your friend's MCP server receives after a run finishes.
    """
    problem: str
    final_output: str
    total_ideas: int
    iterations_run: int
    agents_started: int
    agents_survived: int
    top_ideas: list
    all_ideas: list
    agent_summary: list

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


# ─────────────────────────────────────────────────────────────────────────────
# Core run function — called from main.py or your friend's trigger
# ─────────────────────────────────────────────────────────────────────────────

async def execute_swarm(
    problem: str,
    num_agents: int = None,
    num_iterations: int = None,
    batch_size: int = None,
    send_to_mcp: bool = True,
) -> SwarmResult:
    """
    Runs the full swarm and returns a SwarmResult.
    Optionally calls _send_to_mcp_server() with the result.

    Args:
        problem         → the question or task to solve
        num_agents      → override default agent count
        num_iterations  → override default iteration count
        batch_size      → override default batch size
        send_to_mcp     → whether to forward results to MCP backend

    Returns:
        SwarmResult with everything the MCP server needs
    """
    print(f"\n[API] Starting swarm execution")
    print(f"[API] Problem: {problem[:80]}")

    # Run the LangGraph swarm
    final_state = await run_swarm(
        problem=problem,
        num_agents=num_agents or settings.SWARM_NUM_AGENTS,
        num_iterations=num_iterations or settings.SWARM_NUM_ITERATIONS,
        batch_size=batch_size or settings.SWARM_BATCH_SIZE,
    )

    memory  = final_state["memory"]
    factory = final_state["factory"]

    # Build the clean result payload
    result = SwarmResult(
        problem=memory.problem,
        final_output=final_state["final_output"] or "",
        total_ideas=len(memory.get_all_ideas()),
        iterations_run=memory.iteration,
        agents_started=factory.num_agents,
        agents_survived=len(factory.get_active_agents()),
        top_ideas=[i.to_dict() for i in memory.get_top_ideas()],
        all_ideas=[i.to_dict() for i in memory.get_all_ideas()],
        agent_summary=factory.summary()["agents"],
    )

    print(f"\n[API] Run complete")
    print(f"[API] Total ideas  : {result.total_ideas}")
    print(f"[API] Agents left  : {result.agents_survived}/{result.agents_started}")
    print(f"[API] Output length: {len(result.final_output)} chars")

    # Forward to MCP backend
    if send_to_mcp:
        await _send_to_mcp_server(result)

    return result


# ─────────────────────────────────────────────────────────────────────────────
# MCP integration stub — your friend fills this in
# ─────────────────────────────────────────────────────────────────────────────

async def _send_to_mcp_server(result: SwarmResult) -> None:
    """
    Sends the swarm result to your friend's MCP server.

    CURRENT STATE: logs the payload to console (no server needed to run).

    YOUR FRIEND REPLACES THIS with:
        import httpx
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{MCP_SERVER_URL}/mcp/run_complete",
                json=result.to_dict(),
                timeout=30.0,
            )

    Payload your friend's server will receive (result.to_dict()):
    {
        "problem": "...",
        "final_output": "...",         ← the synthesized answer
        "total_ideas": 30,             ← ideas generated in total
        "iterations_run": 3,
        "agents_started": 10,
        "agents_survived": 7,          ← after evolution pruning
        "top_ideas": [                 ← best ideas with scores
            {
                "idea_id": 1,
                "text": "...",
                "agent_id": 3,
                "agent_style": "pragmatic",
                "iteration": 2,
                "score": 8.7
            },
            ...
        ],
        "all_ideas": [...],            ← every idea from every iteration
        "agent_summary": [             ← per-agent stats
            {
                "id": 1,
                "style": "analytical",
                "temperature": 0.35,
                "average_score": 7.2,
                "idea_scores": [6.8, 7.6],
                "status": "elite"
            },
            ...
        ]
    }
    """
    print("\n[API → MCP] Payload ready to send to MCP server:")
    print(f"  problem        : {result.problem[:60]}")
    print(f"  total_ideas    : {result.total_ideas}")
    print(f"  top_ideas      : {len(result.top_ideas)}")
    print(f"  agents_survived: {result.agents_survived}/{result.agents_started}")
    print(f"  output preview : {result.final_output[:120]}...")
    print("\n[API → MCP] (Stub: replace _send_to_mcp_server with actual HTTP call)")