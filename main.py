# Declare constants
DICTIONARY_FILE = "words.txt"


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


# Determine all possible positions are a given position
def possible_moves(position, board):

    # Get the size of the board (N in NxN) and create list to hold positions
    size = len(board)
    positions = []

    # Iterate over the "9" spaces surrounding the current point (including it)
    for y in range(-1, 2):

        new_y = position[1] + y  # Calculate new y

        for x in range(-1, 2):

            new_x = position[0] + x  # Calculate new x

            # Exclude the positions that are "off" the
            # board and ignore the original position
            if (new_x >= size or new_x < 0 or
                new_y >= size or new_y < 0 or
                (x == 0) and (y == 0)):
                continue

            # Add valid positions to the array
            positions.append((new_y, new_x))

    return positions


# Determine which of the possible moves were not already visited
def legal_moves(possible_moves, move_history):

    # Convert the lists into sets to literally get the difference
    return list(set(possible_moves) - set(move_history))


# Examine new state of board given a new position
def examine_state(board, position, move_history, dictionary):

    # Add current position to history
    move_history.append(position)

    # Get the current word created by the history
    word = "".join(map(lambda p: board[p[0]][p[1]], move_history))

    # Check if the word in in the dictionary
    is_word = word.lower() in dictionary

    # Return tuple of (CURRENT_WORD, WORD_IS_IN_DICTIONARY)
    return (word, is_word)


###########
# Testing #
###########

print("\nTesting Flintstone Functions\n----------------------------\n")

# Load the word dictionary
dictionary = load_dictionary(DICTIONARY_FILE)

# Load and print a board
print("load_board/print_board:")
board = load_board("boards/4x4.txt")
print_board(board)

# Test determination of possible moves
print("\npossible_moves:")
moves = possible_moves((3, 1), board)
print(moves)

# Test determination of legal moves
print("\nlegal_moves:")
print(legal_moves(moves, [(2, 0), (2, 2), (3, 0), (5, 3)]))

# Several example calls of examine_state
print("\nexamine_state:")
print(examine_state(board, (2, 1), [(0, 0), (1, 0), (2, 0)], dictionary))
print(examine_state(board, (0, 1), [(1, 0)], dictionary))
