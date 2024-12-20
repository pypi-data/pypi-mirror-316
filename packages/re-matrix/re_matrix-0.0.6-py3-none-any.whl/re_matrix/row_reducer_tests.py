import time

import row_reducer
test_1 = [[8, 2, 3, 4, 7],
          [5, 3, 7, 8, 5],
          [7, 6, 2, 2, 3],
          [7, 9, 2, 5, 2]]

if __name__ == "__main__":

    start_time = time.time()
    # row reduce
    solved_matrix = row_reducer.get_row_reduced_matrix(test_1)
    row_reducer.pretty_print_matrix(solved_matrix)
    # check to make sure it works
    solutions = row_reducer.get_matrix_solutions(solved_matrix)
    correct = row_reducer.check_solution_set(test_1, solutions)
    print(f"matrix solutions are {correct}")
    print(f"Took {time.time() - start_time} seconds to compute matrix")