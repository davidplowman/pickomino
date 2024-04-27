from enum import Enum
import dice
from throw import Throw

class Action(Enum):
    """Enum class to represet a choice of action, either stop, roll again or give up."""
    GiveUp = 0
    Stop = 1
    Continue = 2

    def label(self):
        return ["give up", "stop", "roll again"][self.value]

class Strategy:
    """
    Base Strategy class, from which actual strategies will need to be derived.

    The base class provides an 'analyse' method to give the expected win in any situation,
    using the strategy defined by the derived 'select_' method.
    """

    def __init__(self):
        """Base class Strategy constructor. Normally you should create a derived class instance."""
        self.clear()

    def clear(self):
        """Clear the cache. Use this if you want to change the board."""
        # This cache helps massively with performance. It's only about 23K entries.
        self.cache_ = [None] * ((dice.MAX_SCORE + 1) * (dice.ALL_USED + 1) * (dice.MAX_NUM + 1))

    def select(self, throw, board, score=0, used=0, history=None):
        """
        Wrapper around the derived select_ method. Normally call this instead.

        The 'history' parameter can be passed as an empty list to get back a list of
        strings that can be printed out to see what work the strategy did.
        """
        if throw.wormed_out(used):
            if history:
                history.append("No dice available")
            return (Action.Stop, -1)
        return self.select_(throw, board, score, used, history)

    def select_(self, throw, board, score, used, history=None):
        """Derived strategy classes must implement this method."""
        raise RuntimeError("No select_ method implemented")

    def analyse(self, board, num_dice, score=0, used=0):
        """
        Return the expected win (or loss, if negative) for the given board and parameters.
        We keep a cache of previous calls for performance reasons. Trust me, you want it.
        """
        # This "hash" value uniquely identifies the parameters, so we can index directly into
        # the cache_ array.
        hash = (score * (dice.ALL_USED + 1) + used) * (dice.MAX_NUM + 1) + num_dice
        entry = self.cache_[hash]
        if not entry:
            entry = self.analyse_(board, num_dice, score, used)
            self.cache_[hash] = entry
        return entry

    def analyse_(self, board, num_dice, score, used):
        """
        Analyse this board with the given number of dice, score and 'used' dice mask.
        Returns the expected payback using this (derived class) strategy.
        """
        expectation = 0
        # Simply loop through all the possible throws of the dice, taking the decisions
        # recommended by the strategy, and accumulating the expected payback from each of
        # these decisions.
        for throw in Throw.all_throws(num_dice):
            if throw.wormed_out(used):
                new_expectation = board.penalty
            else:
                action, die = self.select_(throw, board, score, used)
                new_score = score + throw.histogram[die] * dice.SCORE[die]
                new_used = dice.use(used, die)
                new_num_dice = num_dice - throw.histogram[die]
                if action != Action.Continue or new_num_dice == 0:
                    new_expectation = board.evaluate(new_score, new_used)
                else:
                    new_expectation = self.analyse(board, new_num_dice, new_score, new_used)
            expectation += throw.probability * new_expectation
        return expectation