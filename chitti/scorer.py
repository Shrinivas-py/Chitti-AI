from chitti.memory import ChittiState


def score_text(text: str) -> float:
    t = text.lower()
    score = 0.0

    if len(text) > 20:
        score += 1
    if "practical" in t:
        score += 2
    if "structured" in t:
        score += 2
    if "improve" in t or "refine" in t:
        score += 1
    if "step" in t or "tasks" in t:
        score += 2
    if "solution" in t:
        score += 1

    return score


def score_all_ideas(state: ChittiState):
    for idea in state.ideas:
        idea.score = score_text(idea.content)


def vote_best_ideas(state: ChittiState):
    if not state.ideas:
        return

    max_score = max(idea.score for idea in state.ideas)

    for idea in state.ideas:
        if idea.score == max_score:
            idea.votes += 1


def choose_best_idea(state: ChittiState):
    if not state.ideas:
        return None

    best = sorted(
        state.ideas,
        key=lambda x: (x.score, x.votes, x.iteration),
        reverse=True,
    )[0]

    state.best_idea_id = best.id
    return best
from chitti.memory import ChittiState


def score_text(text: str) -> float:
    t = text.lower()
    score = 0.0

    if len(text) > 20:
        score += 1
    if "practical" in t:
        score += 2
    if "structured" in t:
        score += 2
    if "improve" in t or "refine" in t:
        score += 1
    if "step" in t or "tasks" in t:
        score += 2
    if "solution" in t:
        score += 1

    return score


def score_all_ideas(state: ChittiState):
    for idea in state.ideas:
        idea.score = score_text(idea.content)


def vote_best_ideas(state: ChittiState):
    if not state.ideas:
        return

    max_score = max(idea.score for idea in state.ideas)

    for idea in state.ideas:
        if idea.score == max_score:
            idea.votes += 1


def choose_best_idea(state: ChittiState):
    if not state.ideas:
        return None

    best = sorted(
        state.ideas,
        key=lambda x: (x.score, x.votes, x.iteration),
        reverse=True
    )[0]

    state.best_idea_id = best.id
    return best