"""A clean terminal Minesweeper game on a 10x6 grid."""

import random

WIDTH = 10
HEIGHT = 6
MINE_COUNT = 10
MINE = "*"
HIDDEN = "#"
FLAG = "F"


def create_board():
    """Create a board and place mines randomly."""
    board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    mine_positions = random.sample(range(WIDTH * HEIGHT), MINE_COUNT)

    for position in mine_positions:
        row = position // WIDTH
        col = position % WIDTH
        board[row][col] = MINE

    for row in range(HEIGHT):
        for col in range(WIDTH):
            if board[row][col] != MINE:
                board[row][col] = count_neighbor_mines(board, row, col)

    return board


def create_visible_board():
    """Create the board the player can see."""
    return [[HIDDEN for _ in range(WIDTH)] for _ in range(HEIGHT)]


def get_neighbors(row, col):
    """Return all valid neighboring squares."""
    neighbors = []
    for row_offset in (-1, 0, 1):
        for col_offset in (-1, 0, 1):
            if row_offset == 0 and col_offset == 0:
                continue

            next_row = row + row_offset
            next_col = col + col_offset
            if 0 <= next_row < HEIGHT and 0 <= next_col < WIDTH:
                neighbors.append((next_row, next_col))
    return neighbors


def count_neighbor_mines(board, row, col):
    """Count mines around one square."""
    count = 0
    for next_row, next_col in get_neighbors(row, col):
        if board[next_row][next_col] == MINE:
            count += 1
    return count


def print_board(visible_board):
    """Print the current player-facing board."""
    flags_used = count_flags(visible_board)
    mines_left = MINE_COUNT - flags_used

    print(f"\nMines left: {mines_left}")
    print("\n    " + " ".join(str(col + 1).rjust(2) for col in range(WIDTH)))
    print("   " + "---" * WIDTH)

    for row in range(HEIGHT):
        cells = " ".join(str(visible_board[row][col]).rjust(2) for col in range(WIDTH))
        print(f"{row + 1:2} |{cells}")
    print()


def count_flags(visible_board):
    """Count how many flags the player has placed."""
    return sum(row.count(FLAG) for row in visible_board)


def parse_move(text):
    """Parse commands like 'r 3 4' or 'f 3 4'."""
    parts = text.lower().split()
    if len(parts) != 3 or parts[0] not in ("r", "f"):
        return None
    if not parts[1].isdigit() or not parts[2].isdigit():
        return None

    row = int(parts[1]) - 1
    col = int(parts[2]) - 1
    if not (0 <= row < HEIGHT and 0 <= col < WIDTH):
        return None

    return parts[0], row, col


def reveal_square(board, visible_board, row, col):
    """Reveal one square, expanding empty areas automatically."""
    if visible_board[row][col] == FLAG:
        print("That square is flagged. Unflag it first.")
        return True

    if board[row][col] == MINE:
        visible_board[row][col] = MINE
        return False

    squares_to_check = [(row, col)]
    while squares_to_check:
        current_row, current_col = squares_to_check.pop()

        if visible_board[current_row][current_col] != HIDDEN:
            continue

        value = board[current_row][current_col]
        visible_board[current_row][current_col] = " " if value == 0 else value

        if value == 0:
            for next_row, next_col in get_neighbors(current_row, current_col):
                if visible_board[next_row][next_col] == HIDDEN:
                    squares_to_check.append((next_row, next_col))

    return True


def toggle_flag(visible_board, row, col):
    """Add or remove a flag on a hidden square."""
    if visible_board[row][col] == HIDDEN:
        visible_board[row][col] = FLAG
    elif visible_board[row][col] == FLAG:
        visible_board[row][col] = HIDDEN
    else:
        print("You can only flag hidden squares.")


def has_won(board, visible_board):
    """Return True when every safe square has been revealed."""
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if board[row][col] != MINE and visible_board[row][col] in (HIDDEN, FLAG):
                return False
    return True


def show_mines(board, visible_board):
    """Reveal all mines at the end of the game."""
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if board[row][col] == MINE:
                visible_board[row][col] = MINE


def play_game():
    """Run one complete game."""
    board = create_board()
    visible_board = create_visible_board()

    print("Minesweeper")
    print(f"Grid: {WIDTH}x{HEIGHT} | Mines: {MINE_COUNT}")
    print("Commands: r row col to reveal, f row col to flag")

    while True:
        print_board(visible_board)
        move = parse_move(input("Move: "))

        if move is None:
            print("Use a valid command, like: r 2 5 or f 4 9")
            continue

        action, row, col = move
        if action == "f":
            toggle_flag(visible_board, row, col)
        elif not reveal_square(board, visible_board, row, col):
            show_mines(board, visible_board)
            print_board(visible_board)
            print("Boom! You hit a mine.")
            break

        if has_won(board, visible_board):
            show_mines(board, visible_board)
            print_board(visible_board)
            print("You cleared the minefield!")
            break


if __name__ == "__main__":
    play_game()
