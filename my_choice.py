"""
Your choice rule, for Part 3.

You design the rule. Claude asks you questions about it, writes it here from your answers, and
shows you the code. Then `uv run python hand_check.py` shows each step of your rule on a
two-artist case, so you can say whether each step does what you meant.
"""

from artists import TRUE_POPULARITY
from choose import normalize, step


def my_choice(shown, counts, social_influence):
    """Return the chance that a user picks each shown artist: a list of numbers, one per artist
    in `shown` and in the same order, summing to 1.

    shown              the artists on the list, top first (positions 0, 1, 2, ...)
    counts             the download counts shown with the artists, artist -> number; an artist
                       shown without a count is missing, so read it as counts.get(artist, 0)
    social_influence   from 0 (users ignore the counts) to 1 (users go by the counts alone)

    The rule may use `normalize`, which scales a list of weights so they sum to 1, and
    TRUE_POPULARITY, which gives each artist its hidden true popularity. `step` labels each
    stage of the rule, so that hand_check.py can show it.
    """
    taste = step("taste share: true popularity scaled to sum to 1",
                 normalize([TRUE_POPULARITY[artist] for artist in shown]))
    weights = step("download pull: square root of each count",
                   [counts.get(artist, 0) ** 0.5 for artist in shown])
    if sum(weights) == 0:
        social = step("social share: no shown artist has a download, so true popularity instead",
                      taste)
    else:
        social = step("social share: the pulls scaled to sum to 1", normalize(weights))
    chances = step("chance: taste share times (1 - social_influence) plus social share times social_influence",
                   [(1 - social_influence) * t + social_influence * s
                    for t, s in zip(taste, social)])
    return chances
