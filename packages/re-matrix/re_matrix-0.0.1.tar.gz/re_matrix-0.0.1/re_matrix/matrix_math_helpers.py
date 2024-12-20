import random


def dot_product(row_a, row_b):
    """
    e.g [a, b, c]  * [d, e, f] = [ad, be, fc]
    :param row_a:
    :param row_b:
    :return:
    """
    result = [a * b for a, b in zip(row_a, row_b)]
    return result


def add_row_a_to_b(matrix, row_a_number, row_b_number):
    matrix[row_b_number] = [a + b for a, b in zip(matrix[row_a_number], matrix[row_b_number])]


def subtract_row_a_from_b(matrix, row_a_number, row_b_number):
    """
    modifies matrix, essentially matrix[row_b_number] = matrix[row_b_number] - matrix[row_a_number]
    :param matrix: the matrix to be modified
    :param row_a_number: a row number, must be within len(matrix)
    :param row_b_number: a row number, must be within len(matrix)
    :return:
    """
    matrix[row_b_number] = [b - a for a, b in zip(matrix[row_a_number], matrix[row_b_number])]


def multiply_row(matrix, row, factor):
    matrix[row] = [item * factor for item in matrix[row]]


def divide_row(matrix, row, divisor):
    matrix[row] = [item / divisor for item in matrix[row]]


def create_test_matrix(width, height, min_value, max_value):
    """
    Creates random matrices for testing purposes
    :param width: the width of the resulting matrix
    :param height: the height of the resulting matrix
    :param min_value: the minimum value an item in the matrix can be
    :param max_value: the maximum value an item in the matrix can be
    :return: a width * height matrix
    """
    result = []
    for h in range(height):
        row = []
        for w in range(width):
            row.append(random.randint(min_value, max_value))
        result.append(row)
    return result
