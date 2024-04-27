import dice
from strategy import Action, Strategy

class StrategyHeuristic(Strategy):
    """
    A slightly random 'heuristic' strategy.

    It will take the largest dice value it can and keep rolling again, but will
    decide to stop if it's achieved a positive evaluation and there are fewer than
    3 dice remaining.
    """

    def __init__(self):
        super().__init__()

    def select_(self, throw, board, score, used, history=None):
        best = None
        # First look for the best thing that gives us a positive evaluation right now.
        for die, count in throw.available(used, order=(dice.W, 5, 4, 3, 2, 1)):
            new_num_dice = throw.num_dice - count
            new_used = dice.use(used, die)
            new_score = score + count * dice.SCORE[die]
            evaluation = board.evaluate(new_score, new_used)
            if history is not None:
                history.append(f"Take {die}: {evaluation} leaving {new_num_dice} dice")
            if best is None or evaluation > best[2]:
                best = (die, new_num_dice, evaluation)

        if best is not None and best[2] > 0:
            # We found something. Decide whether to stop or continue.
            action = Action.Stop if best[1] < 3 else Action.Continue
            return (action, best[0])
            
        # Otherwise take the largest dice and carry on.
        for die, count in throw.available(used, order=(dice.W, 5, 4, 3, 2, 1)):
            return (Action.Continue, die)
