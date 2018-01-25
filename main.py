__author__ = "Peter H."


def load_board(file_name):

    # Load file into multidimensional array "lines"
    with open(file_name) as file:
        file_stripped = [line for line in file if line.strip()]
        lines = [line.split() for line in file_stripped]

    # Check if the board lengths all match
    valid_board = all(len(line) == len(lines) for line in lines)

    # Handle invalid boards
    if not valid_board:
        raise ValueError("Invalid input board")

    return lines


def print_board(board):

    # Iterate over rows and print space delimited
    for row in board:
        print(" ".join(row))


def possible_moves(position, board):

    # Get the size of the board (N in NxN) and
    # create an initial positions list
    size = len(board)
    positions = []

    # Iterate over the "9" spaces surrounding the current point (including it)
    for y in range(-1, 2):
        for x in range(-1, 2):

            # Calculate the new positions
            new_x = position[0] + x
            new_y = position[1] + y

            # Exclude the positions that are "off" the
            # board and ignore the original position
            if (new_x >= size or new_x < 0 or
                new_y >= size or new_y < 0 or
                (x == 0) and (y == 0)):
                continue

            # Add valid positions to the array
            positions.append((position[0] + x, position[1] + y))

    return positions


def legal_moves(possible_moves, move_history):

    # Convert the lists into sets to literally get
    # the difference between the two
    return list(set(possible_moves) - set(move_history))


def examine_state(board, position, move_history):

    # Add current position to history
    move_history.append(position)

    # Get the current word created by the history
    word = ''.join(map(lambda p: board[p[1]][p[0]], move_history))

    # TODO: Create return tuple

    return


# Testing
board = load_board("boards/4x4.txt")
print_board(board)

moves = possible_moves((3, 1), board)
print(moves)

legal_moves(moves, [(2, 0), (2, 2), (3, 0), (5, 3)])

print(examine_state(board, (2, 1), [(0, 0), (1, 0), (2, 0)]))
