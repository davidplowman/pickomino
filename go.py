import dice
from strategy import Action
from strategy_optimal import StrategyOptimal
from throw import Throw

class Go:
    """
    Class to manage 'taking a go'. It keeps track of your score, which dice have been
    'used', and hold the 'strategy' to use for recommendations.
    """

    def __init__(self, board, strategy=None):
        """Create a Go object to start a new go. Use the optimal strategy if none was given."""
        self.board = board
        self.score = 0
        self.used = 0
        self.throw = None
        if strategy is None:
            strategy = StrategyOptimal()
        self.strategy = strategy

    def roll(self, throw):
        """
        Pass in the dice values that you've thrown (as a tuple or list) and it will recommend
        what to do according to the strategy that was chosen.

        For example, if you've thrown 2 worms, three 4s and a 1 enter:
        go.roll('ww4441')
        """
        if isinstance(throw, str):
            throw = dice.from_string(throw)
        if isinstance(throw, tuple) or isinstance(throw, list):
            if len(throw) > dice.MAX_NUM:
                raise RuntimeError("Too many dice")
            throw = Throw(throw)
        if self.score + throw.num_dice * 5 > dice.MAX_SCORE:
            raise RuntimeError("Potential score overflow")

        if isinstance(throw, str):
            throw = dice.from_string(throw)
        if isinstance(throw, tuple) or isinstance(throw, list):
            throw = Throw(throw)
        self.throw = throw
        history = []
        action, die = self.strategy.select(throw, self.board, self.score, self.used, history)
        for explanation in history:
            print(explanation)
        if die == -1 or action == Action.GiveUp:
            print("Recommendation: give up")
        else:
            print("Recommendation: take", dice.to_string([die]), "and", action.label())

    def take(self, die):
        """
        Update the state of your go with your choice of die.

        For example, continuing the above example, if you decide to take the 4s enter:
        go.take('4')
        """
        if isinstance(die, str):
            die = dice.from_string(die)[0]
        if not self.throw.histogram[die]:
            raise RuntimeError(f"Dice not available in {self.throw}")

        new_score = self.score + self.throw.histogram[die] * dice.SCORE[die]
        new_used = dice.use(self.used, die)
        print("Score updated from", self.score, "to", new_score)
        print("Used updated from", dice.mask_to_string(self.used), "to", dice.mask_to_string(new_used))
        self.score = new_score
        self.used = new_used
