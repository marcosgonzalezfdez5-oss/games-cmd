"""A beginner-friendly terminal Tic-Tac-Toe game with two AI levels."""

import random

PLAYER = "X"
COMPUTER = "O"
WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def print_board(board):
    """Print the board as a 3x3 grid."""
    print()
    for row in range(0, 9, 3):
        print(f" {board[row]} | {board[row + 1]} | {board[row + 2]} ")
        if row < 6:
            print("---+---+---")
    print()


def check_winner(board):
    """Return 'X' or 'O' if a player has won, otherwise None."""
    for a, b, c in WIN_LINES:
        if board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board):
    """Return True when the board is full and nobody has won."""
    return check_winner(board) is None and not get_available_moves(board)


def get_available_moves(board):
    """Return a list of open cell indexes."""
    return [i for i, cell in enumerate(board) if cell not in (PLAYER, COMPUTER)]


def player_move(board):
    """Ask the player for a valid move and update the board."""
    while True:
        choice = input("Choose a square (1-9): ").strip()

        if not choice.isdigit():
            print("Please type a number from 1 to 9.")
            continue

        move = int(choice) - 1
        if move < 0 or move > 8:
            print("That number is outside the board. Try 1 to 9.")
        elif board[move] in (PLAYER, COMPUTER):
            print("That square is already taken. Choose another one.")
        else:
            board[move] = PLAYER
            return


def choose_difficulty():
    """Ask the player to choose Easy or Hard mode."""
    while True:
        print("Choose difficulty:")
        print("1. Easy")
        print("2. Hard (unbeatable)")
        choice = input("Enter 1 or 2: ").strip()

        if choice == "1":
            return "easy"
        if choice == "2":
            return "hard"
        print("Please choose 1 for Easy or 2 for Hard.\n")


def find_winning_move(board, symbol):
    """Return a move that lets symbol win immediately, if one exists."""
    for move in get_available_moves(board):
        original = board[move]
        board[move] = symbol
        if check_winner(board) == symbol:
            board[move] = original
            return move
        board[move] = original
    return None


def easy_computer_move(board):
    """Play a simple, beatable move."""
    move = find_winning_move(board, COMPUTER)
    if move is None:
        move = find_winning_move(board, PLAYER)
    if move is None:
        move = random.choice(get_available_moves(board))

    board[move] = COMPUTER
    print(f"Computer chooses {move + 1}.")


def minimax(board, is_computer_turn):
    """Score the board by looking ahead at every possible move."""
    winner = check_winner(board)
    if winner == COMPUTER:
        return 1
    if winner == PLAYER:
        return -1
    if is_draw(board):
        return 0

    scores = []
    symbol = COMPUTER if is_computer_turn else PLAYER

    for move in get_available_moves(board):
        original = board[move]
        board[move] = symbol
        scores.append(minimax(board, not is_computer_turn))
        board[move] = original

    return max(scores) if is_computer_turn else min(scores)


def hard_computer_move(board):
    """Choose the best move for the computer using minimax."""
    best_score = -2
    best_move = None

    for move in get_available_moves(board):
        original = board[move]
        board[move] = COMPUTER
        score = minimax(board, False)
        board[move] = original

        if score > best_score:
            best_score = score
            best_move = move

    board[best_move] = COMPUTER
    print(f"Computer chooses {best_move + 1}.")


def computer_move(board, difficulty):
    """Choose a move based on the selected difficulty."""
    if difficulty == "easy":
        easy_computer_move(board)
    else:
        hard_computer_move(board)


def play_game():
    """Run one complete game."""
    board = [str(i) for i in range(1, 10)]

    print("Tic-Tac-Toe")
    print("You are X. The computer is O.")
    difficulty = choose_difficulty()
    print_board(board)

    while True:
        player_move(board)
        print_board(board)

        if check_winner(board) == PLAYER:
            print("You win!")
            break
        if is_draw(board):
            print("It's a draw!")
            break

        computer_move(board, difficulty)
        print_board(board)

        if check_winner(board) == COMPUTER:
            print("Computer wins!")
            break
        if is_draw(board):
            print("It's a draw!")
            break


if __name__ == "__main__":
    play_game()
