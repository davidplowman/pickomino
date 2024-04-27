import dice
from strategy_optimal import Action, StrategyOptimal

class StrategyRiskAverse(StrategyOptimal):
    """
    A highly risk averse strategy.

    As soon as it can take some dice and achieve a positive score, it will do that
    and stop (checking that it's taking the best choice among these). Otherwise it
    plays optimally.
    """

    def __init__(self):
        super().__init__()

    def select_(self, throw, board, score, used, history=None):
        best = None
        # Choose the best outcome and stop if we can achieve a positive evaluation.
        for die, count in throw.available(used):
            new_used = dice.use(used, die)
            new_score = score + count * dice.SCORE[die]
            evaluation = board.evaluate(new_score, new_used)
            if best is None or evaluation > best[1]:
                best = (die, evaluation)
        if best is not None and best[1] > 0:
            return (Action.Stop, best[0])
                
        # Otherwise use the optimal strategy.
        return super().select_(throw, board, score, used, history)
