from swarm_engine.api import initialize_session, run_iteration, score_and_select, get_state

problem = "AI project idea in the field of healthcare"

state = initialize_session(problem)
state = run_iteration(state)
state = score_and_select(state)

output = get_state(state)

print(output)