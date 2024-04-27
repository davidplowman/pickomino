"""
A dice is represented by an index number, from 0 to 5 inclusive. We use 0 to represet
a 'worm'. The index needs to be looked up in the SCORE array to get the score for a
die with that index.

Collections of dice can be represented as a list or tuple of indices, but we also
use a mask to remember which dice have been 'seen'. We can turn these into strings
for human consumption. So the string 'W5' would represent the mask 33.

Also for humans, we can convert lists of tuples of dice indices to or from
readable strings. For example, [0, 3, 0] (a 3 and 2 worms) would become 'W3W'.
"""

MAX_NUM = 8

WORM = 0
W = WORM

ALL_USED = 63

SCORE = [5, 1, 2, 3, 4, 5]

MAX_SCORE = MAX_NUM * max(SCORE)

def use(mask, die):
    """Add the new die index to the dice mask."""
    return mask | (1 << die)

def contains(mask, die):
    """Does the dice mask already contain this die?"""
    return mask & (1 << die)

def contains_worm(mask):
    """Does the dice mask already contain a 'worm'?"""
    return contains(mask, WORM)

LABELS_ = {0: 'W', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}

def to_string(dice):
    """Convert a list or tuple of dice indices to a readable string."""
    return "".join([LABELS_[d] for d in dice])

INDICES_ = {'W': 0, 'w': 0, '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5}

def from_string(s):
    """Convert a dice string to a list of dice indicies."""
    return [INDICES_[c] for c in s]

def mask_to_string(mask):
    """Convert a dice mask to a string."""
    return "".join([LABELS_[d] for d in range(6) if (1 << d) & mask])

def string_to_mask(s):
    """Convert a string to a dice mask."""
    return sum([1 << INDICES_[c] for c in s])