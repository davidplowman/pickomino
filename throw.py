from utils import factorial, power_6

import dice

class Throw:
    """
    The Throw class represents what we get once we have thrown some number of dice,
    passed in as a list or tuple of dice indices (which may of course be repeated).
    We store:
        num_dice - the total number of dice in this throw.
        histogram - a 6-bin histogram of the number of occurrences of each dice index.
        probability - the probability of this throw.
    """

    def __init__(self, dice):
        self.num_dice = len(dice)
        self.histogram = [dice.count(i) for i in range(6)]
        # The probability comes from the multinomial distribution.
        divisor = 1
        for c in self.histogram:
            divisor *= factorial(c)
        self.probability = factorial(self.num_dice) / divisor / power_6(self.num_dice)

    def used(self):
        """Return the mask of dice indices used in this throw."""
        return sum([1 << die for die, count in enumerate(self.histogram) if count])

    def wormed_out(self, used_mask):
        """Have we 'wormed out'? i.e. are all dice in this throw already in the mask."""
        return self.used() & (~used_mask) == 0

    def available(self, used_mask, order=(dice.W, 5, 4, 3, 2, 1)):
        """Generator to loop through the dice in this throw not in the mask, in the order given."""
        for die in order:
            count = self.histogram[die]
            if count and not dice.contains(used_mask, die):
                yield (die, count)

    @staticmethod
    def all_throws(num_dice):
        """List of all throws of this many dice."""
        return ALL_THROWS_[num_dice]

    def __repr__(self):
        """More human readable representation of a Throw."""
        d = sum([[i] * c for i, c in enumerate(self.histogram)], [])
        return f"<Throw {dice.to_string(d)} ({self.probability})>"

# We could have used a generator for listing "all dice", but I'd rather have the lists
# ready-generated so as to loop through them quickly.

def generate_(num_dice):
    all = []
    dice = [0] * num_dice
    while True:
        all.append(Throw(dice))
        index = num_dice - 1
        while index >= 0 and dice[index] == 5:
            index -= 1
        if index < 0:
            return all
        dice[index:] = [dice[index] + 1] * (num_dice - index)

ALL_THROWS_ = [generate_(i) for i in range(dice.MAX_NUM + 1)]
