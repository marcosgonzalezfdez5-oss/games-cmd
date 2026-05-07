"""A terminal Sudoku game with Medium and Hard difficulty levels."""

import random

MEDIUM_REMOVALS = 42
HARD_REMOVALS = 52
SEP = "  +----------+----------+----------+"
HEADER = "     1  2  3    4  5  6    7  8  9"


def is_valid_placement(board, row, col, num):
    """Return True if placing num at (row, col) doesn't break any constraint."""
    if num in board[row]:
        return False
    if any(board[r][col] == num for r in range(9)):
        return False
    box_row, box_col = (row // 3) * 3, (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False
    return True


def create_solved_board():
    """Generate a complete valid 9x9 board using randomized backtracking."""
    board = [[0] * 9 for _ in range(9)]

    def fill(board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    candidates = list(range(1, 10))
                    random.shuffle(candidates)
                    for num in candidates:
                        if is_valid_placement(board, r, c, num):
                            board[r][c] = num
                            if fill(board):
                                return True
                            board[r][c] = 0
                    return False
        return True

    fill(board)
    return board


def count_solutions(board, limit=2):
    """Count distinct solutions up to limit; stops early once limit is reached."""
    board = [row[:] for row in board]

    def solve(board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    count = 0
                    for num in range(1, 10):
                        if is_valid_placement(board, r, c, num):
                            board[r][c] = num
                            count += solve(board)
                            board[r][c] = 0
                            if count >= limit:
                                return count
                    return count
        return 1

    return solve(board)


def create_puzzle(solved_board, removals):
    """Remove cells while preserving a unique solution."""
    puzzle = [row[:] for row in solved_board]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    removed = 0

    for r, c in cells:
        if removed == removals:
            break
        backup = puzzle[r][c]
        puzzle[r][c] = 0
        if count_solutions(puzzle) == 1:
            removed += 1
        else:
            puzzle[r][c] = backup

    return puzzle


def choose_difficulty():
    """Ask the player to choose Medium or Hard; return (removals, name)."""
    while True:
        print("Choose difficulty:")
        print("1. Medium")
        print("2. Hard")
        choice = input("Enter 1 or 2: ").strip()
        if choice == "1":
            return MEDIUM_REMOVALS, "Medium"
        if choice == "2":
            return HARD_REMOVALS, "Hard"
        print("Please choose 1 for Medium or 2 for Hard.\n")


def print_board(current_board, puzzle_board, difficulty_name):
    """Print the Sudoku grid with column labels, box separators, and styled cells."""
    print(f"\nSudoku  |  {difficulty_name}  |  hint: h  quit: q\n")
    print(HEADER)

    for r in range(9):
        if r % 3 == 0:
            print(SEP)
        row_str = f"{r + 1} "
        for c in range(9):
            if c % 3 == 0:
                row_str += "| "
            val = current_board[r][c]
            if val == 0:
                cell = " . "
            elif puzzle_board[r][c] != 0:
                cell = f" {val} "
            else:
                cell = f"[{val}]"
            row_str += cell
        row_str += "|"
        print(row_str)

    print(SEP)
    print()


def parse_move(text):
    """Parse player input; return a command tuple or None on bad input."""
    text = text.strip().lower()
    if text in ("quit", "q"):
        return ("quit", 0, 0)
    if text in ("hint", "h"):
        return ("hint", 0, 0)

    parts = text.split()
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        return None

    row, col, val = int(parts[0]) - 1, int(parts[1]) - 1, int(parts[2])
    if not (0 <= row < 9 and 0 <= col < 9 and 1 <= val <= 9):
        return None

    return ("move", row, col, val)


def apply_move(current_board, puzzle_board, row, col, value):
    """Write a move to the board; return a status string."""
    if puzzle_board[row][col] != 0:
        return "clue"
    current_board[row][col] = value
    return "ok"


def give_hint(current_board, puzzle_board, solved_board):
    """Reveal one random empty non-clue cell from the solution."""
    empty = [
        (r, c)
        for r in range(9)
        for c in range(9)
        if puzzle_board[r][c] == 0 and current_board[r][c] == 0
    ]
    if not empty:
        print("No empty cells to hint.")
        return False
    r, c = random.choice(empty)
    current_board[r][c] = solved_board[r][c]
    return True


def is_solved(current_board, solved_board):
    """Return True when the current board matches the solution exactly."""
    return all(
        current_board[r][c] == solved_board[r][c]
        for r in range(9)
        for c in range(9)
    )


def play_game():
    """Run one complete Sudoku game."""
    print("Sudoku")
    removals, difficulty_name = choose_difficulty()
    print("\nGenerating puzzle...")

    solved_board = create_solved_board()
    puzzle_board = create_puzzle(solved_board, removals)
    current_board = [row[:] for row in puzzle_board]

    print_board(current_board, puzzle_board, difficulty_name)
    print("Enter: row col value  (e.g. 2 5 7)  |  h for hint  |  q to quit")

    while True:
        result = parse_move(input("\nMove: "))

        if result is None:
            print("Invalid input. Use: row col value (e.g. 2 5 7), h for hint, q to quit.")
            continue

        action = result[0]

        if action == "quit":
            print("Thanks for playing!")
            break

        if action == "hint":
            give_hint(current_board, puzzle_board, solved_board)

        elif action == "move":
            _, row, col, val = result
            status = apply_move(current_board, puzzle_board, row, col, val)
            if status == "clue":
                print("That's a starting clue — you can't change it.")
                continue

        print_board(current_board, puzzle_board, difficulty_name)

        if is_solved(current_board, solved_board):
            print("Congratulations! You solved the puzzle!")
            break


if __name__ == "__main__":
    play_game()
