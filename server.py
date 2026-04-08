from mcp.server.fastmcp import FastMCP
from chitti.orchestrator import ChittiOrchestrator

mcp = FastMCP("chitti-ai-server")
orchestrator = ChittiOrchestrator(agent_count=5)


@mcp.tool()
def initialize_chitti(problem: str)  -> dict:
    """
    Initialize a new Chitti AI session with a user problem.
    """
    return orchestrator.initialize(problem)


@mcp.tool()
def run_chitti_iteration() -> dict:
    """
    Run one iteration where all agents read shared memory
    and contribute or improve ideas.
    """
    return orchestrator.run_iteration()


@mcp.tool()
def score_chitti_ideas() -> dict:
    """
    Score all ideas, vote on the best ideas, and return the current best idea.
    """
    return orchestrator.score_and_vote()


@mcp.tool()
def run_chitti_full(iterations: int = 3) -> dict:
    """
    Run the full Chitti process:
    initialize first, then iterative idea generation,
    then scoring and final output selection.
    """
    return orchestrator.run_full_process(iterations=iterations)


@mcp.tool()
def get_chitti_state() -> dict:
    """
    Get the current Chitti shared memory state.
    """
    return orchestrator.get_state()


if __name__ == "__main__":
    print("Testing Chitti locally...")

    print("\n1. Initialize")
    print(orchestrator.initialize("Create a 7-day web development plan"))

    print("\n2. Iteration 1")
    print(orchestrator.run_iteration())

    print("\n3. Iteration 2")
    print(orchestrator.run_iteration())

    print("\n4. Iteration 3")
    print(orchestrator.run_iteration())

    print("\n5. Score")
    print(orchestrator.score_and_vote())