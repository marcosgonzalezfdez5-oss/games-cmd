# Terminal Python Games

A small collection of beginner-friendly terminal games written in Python 3.

No external libraries are required. Each game runs directly in the console.

## Games

### Tic-Tac-Toe

Play as `X` against the computer as `O`.

Features:

- 3x3 numbered board
- Easy and hard difficulty levels
- Hard mode uses minimax and is unbeatable
- Input validation and win/draw detection

Run:

```powershell
python tictactoe.py
```

### Minesweeper

Clear a `10x6` grid without hitting a mine.

Features:

- 10 columns by 6 rows
- Reveal and flag commands
- Automatic empty-area reveal
- Mine counter that updates as flags are placed

Run:

```powershell
python minesweeper.py
```

Commands:

```text
r row col   reveal a square
f row col   flag or unflag a square
```

Example:

```text
r 2 5
f 4 9
```

### Blackjack

Play Blackjack against the dealer.

Features:

- Standard 52-card deck
- Hit or stand choices
- Dealer draws until 17
- Ace handling as 1 or 11
- Optional hints with simple card-count awareness
- Deck carries across rounds and reshuffles when low

Run:

```powershell
python blackjack.py
```

### Number Guesser

Guess a random number between `1` and `500`.

Features:

- Higher/lower feedback after each guess
- Input validation
- Attempt counter

Run:

```powershell
python number_guesser.py
```

## Requirements

- Python 3
- A terminal or command prompt

## Running The Project

Open a terminal in this folder, then run the game you want:

```powershell
python ./games/tictactoe.py
python ./games/minesweeper.py
python ./games/blackjack.py
python ./games/number_guesser.py
python ./games/sudoku.py
```
