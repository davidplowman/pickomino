import dice
from strategy import Action, Strategy

class StrategyOptimal(Strategy):
    """
    Optimal derived strategy class.

    It works by trying to take each possible value of die from the throw, and seeing
    what the expected payout will be if it does that, selecting the highest one. It
    has to check both what happens if it takes the dice and stops, or if it takes them
    and commits to rolling again.
    """

    def __init__(self):
        super().__init__()

    def select_(self, throw, board, score, used, history=None):
        eps = 1e-6
        best = None
        # Try each die value that is available in this throw.
        for die, count in throw.available(used):
            new_score = score + count * dice.SCORE[die]
            new_used = dice.use(used, die)
            # This will be what happens if we take the dice and stop.
            stop_expectation = board.evaluate(new_score, new_used)
            if best is None or stop_expectation > best[2] + eps:
                best = (Action.Stop, die, stop_expectation)
            # And here's what happens if we take the dice and roll again.
            new_num_dice = throw.num_dice - count
            cont_expectation = self.analyse(board, new_num_dice, new_score, new_used)
            if new_num_dice and cont_expectation > best[2] + eps:
                best = (Action.Continue, die, cont_expectation)
            if history is not None:
                die_label = dice.to_string([die])
                history.append(f"Take {die_label}: stop {stop_expectation} continue {cont_expectation}")
        # Basically that's it, but if our best choice is as bad as it can get, then we
        # may as well recommend giving up.
        if best[2] < board.penalty + eps:
            return (Action.GiveUp, die)
        return best[:2]
