# Python Standard Library imports
import time

# Program metadata
__author__ = "Peter H."

# Declare constants
DICTIONARY_FILE = "words.txt"
BOARD_FILE = "boards/4x4.txt"


# Load a dictionary into a set
def load_dictionary(file_name):

    # Load stripped lower-case lines into array
    with open(file_name, "r") as file:
        lines = [line.rstrip("\n").lower() for line in file]

    # Return dictionary object as a set to improve lookup times
    return set(lines)


# Load in a Boggle board into a multi-dimensional array
def load_board(file_name):

    # Load file into multidimensional array "lines"
    with open(file_name, "r") as file:
        file_stripped = [line for line in file if line.strip()]
        lines = [line.split() for line in file_stripped]

    # Check if the board lengths all match
    valid_board = all(len(line) == len(lines) for line in lines)

    # Handle invalid boards
    if not valid_board:
        raise ValueError("Invalid input board")

    return lines


# Prints a Boggle board multi-dimensional array
def print_board(board):

    # Iterate over rows and print space delimited
    for row in board:
        print(" ".join(row))


def print_words(words):
    print("TODO")
    print(words)


# Determine which of the possible moves were not already visited
def legal_moves(board, position, move_history):

    # Get the size of the board (N in NxN) and create list to hold positions
    size = len(board)
    positions = []

    # Iterate over the "9" spaces surrounding the current point (including it)
    for y in range(-1, 2):
        new_y = position[1] + y  # Calculate new y

        for x in range(-1, 2):
            new_point = (position[0] + x, new_y)  # Calculate new point

            # Exclude the positions that are "off" the board or visited
            if (new_point[0] >= size or new_point[0] < 0 or
                new_point[1] >= size or new_point[1] < 0 or
                new_point in move_history):
                continue

            # Add valid positions to the array
            positions.append(new_point)

    return positions


def find_words(words, position, clever, move_history=[]):

    # Add current position to history (avoid mutating variable)
    move_history = move_history + [position]

    # Find the legal moves from this position
    moves = legal_moves(board, position, move_history)

    # If there are no valid moves
    if not moves:
        return words

    # Get the current word created by the history
    word = "".join(map(lambda p: board[p[1]][p[0]], move_history))

    # Check if the word in in the dictionary
    if word.lower() in dictionary and word not in words:
        words.append(word)  # Just mutate the provided array

    # Find words down every legal move path
    for move in moves:
        global total_moves
        total_moves += 1
        words = find_words(words, move, clever, move_history)

    return words


if __name__ == "__main__":

    # Declare and initialize globals
    dictionary = load_dictionary(DICTIONARY_FILE)
    board = load_board(BOARD_FILE)
    words = []
    total_moves = len(board) ** 2
    clever = False

    #####################
    # Program Execution #
    #####################

    # Print initial informational message
    if clever:
        print("OUTPUT FROM NOT-QUITE-SO-NEANDERTHAL APPROACH. "
              "Check out those stats!\n")
    else:
        print("OUTPUT FROM FLINTSTONE CLASSIC BAM-BAM BASH-IT APPROACH:\n")

    # Print board state
    print_board(board)

    # Print starting messages
    print("\nAnd we're off!")
    print("Running with cleverness:", "ON" if clever else "OFF")

    # Save starting time
    start_time = time.time()

    # Find words at each starting point
    for y in range(len(board)):
        for x in range(len(board)):
            find_words(words, (x, y), clever)

    # Save ending time and calculate total elapsed
    end_time = time.time()
    total_time = str(round(end_time - start_time, 3))

    # Print ending messages
    print("All done")
    print("\nSearched total of",
          total_moves, "moves in",
          total_time, "seconds\n")

    # Print word stats
    print_words(words)

    print("\nProcess finished with exit code 0\n")
