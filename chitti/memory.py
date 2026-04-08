from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import uuid


@dataclass
class Idea:
    id: str
    content: str
    agent_name: str
    iteration: int
    score: float = 0.0
    votes: int = 0
    parent_ids: List[str] = field(default_factory=list)
    action_type: str = ""
    reason: str = ""


@dataclass
class ChittiState:
    problem: str
    iteration: int = 0
    ideas: List[Idea] = field(default_factory=list)
    best_idea_id: Optional[str] = None
    history: List[Dict[str, Any]] = field(default_factory=list)


def initialize_state(problem: str) -> ChittiState:
    return ChittiState(problem=problem)


def add_idea(
    state: ChittiState,
    content: str,
    agent_name: str,
    iteration: int,
    parent_ids=None,
    action_type: str = "",
    reason: str = ""
):
    if parent_ids is None:
        parent_ids = []

    idea = Idea(
        id=str(uuid.uuid4()),
        content=content,
        agent_name=agent_name,
        iteration=iteration,
        parent_ids=parent_ids,
        action_type=action_type,
        reason=reason
    )

    state.ideas.append(idea)

    state.history.append({
        "event": "idea_added",
        "agent_name": agent_name,
        "iteration": iteration,
        "idea_id": idea.id,
        "content": content,
        "action_type": action_type,
        "reason": reason,
        "parent_ids": parent_ids
    })

    return idea


def state_to_dict(state: ChittiState) -> dict:
    return {
        "problem": state.problem,
        "iteration": state.iteration,
        "best_idea_id": state.best_idea_id,
        "ideas": [
            {
                "id": idea.id,
                "content": idea.content,
                "agent_name": idea.agent_name,
                "iteration": idea.iteration,
                "score": idea.score,
                "votes": idea.votes,
                "parent_ids": idea.parent_ids,
                "action_type": idea.action_type,
                "reason": idea.reason,
            }
            for idea in state.ideas
        ],
        "history": state.history,
    }