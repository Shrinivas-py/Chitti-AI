import random
from chitti.memory import ChittiState


class ChittiAgent:
    def __init__(self, name: str):
        self.name = name

    def generate_idea(self, state: ChittiState) -> dict:
        if state.iteration == 1 or len(state.ideas) == 0:
            starter_ideas = [
                "Day 1: Learn HTML basics and build a simple webpage",
                "Day 2: Learn CSS styling and responsive design",
                "Day 3: Practice Flexbox and CSS Grid layouts",
                "Day 4: Learn JavaScript basics and syntax",
                "Day 5: Add interactivity using JavaScript DOM manipulation",
                "Day 6: Build a mini frontend project using HTML, CSS, and JavaScript",
                "Day 7: Revise concepts and build a final portfolio-style project"
            ]

            return {
                "content": random.choice(starter_ideas),
                "parent_ids": [],
                "action_type": "new_idea",
                "reason": "Created an initial raw idea"
            }

        existing_idea = random.choice(state.ideas)

        refinements = [
            f"{existing_idea.content} with one hands-on mini project",
            f"{existing_idea.content} and include 1 hour of revision",
            f"{existing_idea.content} while focusing on practical implementation",
            f"{existing_idea.content} and connect it with the next day's topic"
        ]

        return {
            "content": random.choice(refinements),
            "parent_ids": [existing_idea.id],
            "action_type": "refine",
            "reason": "Improved an existing idea"
        }


def build_agents(count: int = 5):
    return [ChittiAgent(f"chitti_agent_{i}") for i in range(1, count + 1)]