# agents/factory.py
# ─────────────────────────────────────────────────────────────────────────────
# AgentFactory — creates, manages, and evolves the agent pool.
#
# What an "agent" is in this system:
#   NOT a separate process, server, or LLM instance.
#   It IS a lightweight Python dataclass that holds:
#       - a personality (thinking style + system prompt + temperature)
#       - state (pruned/elite flags, score history)
#       - logic to build its own LangChain ChatGroq call
#
#   One Groq API key, one model — called N times with different parameters.
#   That's the virtualization. Scaling perspectives, not machines.
#
# LangChain components used:
#   ChatGroq          — LangChain's Groq provider (drop-in ChatModel)
#   ChatPromptTemplate — structures system + human messages cleanly
#   StrOutputParser   — extracts string content from ChatMessage response
# ─────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
import random
from dataclasses import dataclass, field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from agents.personalities import PERSONALITIES
from config import settings


# ─────────────────────────────────────────────────────────────────────────────
# Agent dataclass
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Agent:
    """
    One virtual agent in the swarm.

    Fields:
        id            → unique integer, used in all logs and state records
        style         → personality name (e.g. "analytical")
        description   → one-line summary for display
        temperature   → float, controls response creativity (set per-agent)
        is_pruned     → True after evolution removes this agent
        is_elite      → True after evolution promotes this agent
        idea_scores   → list of floats, one per iteration this agent participated in
    """
    id: int
    style: str
    description: str
    temperature: float
    _system_prompt: str

    is_pruned: bool = field(default=False, init=False)
    is_elite: bool = field(default=False, init=False)
    idea_scores: list[float] = field(default_factory=list, init=False)

    # ── Scoring ───────────────────────────────────────────────────────────────

    def record_score(self, score: float) -> None:
        """Called by nodes.py after the scoring step writes back to this agent."""
        self.idea_scores.append(round(score, 2))

    @property
    def average_score(self) -> float:
        if not self.idea_scores:
            return 5.0
        return round(sum(self.idea_scores) / len(self.idea_scores), 2)

    # ── LangChain chain builder ───────────────────────────────────────────────

    def build_chain(self):
        """
        Builds a LangChain LCEL chain for this agent:
            ChatPromptTemplate | ChatGroq | StrOutputParser

        Returns a runnable chain. Call with:
            chain.invoke({"problem": ..., "iteration": ..., "prior_ideas_text": ...})

        The chain is built fresh each call — ChatGroq is stateless.
        """
        # System message: injects this agent's personality
        system_message = (
            "You are a swarm AI agent. Your thinking style: {style}.\n\n"
            "{system_prompt}\n\n"
            "You are part of a multi-agent collaborative system. "
            "Contribute exactly ONE high-quality, specific idea per turn. "
            "Your thinking style must be clearly visible in your response."
        )

        # Human message: the actual task with context from MCP
        human_message = (
            "Problem: \"{problem}\"\n\n"
            "{iteration_instruction}"
            "{prior_ideas_section}\n\n"
            "RULES:\n"
            "- ONE idea only. Maximum 2 sentences.\n"
            "- Be specific. No vague advice.\n"
            "- Your idea must clearly reflect your {style} thinking style.\n"
            "- No preamble. No 'As an AI'.\n\n"
            "Respond with ONLY valid JSON — no markdown, no extra text:\n"
            '{{"content": "<your idea, max 2 sentences>", '
            '"action_type": "<generate|refine|combine|add>", '
            '"reason": "<one sentence explaining why this idea>"}}'
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human",  human_message),
        ])

        llm = ChatGroq(
            model=settings.AGENT_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=self.temperature,
            max_tokens=settings.MAX_TOKENS_AGENT,
        )

        # LCEL chain: prompt → llm → parse string output
        chain = prompt | llm | StrOutputParser()
        return chain

    def build_invoke_input(
        self,
        problem: str,
        iteration: int,
        prior_ideas: list[dict],
    ) -> dict:
        """
        Builds the input dict for chain.invoke().

        prior_ideas is a list of dicts:
            [{"text": str, "style": str, "score": float}, ...]
        These come from MCP shared memory.
        """
        # Format prior ideas for injection into the prompt
        if prior_ideas and iteration > 1:
            recent = prior_ideas[-settings.PRIOR_IDEAS_CONTEXT_WINDOW:]
            lines = "\n".join(
                f"  {i + 1}. [{idea['style']}] {idea['text']}"
                + (f"  ★{idea['score']:.1f}" if idea.get("score", 0) > 0 else "")
                for i, idea in enumerate(recent)
            )
            prior_ideas_section = (
                f"\n\n--- MCP SHARED MEMORY (what other agents contributed) ---\n"
                f"{lines}\n"
                f"--- END MCP ---"
            )
            iteration_instruction = (
                f"Iteration {iteration}: Read the shared memory above carefully. "
                "Then do ONE of: (a) improve the best idea you see, "
                "(b) combine two ideas into one stronger idea, "
                "(c) add what is clearly missing. Do NOT repeat what's already there.\n"
            )
        else:
            prior_ideas_section = ""
            iteration_instruction = (
                "Iteration 1: The idea pool is empty. "
                "Think independently and generate a fresh idea.\n"
            )

        return {
            "style": self.style,
            "system_prompt": self._system_prompt,
            "problem": problem,
            "iteration_instruction": iteration_instruction,
            "prior_ideas_section": prior_ideas_section,
        }

    # ── Display ───────────────────────────────────────────────────────────────

    def label(self) -> str:
        return f"A-{self.id:02d}|{self.style}"

    def to_dict(self) -> dict:
        """Serializable dict — used in api.py response payload."""
        tag = "pruned" if self.is_pruned else ("elite" if self.is_elite else "active")
        return {
            "id": self.id,
            "style": self.style,
            "description": self.description,
            "temperature": self.temperature,
            "average_score": self.average_score,
            "idea_scores": self.idea_scores,
            "status": tag,
        }

    def __repr__(self) -> str:
        tag = " [PRUNED]" if self.is_pruned else (" [ELITE]" if self.is_elite else "")
        return f"Agent({self.label()} temp={self.temperature} avg={self.average_score}){tag}"


# ─────────────────────────────────────────────────────────────────────────────
# AgentFactory
# ─────────────────────────────────────────────────────────────────────────────

class AgentFactory:
    """
    Creates and manages the full agent pool for one swarm run.

    Usage:
        factory = AgentFactory(num_agents=10)
        factory.initialize()
        agents = factory.get_active_agents()
        # ... after scoring ...
        factory.evolve()
    """

    def __init__(self, num_agents: int):
        self.num_agents = num_agents
        self.agents: list[Agent] = []

    def initialize(self) -> list[Agent]:
        """
        Spawns num_agents agents by cycling through personalities.
        Personalities are shuffled so the first N are always varied.
        If num_agents > 20, personalities repeat with different temperatures.
        """
        self.agents = []
        shuffled = PERSONALITIES.copy()
        random.shuffle(shuffled)

        for i in range(self.num_agents):
            p = shuffled[i % len(shuffled)]

            # Add a small random offset to the personality's base temperature
            # This ensures two agents with the same personality still differ slightly
            base_temp = p["temperature"]
            offset = random.uniform(-0.08, 0.08)
            final_temp = round(
                max(settings.TEMPERATURE_MIN, min(settings.TEMPERATURE_MAX, base_temp + offset)),
                2,
            )

            agent = Agent(
                id=i + 1,
                style=p["style"],
                description=p["description"],
                temperature=final_temp,
                _system_prompt=p["system_prompt"],
            )
            self.agents.append(agent)

        print(f"[Factory] Spawned {self.num_agents} agents:")
        for a in self.agents:
            print(f"  {a}")

        return self.agents

    def get_active_agents(self) -> list[Agent]:
        """Returns all non-pruned agents."""
        return [a for a in self.agents if not a.is_pruned]

    def get_agent_by_id(self, agent_id: int) -> Agent | None:
        return next((a for a in self.agents if a.id == agent_id), None)

    def evolve(self) -> dict:
        """
        One evolution step:
          1. Rank active agents by average score (ascending = worst first)
          2. Prune bottom PRUNE_RATE fraction
          3. Mark top 20% of survivors as elite

        Returns summary dict: {"pruned": [ids], "elite": [ids]}
        """
        active = self.get_active_agents()

        if len(active) < 3:
            print("[Factory] Too few agents to evolve. Skipping.")
            return {"pruned": [], "elite": []}

        ranked = sorted(active, key=lambda a: a.average_score)
        prune_count = max(1, int(len(active) * settings.PRUNE_RATE))

        # Prune weakest
        pruned_ids = []
        for agent in ranked[:prune_count]:
            agent.is_pruned = True
            pruned_ids.append(agent.id)
            print(f"  [Pruned] {agent.label()} avg={agent.average_score}")

        # Reset and re-promote elite
        survivors = self.get_active_agents()
        for a in survivors:
            a.is_elite = False

        elite_count = max(1, int(len(survivors) * 0.20))
        elite_ids = []
        for agent in sorted(survivors, key=lambda a: a.average_score, reverse=True)[:elite_count]:
            agent.is_elite = True
            elite_ids.append(agent.id)
            print(f"  [Elite]  {agent.label()} avg={agent.average_score}")

        print(
            f"[Factory] {len(survivors)} active | "
            f"{prune_count} pruned | "
            f"{elite_count} elite"
        )
        return {"pruned": pruned_ids, "elite": elite_ids}

    def summary(self) -> dict:
        """Full serializable summary for api.py."""
        active = self.get_active_agents()
        return {
            "total": len(self.agents),
            "active": len(active),
            "pruned": len(self.agents) - len(active),
            "elite": sum(1 for a in active if a.is_elite),
            "agents": [a.to_dict() for a in self.agents],
        }