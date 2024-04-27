from board import Board
from go import Go
from strategy import Action
from strategy_heuristic import StrategyHeuristic
from strategy_optimal import StrategyOptimal
from strategy_risk_averse import StrategyRiskAverse
from throw import Throw
import dice

b = Board.load("board.json")
so = StrategyOptimal()
sh = StrategyHeuristic()
sr = StrategyRiskAverse()
g = Go(b, so)

# Use like this:
# g.roll('wwww1233')
# g.take('w')

# Or to analyse a strategy:
# so.analyse(b, 8)