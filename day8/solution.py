"""
Advent of Code 2022: day 8
"""
split_input = open('input.txt').read().splitlines()
rows = tuple([tuple([int(h) for h in row]) for row in split_input])


def compute_visible_trees(_rows: tuple[tuple[int]], _visible_trees: set[str],
                          reverse_dir: bool = False, reverse_coords: bool = False) -> None:
    """
    Compute the visible trees horizontally.
    :param _rows: The rows of the map.
    :param _visible_trees: The set of visible trees.
    :param reverse_dir: Whether to traverse in the opposite direction.
    :param reverse_coords: Whether the coordinates should be reversed.
    """
    # Traverse each row individually
    for _r, row in enumerate(_rows):
        row = row[::-1] if reverse_dir else row
        max_height = 0

        # Traverse column (horizontally)
        for _c, h in enumerate(row):
            _c = len(row) - _c - 1 if reverse_dir else _c

            # Tree visible
            if _r == 0 or _r == len(rows) - 1 or _c == 0 or _c == len(row) - 1 or h > max_height:
                _visible_trees.add(f'{_c},{_r}') if reverse_coords else _visible_trees.add(f'{_r},{_c}')
                max_height = h

            # No more visible trees possible beyond this
            if h == 9:
                break


visible_trees: set[str] = set()

# Traverse horizontally
compute_visible_trees(rows, visible_trees)
compute_visible_trees(rows, visible_trees, reverse_dir=True)

# Traverse vertically
compute_visible_trees(tuple(zip(*rows)), visible_trees, reverse_coords=True)
compute_visible_trees(tuple(zip(*rows)), visible_trees, reverse_coords=True, reverse_dir=True)

print(f'part1: {len(visible_trees)}')


def compute_scenic_score(_rows: tuple[tuple[int]], _r: int, _c: int, _h: int) -> int:
    """
    Compute the scenic score for a given tree with its height and coordinates.
    :param _rows: The rows of the map.
    :param _r: The row of the tree in question.
    :param _c: The column of the tree in question.
    :param _h: The height of the tree in question.
    :return: The scenic score of the tree.
    """
    def _compute_dir(_from: int, _to: int, _step: int, on_col: bool = False) -> int:
        """
        Compute the scenic score in a direction.
        :param _from: Starting index.
        :param _to: Ending index (exclusive).
        :param _step: Step size.
        :param on_col: Whether to check column-wise (or row-wise).
        :return: The scenic score in the direction.
        """
        score = 0
        for i in range(_from, _to, _step):
            # The next tree in the row/col
            tree = _rows[i][_c] if on_col else _rows[_r][i]
            score += 1

            # Scenic score ends here
            if tree >= _h:
                break
        return score

    # Compute the scenic score in each direction
    return (_compute_dir(_c - 1, -1, -1)                         # Left
            * _compute_dir(_c + 1, len(_rows[_r]), 1)            # Right
            * _compute_dir(_r - 1, -1, -1, on_col=True)          # Up
            * _compute_dir(_r + 1, len(_rows), 1, on_col=True))  # Down


scenic_scores: list[int] = []
for r, row in enumerate(rows):
    for c, h in enumerate(row):
        scenic_scores.append(compute_scenic_score(rows, r, c, h))

print(f'part2: {max(scenic_scores)}')
