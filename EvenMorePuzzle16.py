import random

BOARD_SIZE = 4
GO_AROUND_MOVE_LEFT = "saawd"
GO_AROUND_MOVE_RIGHT = "sddwa"
GO_AROUND_MOVE_UP = "dwwas"
LEFT_TO_RIGHT_UNDER = "sddw"
LEFT_TO_RIGHT_OVER = "wdds"
UP_LEFT_DOWN = "was"
AROUND_ABOVE_MOVE_LEFT = "waasd"
AROUND_ABOVE_MOVE_RIGHT = "wddsa"
UP_RIGHT_DOWN = "wds"
ARRANGE_LAST_TWO_COLS = "dwwas"
GET_PENULTIMATE_NUMBER_OUT_OF_CORNER = "dwassdwawdsa"


def generate_board(size=BOARD_SIZE):
    board = []
    for row_index in range(size):
        row = []
        for number_index in range(size):
            row.append((row_index * size) + number_index + 1)
        board.append(row)
    board[-1][-1] = 0
    return board


def print_board(board):
    for row in board:
        separators = (BOARD_SIZE * 5 + 3) * "-"
        string_row = ""
        print(separators)
        for digit in row:
            string_row += " | "
            if digit != 0:
                string_row += format(digit, '02d')
            else:
                string_row += "  "
        string_row += " |"
        print(string_row)
    print(separators)
    print(" ")


def square_finder(board, value):
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if cell == value:
                return row_index, col_index


def movement(board, movement):
    """Take a string of inputs and perform moves based on each element of the string"""
    for direction in movement:
        empty_x, empty_y = square_finder(board, 0)  # Find the coordinates of the empty field
        target_x, target_y = empty_x, empty_y
        if direction == "w" and empty_x > 0:  # Move once up if not in the top row
            target_x -= 1
        elif direction == "s" and empty_x < BOARD_SIZE - 1:  # Move once left if not in the leftmost column
            target_x += 1
        elif direction == "a" and empty_y > 0:
            target_y -= 1
        elif direction == "d" and empty_y < BOARD_SIZE - 1:  # Move once down if not in the bottom row
            target_y += 1
        board[empty_x][empty_y] = board[target_x][target_y]
        board[target_x][target_y] = 0


def generate_movement_sequence(length=500):
    movements = ""
    for _ in range(length):
        movements += random.choice("wasd")
    return movements


def take_user_input():
    while True:
        direction = input("'w', 'a', 's', or 'd'.")
        if direction in ['w', 'a', 's', 'd']:
            return direction


def move_zero_to_target(empty_row_index, empty_col_index, target_row_index, target_col_index):
    """Returns a sequence of moves to shift the empty space to where the number should ultimately go."""
    sequence = ""
    col_difference = empty_col_index - target_col_index
    if col_difference > 0:
        sequence += ("a" * col_difference)
    else:
        sequence += ("d" * abs(col_difference))  # absolute value of difference to multiply string by a positive number

    row_difference = empty_row_index - target_row_index
    if row_difference > 0:
        sequence += ("w" * row_difference)
    else:
        sequence += ("s" * abs(row_difference))  # absolute value of difference to multiply string by a positive number
    return sequence


def movement_of_standard_element(empty_row_index, empty_col_index, value_row_index, value_col_index):
    """Take empty square located at target, move it to value, then transport value to target"""
    sequence = ""
    col_difference = abs(value_col_index - empty_col_index)
    row_difference = value_row_index - empty_row_index
    if value_row_index == empty_row_index + 1:  # one row below
        sequence += "s"
        if value_col_index > empty_col_index:  # Further right from the target
            go_around_move_left = AROUND_ABOVE_MOVE_LEFT if value_row_index == BOARD_SIZE - 1 else GO_AROUND_MOVE_LEFT
            sequence += ("d" * col_difference) + (go_around_move_left * (col_difference - 1)) + UP_LEFT_DOWN
        elif value_col_index < empty_col_index:  # Further left from the target
            go_around_move_right = AROUND_ABOVE_MOVE_RIGHT if value_row_index == BOARD_SIZE - 1 else GO_AROUND_MOVE_RIGHT
            left_to_right = LEFT_TO_RIGHT_OVER if value_row_index == BOARD_SIZE - 1 else LEFT_TO_RIGHT_UNDER
            sequence += ("a" * col_difference) + (
                    go_around_move_right * (col_difference - 1)) + left_to_right + UP_LEFT_DOWN
    elif value_row_index > empty_row_index + 1:  # More than one row below
        sequence += ("s" * row_difference)
        if value_col_index == empty_col_index:  # Same column
            sequence += (GO_AROUND_MOVE_UP * (row_difference - 1))
        elif value_col_index > empty_col_index:  # Further right from the target
            go_around_move_left = AROUND_ABOVE_MOVE_LEFT if value_row_index == BOARD_SIZE - 1 else GO_AROUND_MOVE_LEFT
            # If number in bottom row, circumvent above, else circumvent below
            sequence += ("d" * col_difference) + (go_around_move_left * (col_difference - 1)) + (UP_LEFT_DOWN) + (
                    GO_AROUND_MOVE_UP * (row_difference - 1))
        else:  # Further left from the target
            go_around_move_right = AROUND_ABOVE_MOVE_RIGHT if value_row_index == BOARD_SIZE - 1 else GO_AROUND_MOVE_RIGHT
            # If number in bottom row, circumvent above, else circumvent below
            sequence += ("a" * col_difference) + (
                    go_around_move_right * (col_difference - 1)) + UP_RIGHT_DOWN + (
                                GO_AROUND_MOVE_UP * (row_difference - 1))
    else:  # On the same row
        direction = "d" if value_col_index > empty_col_index else "a"
        sequence += direction * col_difference
        col_difference -= 1
        move_value_direction = GO_AROUND_MOVE_LEFT if value_col_index > empty_col_index else GO_AROUND_MOVE_RIGHT
        sequence += move_value_direction * col_difference
    return sequence


# def movement_two_rightmost_elements(empty_row_index, empty_col_index, value_row_index, value_col_index):
#     rightmost_number_row_index, rightmost_number_col_index =


def self_solve_algorithm(board, win_con):
    # for number in range(1, BOARD_SIZE * BOARD_SIZE):
    # number = 3
    for number in range(1, 9):
        """Move empty to the target square"""
        print_board(board)
        target_row_index, target_col_index = square_finder(win_con, number)  # Find where a number should be placed
        if board[target_row_index][target_col_index] == win_con[target_row_index][
            target_col_index]:  # Check if the number is already set.
            if not (target_col_index == BOARD_SIZE - 2 and not (
                    board[target_row_index][target_col_index + 1] == win_con[target_row_index][
                target_col_index + 1])):  # If the number is in the third row, we check if the fourth is also set
                continue

        empty_row_index, empty_col_index = square_finder(board, 0)  # Find where the empty square is
        empty_to_target_sequence = move_zero_to_target(empty_row_index, empty_col_index, target_row_index,
                                                       target_col_index)
        movement(board, empty_to_target_sequence)
        if target_row_index < BOARD_SIZE - 2:
            if target_col_index < BOARD_SIZE - 2:
                """Set standard element"""
                empty_row_index, empty_col_index = square_finder(board, 0)
                value_row_index, value_col_index = square_finder(board, number)
                sequence = movement_of_standard_element(empty_row_index, empty_col_index, value_row_index,
                                                        value_col_index)
                movement(board, sequence)
            else:
                """Set the two rightmost numbers in the row by using the standard element function for each,
                but with clever indexation haha"""
                """Set the ultimate number of the row"""
                number_plus_one_value_row, number_plus_one_value_col = square_finder(board, (number + 1))
                empty_row_index, empty_col_index = square_finder(board, 0)
                sequence = movement_of_standard_element(empty_row_index, empty_col_index,
                                                        number_plus_one_value_row, number_plus_one_value_col)
                movement(board, sequence)
                """set the penultimate number of the row below it"""
                sequence = ""
                empty_row_index, empty_col_index = square_finder(board, 0)
                number_plus_one_value_row, number_plus_one_value_col = square_finder(board, (number + 1))
                if empty_col_index > number_plus_one_value_col:  # If the empty square ends up on the right side
                    # of the number, move it to the square below
                    sequence += "sa"
                    movement(board, sequence)
                    empty_row_index, empty_col_index = square_finder(board, 0)
                    sequence = ""
                value_row_index, value_col_index = square_finder(board, number)
                if value_col_index == BOARD_SIZE - 1:  # If the second to last number is stuck in the corner, move it
                    sequence += GET_PENULTIMATE_NUMBER_OUT_OF_CORNER
                    movement(board, sequence)
                sequence = ""
                value_row_index, value_col_index = square_finder(board, number)
                sequence += movement_of_standard_element(empty_row_index, empty_col_index, value_row_index,
                                                         value_col_index)
                movement(board, sequence)
                """Shift the two numbers to set them in place"""
                empty_row_index, empty_col_index = square_finder(board, 0)
                value_row_index, value_col_index = square_finder(board, number)
                sequence = ""
                if empty_col_index > value_col_index:
                    sequence += "sa"
                elif empty_col_index < value_col_index:
                    sequence += "sd"
                sequence += ARRANGE_LAST_TWO_COLS
                movement(board, sequence)

        else:
            """Set the numbers in the two bottom rows"""
            pass

    # empty_row_index, empty_col_index = int(target_row_index), int(target_col_index)
    # if target_row_index == value_row_index and target_col_index == value_col_index:
    #     continue
    # if target_row_index < BOARD_SIZE - 2:
    #     if target_col_index < BOARD_SIZE - 2:
    #         """common case"""
    #     else:
    #          """posledni dve koloni"""
    # else:
    #     """posledni dva reda"""
    #


def main():
    board = generate_board(BOARD_SIZE)
    win_con = generate_board(BOARD_SIZE)
    sequence = generate_movement_sequence(500)
    movement(board, sequence)
    # board = [
    #     [1, 9, 10, 2],
    #     [0, 5, 15, 8],
    #     [13, 11, 12, 6],
    #     [4, 7, 14, 3],
    # ]
    # win_con = generate_board(BOARD_SIZE)
    print_board(board)
    self_solve_algorithm(board, win_con)
    print_board(board)
    while board != win_con:
        movement(board, take_user_input())
        print_board(board)
    print("Congrats, you win!")


if __name__ == "__main__":
    main()
