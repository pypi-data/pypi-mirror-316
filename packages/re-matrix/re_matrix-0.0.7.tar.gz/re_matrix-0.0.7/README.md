# RowReducer
This library row takes a matrix and row reduces it. For example, the following code reduces an example matrix.

```py

from base_re_matrix.re_matrix import row_reducer

example_matrix = [[8, 2, 3, 4],
                  [5, 3, 7, 8],
                  [7, 9, 2, 5]]
reduced_matrix = row_reducer.get_row_reduced_matrix(example_matrix)
row_reducer.pretty_print_matrix(reduced_matrix)
```

