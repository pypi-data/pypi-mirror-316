import random
from matrix_math_helpers import dot_product, subtract_row_a_from_b, multiply_row, divide_row


def get_row_reduced_matrix(matrix):
    """
    :param matrix: a rectangular matrix to be row reduced
    :return: the row reduced form of matrix
    """
    copy_matrix = matrix.copy()
    if not is_matrix_rectangular(copy_matrix):
        raise ValueError("Input matrix must be rectangular to perform row reduction.")

    row_length = len(copy_matrix[0])
    for col in range(len(copy_matrix[0])):
        for row in range(len(copy_matrix)):
            # only row reduce the spot in the matrix if:
            # 1. it's not a leading zero
            # 2. it's not zeroed already
            # 3. It's not in the rightmost column (the right side of the equation
            if row != col and copy_matrix[row][col] != 0 and col != row_length-1:
                zero_value_with_reduction(copy_matrix, row, col)
            # this line is optional, but prevents the matrix values from getting absurdley high
            reduce_row_to_lowest_terms(copy_matrix, row)
    return copy_matrix


def reduce_row_to_lowest_terms(matrix, row):
    """
    Reduced a row to lowest terms, based on the first non-zero value e.g [3, 6, 9] becomes [1, 2, 3]
    :param matrix:
    :param row:
    :return:
    """
    for c in range(len(matrix[row])):
        if matrix[row][c] != 0:
            divide_row(matrix, row, matrix[row][c])
            break


def zero_value_with_reduction(matrix, row, col):
    """
    Zeros value at matrix[row][col] using the others rows in the matrix using reduction
    """
    if matrix[row][col] == 0:
        return
    # To zero the matrix[row] row, find another row to subtract from it
    for i in range(len(matrix)):
        # all values to the left of col in the selected row need to be 0s
        if matrix[i][col] != 0 and i != row and all(x == 0 for x in matrix[i][:col]):
            stored_list = matrix[i]
            # multiply both rows together so that matrix[row][col] = matrix[i][col]
            factor1 = matrix[i][col]
            factor2 = matrix[row][col]
            multiply_row(matrix, row, factor1)
            multiply_row(matrix, i, factor2)
            subtract_row_a_from_b(matrix, i, row)
            matrix[i] = stored_list # reset the row to the lowest form
            return


def reduce_rows_to_lowest_terms(matrix):
    """
    Reduces the row so that at least one of the terms is 1
    E.g [5, 0, 0, 15] -> [1, 0, 0, 3]
    :param matrix:
    :return:
    """
    for r in range(len(matrix)):
        reduce_row_to_lowest_terms(matrix, r)


def is_matrix_rectangular(matrix):
    """
    :param matrix: returns true if a matrix is rectangular
    :return:
    """
    row_length = len(matrix[0])
    for row in matrix:
        if len(row) != row_length:
            return False
    return True


def pretty_print_matrix(matrix):
    """
    :param matrix: prints a matrix in an aesthetically pleasing way
    :return: n/a
    """
    print("------------------")
    # Determine the maximum width of each column
    col_widths = []
    for col in range(len(matrix[0])):
        # a list representing the length of each item in the column
        col_lengths = (len(str(row[col])) for row in matrix)
        # the column is as wide as the largest item
        col_widths.append(max(col_lengths))

    # Print each row with the columns aligned
    for row in matrix:
        formatted_row = "  ".join(f"{str(item).rjust(width)}" for item, width in zip(row, col_widths))
        print(formatted_row)
    print("------------------")


def get_matrix_solutions(row_reduced_matrix):
    """
    :param row_reduced_matrix: a matrix that is in row reduced form
    :return: The solution set of the row reduced matrix, e.g [x_0, x_1, x_2, ...]
    """
    solution_set = []
    for i in range(len(row_reduced_matrix)):
        if all(x == 0 for x in row_reduced_matrix[i][:-1]):
            # when there is no solution from that line
            solution_set.append(None)
        else:
            solution_set.append(row_reduced_matrix[i][-1])
    return solution_set


def print_solution_set(solution_set):
    """
    :param solution_set: a solution set, such as the one returned by get_matrix_solutions
    :return: n/a
    """
    print("the solution set is: ")
    for i in range(len(solution_set)):
        print(f"x_{i} = {solution_set[i]}")


def analyze_and_row_reduce_matrix(matrix):
    """
    An all-in-one function for getting the row reducing from of a matrix,
    finding the solutions,
    and printing the output in a pleasing way.
    :param matrix: a matrix, in either row reduced or original form
    :return: n/a
    """
    print("original matrix:")
    pretty_print_matrix(matrix)
    row_reduced_matrix = get_row_reduced_matrix(matrix)
    print("solved matrix:")
    pretty_print_matrix(row_reduced_matrix)
    solution_set = get_matrix_solutions(row_reduced_matrix)
    print_solution_set(solution_set)
    correct = check_solution_set(matrix, solution_set)
    if correct:
        print("The solution set solves the original matrix")
    else:
        print("The matrix cannot be solved")


def check_solution_set(original_matrix, solution_set):
    """
    :param original_matrix: The matrix that's not row-reduced
    :param solution_set: a list of [x_1, x_2, x_3...]
    :return:
    """
    def is_a_within_margin_of_b(a, b):
        margin_of_error = 0.00005
        return b + margin_of_error > a > b - margin_of_error

    for row in original_matrix:
        coefficients = row[:-1]
        row_sum = row[-1]
        dot = dot_product(coefficients, solution_set)
        if not is_a_within_margin_of_b(sum(dot), row_sum):
            return False
    return True



