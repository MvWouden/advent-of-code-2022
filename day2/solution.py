"""
Advent of Code 2022: day 2
"""
split_input = open('input.txt', 'r').read().splitlines()

states: dict = {  # Win, draw, loss based on pick
    'AX': 3,
    'AY': 6,
    'AZ': 0,
    'BX': 0,
    'BY': 3,
    'BZ': 6,
    'CX': 6,
    'CY': 0,
    'CZ': 3,
}
points: dict = {  # Base points for selection
    'X': 1,
    'Y': 2,
    'Z': 3,
}
solution = sum([                                      # Compute total score of rounds
    states[round[0] + round[-1]] + points[round[-1]]  # Determine round count
    for round in split_input                          # Split into rounds
])
print(f'part1: {solution}')

points_pt2: dict = {  # Points for win, draw, loss
    'X': 0,
    'Y': 3,
    'Z': 6,
}
pick_pt2: dict = {  # Base points based on win, draw, loss
    'AX': 3,
    'AY': 1,
    'AZ': 2,
    'BX': 1,
    'BY': 2,
    'BZ': 3,
    'CX': 2,
    'CY': 3,
    'CZ': 1,
}
solution = sum([                                             # Compute total score of rounds
    pick_pt2[round[0] + round[-1]] + points_pt2[round[-1]]   # Determine round count
    for round in split_input                                 # Split into rounds
])
print(f'part2: {solution}')
