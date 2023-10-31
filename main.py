"""
CP1404 - Guessing Game for review and refactor
Some of this is "good" code, but some things are intentionally poor
This is for a code review and refactoring exercise
"""
import math
import random

FILENAME = "scores.txt"

DEFAULT_LOW = 1
DEFAULT_HIGH = 10


def main():
    """Menu-driven guessing game with option to change high limit."""
    low = DEFAULT_LOW
    high = DEFAULT_HIGH
    number_of_games = 0
    print("Welcome to the guessing game")
    choice = input("(P)lay, (S)et limit, (H)igh scores, (Q)uit: ").upper()
    while choice != "Q":
        if choice == "P":
            play(low, high)
            number_of_games += 1
        elif choice == "S":
            high = set_limit(low)
        elif choice == "H":
            display_scores()
        else:
            print("Invalid choice")
        choice = input("(P)lay, (S)et limit, (H)igh scores, (Q)uit: ").upper()
    print(f"Thanks for playing ({number_of_games} times)!")


def play(low, high):
    """Play guessing game using current low and high values."""
    secret = random.randint(low, high)
    number_of_guesses = 1
    guess = int(input(f"Guess a number between {low} and {high}: "))
    while guess != secret:
        number_of_guesses += 1
        if guess < secret:
            print("Higher")
        else:
            print("Lower")
        guess = int(input(f"Guess a number between {low} and {high}: "))
    print(f"You got it in {number_of_guesses} guesses.")
    if is_good_score(number_of_guesses, high - low + 1) is True:
        print("Good guessing!")
    choice = input("Do you want to save your score? (y/N) ")
    if choice.upper() == "Y":
        write_score_to_file(number_of_guesses, low, high, FILENAME)
    else:
        print("Fine then.")


def write_score_to_file(number_of_guesses, low, high, filename):
    """Save score to scores.txt with range"""
    with open(filename, "a") as outfile:
        print(f"{number_of_guesses}|{high - low + 1}", file=outfile)


def set_limit(low):
    """Set high limit to new value from user input."""
    print("Set new limit")
    new_high = get_valid_number(f"Enter a new high value, above {low}: ")
    while new_high <= low:
        print("Higher!")
        new_high = get_valid_number(f"Enter a new high value, above {low}: ")
    return new_high


def get_valid_number(prompt):
    """Get a valid integer from the user."""
    is_valid = False
    while not is_valid:
        try:
            number = int(input(prompt))
            is_valid = True
        except ValueError:
            print("Invalid number")
    return number


def is_good_score(number_of_guesses, range_):
    """Determine if number of guesses is less than or equal to
     range calculation."""
    return number_of_guesses <= math.ceil(math.log2(range_))


def display_scores():
    """Display scores in descending order with good score markers."""
    scores = load_scores(FILENAME)
    scores.sort()
    for score in scores:
        marker = "!" if is_good_score(score[0], score[1]) else ""
        print(f"{score[0]} ({score[1]}) {marker}")


def load_scores(filename):
    """Load scores from a file and return scores list."""
    scores = []
    with open(filename) as in_file:
        for line in in_file:
            line = line.split("|")
            scores.append((int(line[0]), int(line[1])))
    return scores


main()