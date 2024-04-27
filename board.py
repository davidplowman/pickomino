import json

import dice
import tile

class Board:
    """
    The state of the "board", that is:
        tiles - what tiles are available on the table to grab.
        others - the topmost tile of the other playes, that can be pinched.
        own - your own top tile, that you stand to lose!

    After reading the board description (usually a json file), we calculate the expected
    'payout' for each final score and store it. This is pretty much all we need to know,
    along with the 'penalty' associated with your own tile if you lose it.
    """

    def __init__(self, tiles=[], others=[], own=None):
        self.tiles_ = tiles
        self.others_ = others
        self.own_ = own
        self.penalty = 0
        self.update_payouts_()

    @property
    def tiles(self):
        """Tiles available to be won."""
        return self.tiles_

    @tiles.setter
    def tiles(self, value):
        """Set the list of tiles that can be won."""
        self.tiles_ = sorted(value)
        self.update_payouts_()

    @property
    def others(self):
        """Other player's tiles than can be pinched."""
        return self.others_

    @others.setter
    def others(self, value):
        """Set the list of other player's tiles."""
        self.others_ = sorted(value)
        self.update_payouts_()

    @property
    def own(self):
        """Your own tile, that you stand to lose."""
        return self.own_

    @own.setter
    def own(self, value):
        """Set the tile that you might lose, or None if you don't have one."""
        self.own_ = value
        self.update_payouts_()

    @property
    def payouts(self):
        return self.payouts_

    def update_payouts_(self):
        """Update the list of payouts associated with each score, plus your own 'penalty'."""
        self.penalty = 0
        if self.own_:
            if self.own_ > tile.MAX:
                raise RuntimeError("Invalid 'own' tile")
            self.penalty = -tile.VALUES[self.own_]
        self.payouts_ = [self.penalty] * (dice.MAX_SCORE + 1)
        for t in self.tiles:
            if t > tile.MAX:
                raise RuntimeError("Invalid tile in 'tiles' list")
            self.payouts_[t:] = [tile.VALUES[t]] * (dice.MAX_SCORE + 1 - t)
        for t in self.others:
            if t > tile.MAX:
                raise RuntimeError("Invalid tile in 'others' list")
            self.payouts_[t] = tile.VALUES[t]

    def evaluate(self, score, used):
        """Evaluate what you would win with this score given the board state."""
        if dice.contains_worm(used):
            return self.payouts_[score]
        return self.penalty;

    @staticmethod
    def from_dict(dict):
        """Make a Board from a dictionary."""
        return Board(tiles=dict.get('tiles', []), others=dict.get('others', []), own=dict.get('own'))

    @staticmethod
    def load(file="board.json"):
        """Load a Board from a json file."""
        with open(file, 'r') as f:
            dict = json.load(f)
        return Board.from_dict(dict)

    def __repr__(self):
        """Human friendly representation of a Board."""
        return f"<Board tiles={self.tiles_} others={self.others_} own={self.own_}>"