# memory/memory.py
# ─────────────────────────────────────────────────────────────────────────────
# SwarmMemory — the shared whiteboard that all agents read from and write to.
#
# Current implementation: pure in-memory Python (no server needed to run).
#
# ┌──────────────────────────────────────────────────────────────────────────┐
# │  FOR YOUR FRIEND (MCP backend developer)                                 │
# │                                                                          │
# │  This class is the ONLY integration point between the agent engine       │
# │  and the MCP server.                                                     │
# │                                                                          │
# │  To connect: subclass SwarmMemory and override these 5 methods:         │
# │    - add_idea()          → POST to your MCP server                      │
# │    - update_score()      → PUT to your MCP server                       │
# │    - get_all_ideas()     → GET from your MCP server                     │
# │    - get_top_ideas()     → GET /top from your MCP server                │
# │    - get_ideas_for_iter()→ GET ?iteration=N from your MCP server        │
# │                                                                          │
# │  Everything else in the engine stays the same. Just swap the class.     │
# │                                                                          │
# │  Example (your friend writes this):                                      │
# │    class MCPServerMemory(SwarmMemory):                                   │
# │        async def add_idea(self, ...):                                    │
# │            await httpx.post(f"{MCP_URL}/ideas", json={...})             │
# └──────────────────────────────────────────────────────────────────────────┘
from __future__ import annotations
from dataclasses import dataclass, field
from config import settings


# ─────────────────────────────────────────────────────────────────────────────
# Idea — the atomic unit of data in shared memory
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Idea:
    """
    One idea contributed by one agent in one iteration.
    This is everything stored in MCP for each thought.
    """
    idea_id: int
    text: str
    agent_id: int
    agent_style: str
    iteration: int
    score: float = 0.0
    parent_ids: list = field(default_factory=list)
    action_type: str = "generate"   # generate | refine | combine | add
    reason: str = ""
    votes: int = 0

    def to_context_dict(self) -> dict:
        """
        Format used when agents read MCP before generating.
        Keys match what agents/factory.py expects in prior_ideas list.
        """
        return {
            "text": self.text,
            "style": self.agent_style,
            "score": self.score,
        }

    def to_dict(self) -> dict:
        """Full serializable dict for api.py and MCP server handoff."""
        return {
            "idea_id":     self.idea_id,
            "text":        self.text,
            "agent_id":    self.agent_id,
            "agent_style": self.agent_style,
            "iteration":   self.iteration,
            "score":       self.score,
            "parent_ids":  self.parent_ids,
            "action_type": self.action_type,
            "reason":      self.reason,
            "votes":       self.votes,
        }


# ─────────────────────────────────────────────────────────────────────────────
# SwarmMemory — the whiteboard
# ─────────────────────────────────────────────────────────────────────────────

class SwarmMemory:
    """
    Shared memory for the swarm. All agents read from and write to this.

    In swarm intelligence terms: this is the digital pheromone field.
    Agents don't talk directly to each other — they communicate through here.

    To connect to your friend's MCP server: subclass and override methods.
    See the comment block at the top of this file.
    """

    def __init__(self):
        self.problem: str = ""
        self.iteration: int = 0
        self._ideas: list[Idea] = []
        self._counter: int = 0

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def initialize(self, problem: str) -> None:
        """
        Resets memory and sets the problem for this run.
        FIRST thing called at the start of every swarm run.

        [MCP INTEGRATION] Your friend's server receives:
            POST /mcp/initialize  body: {"problem": problem}
        """
        self.problem = problem
        self.iteration = 0
        self._ideas = []
        self._counter = 0
        print(f"[Memory] Initialized | {problem[:80]}{'...' if len(problem) > 80 else ''}")

    def advance_iteration(self) -> int:
        """
        Increments iteration counter. Called at the start of each cycle.

        [MCP INTEGRATION] Tracked server-side via iteration field in state.
        """
        self.iteration += 1
        print(f"[Memory] → Iteration {self.iteration}")
        return self.iteration

    # ── Write operations ─────────────────────────────────────────────────────
    # These are called BY the engine, received BY the MCP server

    def add_idea(
        self,
        text: str,
        agent_id: int,
        agent_style: str,
        action_type: str = "generate",
        reason: str = "",
        parent_ids: list = None,
    ) -> Idea:
        """
        Writes one agent's idea into shared memory.
        Called once per agent per iteration.

        [MCP INTEGRATION] Your friend's server receives:
            POST /mcp/ideas
            body: {"text": text, "agent_id": agent_id,
                   "agent_style": agent_style, "iteration": self.iteration,
                   "action_type": action_type, "reason": reason}
        """
        self._counter += 1
        idea = Idea(
            idea_id=self._counter,
            text=text,
            agent_id=agent_id,
            agent_style=agent_style,
            iteration=self.iteration,
            action_type=action_type,
            reason=reason,
            parent_ids=parent_ids or [],
        )
        self._ideas.append(idea)
        return idea

    def update_score(self, idea_id: int, score: float) -> None:
        """
        Writes quality score back to a specific idea.
        Called by the scoring node after Grok evaluates each idea.

        [MCP INTEGRATION] Your friend's server receives:
            PUT /mcp/ideas/{idea_id}
            body: {"score": score}
        """
        for idea in self._ideas:
            if idea.idea_id == idea_id:
                idea.score = round(score, 2)
                return
        print(f"[Memory] Warning: idea_id={idea_id} not found for score update")

    # ── Read operations ───────────────────────────────────────────────────────
    # These are called BY the engine, served BY the MCP server

    def get_all_ideas(self) -> list[Idea]:
        """
        Returns all ideas ever written to memory (all iterations).
        Used to build context for agents before they generate.

        [MCP INTEGRATION] Your friend's server handles:
            GET /mcp/ideas → returns list of all Idea dicts
        """
        return self._ideas.copy()

    def get_ideas_for_iteration(self, iteration: int) -> list[Idea]:
        """
        Returns only ideas from a specific iteration.
        Used by the scoring node to score one batch at a time.

        [MCP INTEGRATION] Your friend's server handles:
            GET /mcp/ideas?iteration={iteration}
        """
        return [i for i in self._ideas if i.iteration == iteration]

    def get_top_ideas(self, n: int = None) -> list[Idea]:
        """
        Returns n highest-scoring ideas across all iterations.
        Used by the synthesis node for final output generation.

        [MCP INTEGRATION] Your friend's server handles:
            GET /mcp/ideas/top?n={n}
        """
        n = n or settings.TOP_IDEAS_TO_KEEP
        scored = [i for i in self._ideas if i.score > 0.0]
        return sorted(scored, key=lambda x: x.score, reverse=True)[:n]

    def get_context_for_agents(self) -> list[dict]:
        """
        Returns all ideas as context dicts — the format agents read from MCP.
        This is what gets injected into agent prompts as 'prior ideas'.
        """
        return [i.to_context_dict() for i in self._ideas]

    # ── Inspection ────────────────────────────────────────────────────────────

    def state_summary(self) -> dict:
        """Human-readable summary. Printed after every iteration."""
        scored = [i for i in self._ideas if i.score > 0.0]
        return {
            "iteration": self.iteration,
            "total_ideas": len(self._ideas),
            "scored": len(scored),
            "top_score": round(max((i.score for i in scored), default=0.0), 2),
            "avg_score": round(
                sum(i.score for i in scored) / len(scored), 2
            ) if scored else 0.0,
        }

    def export(self) -> dict:
        """
        Full export of memory state.
        This is what api.py passes to your friend's MCP server at the end.
        """
        return {
            "problem": self.problem,
            "iteration": self.iteration,
            "ideas": [i.to_dict() for i in self._ideas],
            "top_ideas": [i.to_dict() for i in self.get_top_ideas()],
        }