# swarm_ai-main/__init__.py
# Inner engine package. Imports are done directly by consumers via sys.path.
# Do NOT re-export here — it causes circular imports with the sys.path injection
# pattern used in swarm_engine/api.py.