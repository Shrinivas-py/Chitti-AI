from chitti.memory import initialize_state, add_idea, state_to_dict
from chitti.agents import build_agents
from chitti.scorer import score_all_ideas, vote_best_ideas, choose_best_idea
import re


class ChittiOrchestrator:
    def __init__(self, agent_count: int = 5):
        self.agents = build_agents(agent_count)
        self.state = None

    def initialize(self, problem: str):
        self.state = initialize_state(problem)
        return state_to_dict(self.state)

    def deduplicate_ideas(self):
        if self.state is None:
            return

        seen = set()
        unique_ideas = []

        for idea in self.state.ideas:
            normalized = idea.content.strip().lower()
            if normalized not in seen:
                seen.add(normalized)
                unique_ideas.append(idea)

        self.state.ideas = unique_ideas

    def extract_day_number(self, text: str):
        match = re.search(r"Day\s+(\d+)", text)
        return int(match.group(1)) if match else 999

    def clean_line(self, text: str):
        while "and connect it with the next day's topic and connect it with the next day's topic" in text:
            text = text.replace(
                "and connect it with the next day's topic and connect it with the next day's topic",
                "and connect it with the next day's topic"
            )

        while "with one hands-on mini project with one hands-on mini project" in text:
            text = text.replace(
                "with one hands-on mini project with one hands-on mini project",
                "with one hands-on mini project"
            )

        while "and include 1 hour of revision and include 1 hour of revision" in text:
            text = text.replace(
                "and include 1 hour of revision and include 1 hour of revision",
                "and include 1 hour of revision"
            )

        while "while focusing on practical implementation while focusing on practical implementation" in text:
            text = text.replace(
                "while focusing on practical implementation while focusing on practical implementation",
                "while focusing on practical implementation"
            )

        return text.strip()

    def synthesize_final_answer(self):
        if self.state is None or not self.state.ideas:
            return None

        sorted_ideas = sorted(
            self.state.ideas,
            key=lambda x: (x.score, x.votes, x.iteration),
            reverse=True
        )

        unique_by_day = {}

        for idea in sorted_ideas:
            day = self.extract_day_number(idea.content)
            cleaned = self.clean_line(idea.content)

            if day not in unique_by_day:
                unique_by_day[day] = cleaned

        final_lines = [unique_by_day[day] for day in sorted(unique_by_day.keys())]
        final_lines = [f"{i+1}. {line}" for i, line in enumerate(final_lines)]

        return "\n".join(final_lines)

    def run_iteration(self):
        if self.state is None:
            raise ValueError("Chitti working not initialized")

        self.state.iteration += 1

        for agent in self.agents:
            result = agent.generate_idea(self.state)
            add_idea(
                state=self.state,
                content=result["content"],
                agent_name=agent.name,
                iteration=self.state.iteration,
                parent_ids=result.get("parent_ids", []),
                action_type=result.get("action_type", ""),
                reason=result.get("reason", "")
            )

        self.deduplicate_ideas()
        return state_to_dict(self.state)

    def score_and_vote(self):
        if self.state is None:
            raise ValueError("Chitti session not initialized")

        score_all_ideas(self.state)
        vote_best_ideas(self.state)
        best = choose_best_idea(self.state)
        final_output = self.synthesize_final_answer()

        return {
            "best_idea": best.content if best else None,
            "final_output": final_output,
            "state": state_to_dict(self.state)
        }

    def run_full_process(self, iterations: int = 3):
        if self.state is None:
            raise ValueError("Chitti session not initialized")

        for _ in range(iterations):
            self.run_iteration()

        score_all_ideas(self.state)
        vote_best_ideas(self.state)
        best = choose_best_idea(self.state)
        final_output = self.synthesize_final_answer()

        return {
            "best_idea": best.content if best else None,
            "final_output": final_output,
            "state": state_to_dict(self.state)
        }

    def get_state(self):
        if self.state is None:
            raise ValueError("Chitti session not initialized")

        return state_to_dict(self.state)