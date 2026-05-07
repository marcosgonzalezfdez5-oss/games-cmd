"""A simple terminal number guessing game."""

import random

LOWEST_NUMBER = 1
HIGHEST_NUMBER = 500


def get_guess():
    """Ask the player for a valid number."""
    while True:
        guess = input(f"Enter your guess ({LOWEST_NUMBER}-{HIGHEST_NUMBER}): ").strip()

        if not guess.isdigit():
            print("Please type a whole number.")
            continue

        guess = int(guess)
        if LOWEST_NUMBER <= guess <= HIGHEST_NUMBER:
            return guess

        print(f"Please choose a number from {LOWEST_NUMBER} to {HIGHEST_NUMBER}.")


def play_game():
    """Run one complete number guessing game."""
    secret_number = random.randint(LOWEST_NUMBER, HIGHEST_NUMBER)
    attempts = 0

    print("Number Guesser")
    print(f"I picked a number between {LOWEST_NUMBER} and {HIGHEST_NUMBER}.")

    while True:
        guess = get_guess()
        attempts += 1

        if guess < secret_number:
            print("Too low. Guess higher.")
        elif guess > secret_number:
            print("Too high. Guess lower.")
        else:
            print(f"Correct! You guessed it in {attempts} attempts.")
            break


if __name__ == "__main__":
    play_game()
