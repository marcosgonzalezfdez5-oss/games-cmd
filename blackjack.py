"""A clean terminal Blackjack game."""

import random

SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")
RANKS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
RESHUFFLE_AT = 15


def create_deck():
    """Create and shuffle a standard 52-card deck."""
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck


def card_value(rank):
    """Return the starting value for a card rank."""
    if rank == "A":
        return 11
    if rank in ("J", "Q", "K"):
        return 10
    return int(rank)


def count_card(card):
    """Return the Hi-Lo count value for a visible card."""
    rank, _ = card
    if rank in ("2", "3", "4", "5", "6"):
        return 1
    if rank in ("10", "J", "Q", "K", "A"):
        return -1
    return 0


def hand_value(hand):
    """Calculate a hand total, counting aces as 1 when needed."""
    total = sum(card_value(rank) for rank, _ in hand)
    aces = sum(1 for rank, _ in hand if rank == "A")

    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total


def is_soft_hand(hand):
    """Return True if the hand has an ace currently counted as 11."""
    total = sum(card_value(rank) for rank, _ in hand)
    aces = sum(1 for rank, _ in hand if rank == "A")

    while total > 21 and aces:
        total -= 10
        aces -= 1

    return aces > 0


def dealer_upcard_value(dealer_hand):
    """Return the value of the dealer's visible card."""
    visible_rank = dealer_hand[1][0]
    return card_value(visible_rank)


def get_basic_hint(player_hand, dealer_hand):
    """Recommend hit or stand using simple Blackjack strategy."""
    total = hand_value(player_hand)
    dealer_value = dealer_upcard_value(dealer_hand)
    dealer_label = dealer_hand[1][0]

    if is_soft_hand(player_hand):
        if total <= 17:
            return "hit", "your ace gives you room to improve safely"
        if total == 18 and dealer_value >= 9:
            return "hit", f"soft 18 is weak against dealer {dealer_label}"
        return "stand", "your soft total is strong enough to keep"

    if total <= 11:
        return "hit", "you cannot bust with one more card"
    if total == 12:
        if 4 <= dealer_value <= 6:
            return "stand", f"dealer {dealer_label} is more likely to bust"
        return "hit", "12 is too low against this dealer card"
    if 13 <= total <= 16:
        if 2 <= dealer_value <= 6:
            return "stand", f"dealer {dealer_label} is in a weak position"
        return "hit", "the dealer has a strong upcard"

    return "stand", "17 or more is usually strong enough"


def get_hint(player_hand, dealer_hand, running_count):
    """Recommend hit or stand, including a small card-count adjustment."""
    recommendation, reason = get_basic_hint(player_hand, dealer_hand)
    total = hand_value(player_hand)
    dealer_value = dealer_upcard_value(dealer_hand)
    count_text = f"running count is {running_count:+d}"

    # A positive count means more high cards remain, so standing becomes safer
    # in a few close situations. A negative count favors taking another card.
    if not is_soft_hand(player_hand):
        if total == 16 and dealer_value == 10 and running_count >= 2:
            return "stand", f"{count_text}, so forcing the dealer to draw is better"
        if total == 15 and dealer_value == 10 and running_count >= 4:
            return "stand", f"{count_text}, so the deck favors dealer bust chances"
        if total == 12 and 2 <= dealer_value <= 3 and running_count >= 3:
            return "stand", f"{count_text}, so standing is safer than usual"
        if total == 12 and 4 <= dealer_value <= 6 and running_count <= -2:
            return "hit", f"{count_text}, so standing is less attractive"

    return recommendation, f"{reason}; {count_text}"


def format_card(card):
    """Return a readable card name."""
    rank, suit = card
    return f"{rank} of {suit}"


def print_hand(name, hand, hide_first_card=False):
    """Print one hand and its total."""
    if hide_first_card:
        visible_cards = ["Hidden card", format_card(hand[1])]
        print(f"{name}: {', '.join(visible_cards)}")
        return

    cards = ", ".join(format_card(card) for card in hand)
    print(f"{name}: {cards}  (total: {hand_value(hand)})")


def deal_card(deck, hand):
    """Move one card from the deck to a hand."""
    card = deck.pop()
    hand.append(card)
    return card


def ask_yes_no(prompt):
    """Ask a yes/no question."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("Please type y or n.")


def get_player_choice():
    """Ask the player to hit or stand."""
    while True:
        choice = input("Hit or stand? (h/s): ").strip().lower()
        if choice in ("h", "hit"):
            return "hit"
        if choice in ("s", "stand"):
            return "stand"
        print("Please type h to hit or s to stand.")


def player_turn(deck, player_hand, dealer_hand, hints_enabled, running_count):
    """Run the player's turn. Return bust status and updated count."""
    while True:
        print()
        print_hand("Dealer", dealer_hand, hide_first_card=True)
        print_hand("You", player_hand)
        
        if hand_value(player_hand) > 21:
            print("You busted!")
            return False, running_count

        if hints_enabled:
            recommendation, reason = get_hint(player_hand, dealer_hand, running_count)
            print(f"Hint: {recommendation.title()} - {reason}.")

        if get_player_choice() == "stand":
            return True, running_count

        running_count += count_card(deal_card(deck, player_hand))


def dealer_turn(deck, dealer_hand, running_count):
    """Dealer reveals the hidden card, then hits until reaching 17 or more."""
    running_count += count_card(dealer_hand[0])
    while hand_value(dealer_hand) < 17:
        running_count += count_card(deal_card(deck, dealer_hand))
    return running_count


def print_final_hands(player_hand, dealer_hand):
    """Show both final hands."""
    print()
    print_hand("Dealer", dealer_hand)
    print_hand("You", player_hand)
    print()


def announce_winner(player_hand, dealer_hand):
    """Compare final totals and print the result."""
    player_total = hand_value(player_hand)
    dealer_total = hand_value(dealer_hand)

    if dealer_total > 21:
        print("Dealer busted. You win!")
    elif player_total > dealer_total:
        print("You win!")
    elif player_total < dealer_total:
        print("Dealer wins.")
    else:
        print("Push. It's a tie.")


def play_round(deck, hints_enabled, running_count):
    """Play one round of Blackjack."""
    player_hand = []
    dealer_hand = []

    for _ in range(2):
        deal_card(deck, player_hand)
        deal_card(deck, dealer_hand)

    for card in player_hand:
        running_count += count_card(card)
    running_count += count_card(dealer_hand[1])

    if hand_value(player_hand) == 21:
        running_count += count_card(dealer_hand[0])
        print_final_hands(player_hand, dealer_hand)
        if hand_value(dealer_hand) == 21:
            print("Both have blackjack. Push.")
        else:
            print("Blackjack! You win!")
        return running_count

    player_still_in, running_count = player_turn(
        deck, player_hand, dealer_hand, hints_enabled, running_count
    )
    if player_still_in:
        running_count = dealer_turn(deck, dealer_hand, running_count)
        print_final_hands(player_hand, dealer_hand)
        announce_winner(player_hand, dealer_hand)

    return running_count


def play_game():
    """Run Blackjack until the player quits."""
    print("Blackjack")
    print("Try to get closer to 21 than the dealer without going over.")
    hints_enabled = ask_yes_no("Show hints? (y/n): ")
    deck = create_deck()
    running_count = 0

    while True:
        if len(deck) < RESHUFFLE_AT:
            print("\nShuffling a fresh deck.")
            deck = create_deck()
            running_count = 0

        running_count = play_round(deck, hints_enabled, running_count)
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Thanks for playing!")
            break
        print()


if __name__ == "__main__":
    play_game()
