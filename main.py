import json
import sys
from swarm_engine.api import initialize_session, run_iteration, score_and_select, get_state
from swarm_engine.fallback import DUMMY_ITERATIONS, DUMMY_FINAL_OUTPUT, PROBLEM


# ─────────────────────────────────────────────────────────────────────────────
# SHARED PRINTER — used by both live and fallback paths
# ─────────────────────────────────────────────────────────────────────────────

W = 70

def _print_iteration(iter_payload: dict) -> None:
    iter_num = iter_payload["iteration"]
    print()
    print()
    print("█" * W)
    print("█" + " " * (W - 2) + "█")
    label = f"  ITERATION  {iter_num}  "
    print("█" + label.center(W - 2) + "█")
    print("█" + " " * (W - 2) + "█")
    print("█" * W)
    print(json.dumps(iter_payload, indent=2))


def _print_final(final_output: str, total_ideas: int, total_iters: int, source: str = "LIVE") -> None:
    print()
    print()
    print("█" * W)
    print("█" + " " * (W - 2) + "█")
    label = "  FINAL SYNTHESIZED OUTPUT  "
    print("█" + label.center(W - 2) + "█")
    print("█" + " " * (W - 2) + "█")
    print("█" * W)
    print()
    print(final_output or "(no synthesis output)")
    print()
    print(f"Source         : {source}")
    print(f"Total ideas    : {total_ideas}")
    print(f"Total iterations: {total_iters}")


# ─────────────────────────────────────────────────────────────────────────────
# LIVE PATH — try running the real swarm
# ─────────────────────────────────────────────────────────────────────────────

def run_live(problem: str) -> bool:
    """Returns True if the live swarm ran successfully, False otherwise."""
    try:
        state  = initialize_session(problem)
        state  = run_iteration(state)
        state  = score_and_select(state)
        output = get_state(state)

        # Group ideas by iteration
        from collections import defaultdict
        by_iteration = defaultdict(list)
        for idea in output["ideas"]:
            by_iteration[idea["iteration"]].append(idea)

        total_iterations = max(by_iteration.keys(), default=0)

        for iter_num in range(1, total_iterations + 1):
            ideas_raw = by_iteration.get(iter_num, [])
            iter_payload = {
                "problem":   output["problem"],
                "iteration": iter_num,
                "ideas": [
                    {
                        "content":     idea["content"],
                        "agent_style": idea["agent_style"],
                        "parent_ids":  idea["parent_ids"],
                        "action_type": idea["action_type"],
                        "reason":      idea["reason"],
                        "score":       idea["score"],
                        "votes":       idea["votes"],
                    }
                    for idea in ideas_raw
                ],
            }
            _print_iteration(iter_payload)

        _print_final(
            output.get("final_output", ""),
            total_ideas=len(output["ideas"]),
            total_iters=output["iteration"],
            source="LIVE (AI)",
        )
        return True

    except Exception as e:
        print(f"\n[SWARM] Live execution failed: {e}", file=sys.stderr)
        print("[SWARM] Falling back to pre-generated dummy output.\n", file=sys.stderr)
        return False


# ─────────────────────────────────────────────────────────────────────────────
# FALLBACK PATH — static pre-generated output (AI unavailable)
# ─────────────────────────────────────────────────────────────────────────────

def run_fallback() -> None:
    total_ideas = sum(len(it["ideas"]) for it in DUMMY_ITERATIONS)
    for iter_payload in DUMMY_ITERATIONS:
        _print_iteration(iter_payload)
    _print_final(
        DUMMY_FINAL_OUTPUT,
        total_ideas=total_ideas,
        total_iters=len(DUMMY_ITERATIONS),
        source="FALLBACK (pre-generated — AI unavailable)",
    )


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

problem = PROBLEM

if not run_live(problem):
    run_fallback()