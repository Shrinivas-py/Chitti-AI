import sys
import os
import asyncio

# -------------------------------
# PATH FIX (to access core engine)
# -------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENGINE_PATH = os.path.join(BASE_DIR, "swarm_ai-main")

if ENGINE_PATH not in sys.path:
    sys.path.insert(0, ENGINE_PATH)


import uuid
from typing import Dict, Any
from core.workflow import run_swarm


# -------------------------------
# STATE STORE (in-memory for now)
# -------------------------------
STATE_DB: Dict[str, Dict[str, Any]] = {}


# -------------------------------
# SESSION INIT
# -------------------------------
def initialize_session(problem: str) -> Dict[str, Any]:
    state = {
        "id": str(uuid.uuid4()),
        "problem": problem,
        "iteration": 0,
        "ideas": [],
        "final_output": "",
    }
    STATE_DB[state["id"]] = state
    return state


# -------------------------------
# RUN ONE ITERATION
# -------------------------------
def run_iteration(state: Dict[str, Any]) -> Dict[str, Any]:
    problem = state["problem"]

    # Run the full async LangGraph swarm
    import time

    try:
        result = asyncio.run(run_swarm(problem))
    except Exception as e:
        if "rate_limit" in str(e):
            print("⚠️ Rate limit hit. Waiting 6 seconds...")
            time.sleep(6)
            result = asyncio.run(run_swarm(problem))
        else:
            raise e

    # result is a LangGraph state DICT — access via keys, not getattr
    ideas = []
    memory = result.get("memory")
    if memory:
        for idea in memory.get_all_ideas():
            ideas.append({
                "content":     idea.text,
                "agent_id":    idea.agent_id,
                "agent_style": idea.agent_style,
                "iteration":   idea.iteration,
                "score":       idea.score,
                "parent_ids":  idea.parent_ids,
                "action_type": idea.action_type,
                "reason":      idea.reason,
                "votes":       idea.votes,
            })

    state["iteration"]    += 1
    state["ideas"]         = ideas
    state["final_output"]  = result.get("final_output") or ""

    return state


# -------------------------------
# SCORE + SELECT BEST IDEAS
# -------------------------------
def score_and_select(state: Dict[str, Any]) -> Dict[str, Any]:
    ideas = state["ideas"]

    # Fall back to content-length score if LLM didn't score it
    for idea in ideas:
        if idea["score"] == 0:
            idea["score"] = len(idea["content"])

    ideas.sort(key=lambda x: x["score"], reverse=True)
    state["ideas"] = ideas
    return state


# -------------------------------
# GET CURRENT STATE
# -------------------------------
def get_state(state: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "problem":      state["problem"],
        "iteration":    state["iteration"],
        "ideas":        state["ideas"],
        "final_output": state.get("final_output", ""),
    }