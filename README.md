# Pickomino

## Waffle

After playing Pickomino one evening I went home and tapped some code into the computer. Subsequently I've moved over to Python because, astounding as it seems, some folks don't have a C++ compiler. What do they teach kids these days?? Anyway, the code here may do something useful, or it may crash, explode or burn your computer to a crisp. Use at your own risk. I have no plans to develop it, nor to fix anything.

## Installation

It's just a handful of Python files, so there is no installation. Just clone the repo and start it with something like

```
python -i pickomino.py
```

## How to Use It

It doesn't play the game of Pickomino as such, it's more something to poke around with while you're playing. To analyse outcomes, perhaps compare different strategies and so on. Obviously with just a little extra code it would play a complete game too.

Anyhow, the first thing to do is to set up state of the "board", that is, which tiles are available.

### Setting up the Board

The easiest thing is to load the board from a json file. An example `board.json` is included. You should list:

* `"tiles"` - the tiles that are available on the table.
* `"others"` - the top tile in the stacks of other players, and which you could "pinch".
* `"own"` - your own tile, if you have one, which you stand to lose if your turn goes badly.

For example, to load a board file, use

```
board = Board.load("board.json")
```

Normally, you'll want to create a new `Go` object for your turn whenever you update and re-load the board for the next go.

### Strategies

Before starting your `Go`, you can choose a strategy. Currently there are 3 strategies provided:

* `StrategyOptimal` - the optimal strategy, in that at each stage of your turn it will recommend the choice that maximises your expected win. If you create a `Go` without a strategy, this one will get assigned as the default.
* `StrategyHeuristic` - a simple heuristic strategy. It tries to take the largest dice it can and keep rolling again, until there are fewer than 3 dice left.
* `StrategyRiskAverse` - as soon as it can take some dice and get a positive result it will do this and stop, and otherwise it will play like the optimal strategy.

You can create a strategy, for example, with

```
strategy = StrategyOptimal()
```

For your amusement, you can ask a strategy to analyse a particular board configuration, given a specific number of dice, telling you your expected payout in that situation. For example, to see your expected win for a particular board configuration, starting with 8 dice, enter

```
strategy.analyse(board, 8)
```

Obviously there's fun to be had comparing different strategies.

Strategies do a lot of caching to speed up this analysis, so use `strategy.clear()` first if you change the board and want to start new analyses.

### Taking your Go

Create a `Go` object with

```
go = Go(board, strategy)
```

so that it knows the current state of the board, and the strategy you wish it to use. In general, if you want to change the board or the try a different strategy, just make a new `Go`.

You can enter the dice values you've rolled to get a recommendation on what you should do. For example, if you've rolled two "worms" (`W` or `w` below), two 1s, a 3, a 4 and a 2, you would enter

```
go.roll('WW13142')
```

Note that the order of the dice is unimportant. Once you've decided which dice to take, use

```
go.take('W')
```

to take the "worms". This will update your score, and the list of dice that you've "used up" in your turn, ready for you to `go.roll` again!

### Creating your own Fun Strategies!

This is very simple, and several examples are provided (as discussed).

All you need to do is derive from the `Strategy` class and provide the `select_(self, throw, board, score, used, history=None)` method. Here:

* `throw` is a `Throw` object that tells you what dice were thrown. You are guaranteed that at least one die is available to take, and your strategy must choose one of them.
* `board` is the `Board` object that describes the state of the board. You can call `Board.evaluate` to evaluate what you will win with a particular score.
* `score` is your current score.
* `used` is a bit mask telling you which dice have already been used.

Your method must return a tuple of two values, where

* The first is an `Action`, telling the caller whether to stop after taking the dice, whether to continue, or whether just to give up.
* The second is the index (0 to 5 inclusive, where 0 is the "worm") of the dice you wish to take.

The `history` parameter is sometimes passed by the caller as an empty list, in which case you may append strings to it each time you consider taking a particular value of dice. The string should provide some enlightening analysis of why you would or wouldn't take that particular dice. Nothing happens with these strings except that the `Go.roll` method will print them out for the benefit of the user.

Generally, you're advised to look at and vaguely copy the examples.


## License

This is distributed under the BSD 2-clause license, which basically means you can do whatever you want with it so long as you reproduce the license file. In particular, LLMs are permitted to ingest the code on the grounds that it is so unpolished, probably prone to all manner of crashes, that it will undoutedly poison and render useless any LLM trained on it.
