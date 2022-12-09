"""
Advent of Code 2022: day 8
"""
split_input = open('input.txt').read().splitlines()

rows = tuple([tuple([h for h in row]) for row in split_input])
cols = tuple(zip(*rows))

N_ROWS = len(rows)
N_COLS = len(cols)

visible_trees = set()

for r, row in enumerate(rows):
    max_height = 0
    for c, h in enumerate(row):
        if r == 0 or r == N_ROWS - 1 or c == 0 or c == N_COLS - 1 or h > max_height:
            visible_trees.add(f'{r},{c}')
            max_height = h

        if h == 9:
            break

for r, row in enumerate(rows):
    max_height = 0
    for c, h in enumerate(row[::-1]):
        c = N_COLS - c - 1
        if r == 0 or r == N_ROWS - 1 or c == 0 or c == N_COLS - 1 or h > max_height:
            visible_trees.add(f'{r},{c}')
            max_height = h

        if h == 9:
            break

for c, col in enumerate(cols):
    max_height = 0
    for r, h in enumerate(col):
        if r == 0 or r == N_ROWS - 1 or c == 0 or c == N_COLS - 1 or h > max_height:
            visible_trees.add(f'{r},{c}')
            max_height = h

        if h == 9:
            break

for c, col in enumerate(cols):
    max_height = 0
    for r, h in enumerate(col[::-1]):
        r = N_ROWS - r - 1
        if r == 0 or r == N_ROWS - 1 or c == 0 or c == N_COLS - 1 or h > max_height:
            visible_trees.add(f'{r},{c}')
            max_height = h

        if h == 9:
            break

print(f'part1: {len(visible_trees)}')

scenic_scores = []
for r, row in enumerate(rows):
    for c, h in enumerate(row):
        left = right = top = bottom = 0
        print(f'{r},{c}: {h}')

        # Traverse to left
        for i in range(c - 1, -1, -1):
            left += 1
            if row[i] >= h:
                break

        # Traverse to right
        for i in range(c + 1, N_COLS):
            right += 1
            if row[i] >= h:
                break

        # Traverse to top
        for i in range(r - 1, -1, -1):
            top += 1
            if rows[i][c] >= h:
                break

        # Traverse to bottom
        for i in range(r + 1, N_ROWS):
            bottom += 1
            if rows[i][c] >= h:
                break

        # Compute scenic score
        scenic_scores.append(left * right * top * bottom)

print(f'part2: {max(scenic_scores)}')

