# Python Standard Library imports
import time

# Program metadata
__author__ = "Peter H."

# Declare constants
DICTIONARY_FILE = "words.txt"
BOARD_FILE = "boards/4x4.txt"
IS_CLEVER = True


# Load a dictionary into a set
def load_dictionary(file_name, board):

    # Create set of all letter in the board
    board_letters = set([word for row in board for word in row])

    # Load stripped lower-case lines into array
    with open(file_name, "r") as file:

        # Keep words only if they can be created with the board_letters
        return set([word.rstrip("\n").lower()
                    for word in file
                    if set(word.rstrip("\n").lower()) <= board_letters])


# Load in a Boggle board into a multi-dimensional array
def load_board(file_name):

    # Load file into multidimensional array "board"
    with open(file_name, "r") as file:
        board = [line.lower().split() for line in file if line.strip()]

    # Check if the board lengths all match
    valid_board = all(len(row) == len(board) for row in board)

    # Handle invalid boards
    if not valid_board:
        raise ValueError("Invalid input board")

    return board


# Prints a Boggle board multi-dimensional array
def print_board(board):

    # Iterate over rows and print space delimited
    for row in board:
        print(" ".join(row).upper())


# Prints a formatted output of the words found
def print_words(words):

    # Initial print and sort words set
    print("Words found:")
    words = sorted(map(str.upper, words))

    # Find all word lengths that exist
    lengths = {len(word) for word in words}
    for word in words:
        if not len(word) in lengths:
            lengths.add(len(word))

    # Print each word that matches the each length
    for length in lengths:
        print(length, "- letter words:", ", ".join(
            [word for word in words if len(word) == length]))

    # Print final word wrapup
    print("\nFound", len(words), "words in total.")
    print("Alpha-sorted list words:")
    print(words)


# Determine which of the possible moves were not already visited
def legal_moves(board, position, move_history):

    # Create list to hold positions and find board size
    positions = []
    size = len(board)

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


# Recursively finds words given a starting position
def find_words(position, clever, move_history):

    # Iterate the total number of moves count
    global total_moves
    total_moves += 1

    # Add current position to history (avoid mutating variable)
    move_history = move_history + [position]

    # Find the legal moves from this position and break if none
    moves = legal_moves(board, position, move_history)
    if not moves:
        return

    # Get the current word created by the history
    word = "".join([board[move[1]][move[0]] for move in move_history])

    # On clever search, break if the current word is not the prefix of any word
    if (clever and
        not any(dict_word.startswith(word) for dict_word in dictionary)):
        return

    # Check if the word in in the dictionary
    if word in dictionary:
        words.add(word)  # Just mutate the provided set

    # Find words at each of the legal moves
    for move in moves:
        find_words(move, clever, move_history)


if __name__ == "__main__":

    # Declare and initialize globals
    board = load_board(BOARD_FILE)
    dictionary = load_dictionary(DICTIONARY_FILE, board)
    words = set()
    total_moves = 0

    #####################
    # Program Execution #
    #####################

    # Print board state
    print_board(board)

    # Print starting messages
    print("\nAnd we're off!")
    print("Running with cleverness:", "ON" if IS_CLEVER else "OFF")

    # Save starting time
    start_time = time.time()

    # Find words at each starting point
    for y in range(len(board)):
        for x in range(len(board)):
            find_words((x, y), IS_CLEVER, [])

    # Save ending time and calculate total elapsed
    end_time = time.time()
    total_time = str(round(end_time - start_time, 3))

    # Print ending messages
    print("All done")
    print("\nSearched total of",
          total_moves, "moves in",
          total_time, "seconds\n")

    # Print words found and close her out
    print_words(words)
